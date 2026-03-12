"""Fetch and parse Substack, blog posts, and newsletters from URLs.

Reads URLs from data/writers/urls.txt in format:
    writer_name | url
"""

import logging
from pathlib import Path

import httpx
from bs4 import BeautifulSoup

from src.config.settings import settings
from src.schemas.engagement import PostRecord
from src.ingestion.docx_parser import ingest_posts

logger = logging.getLogger(__name__)


def parse_urls_file(file_path: Path) -> list[tuple[str, str]]:
    """Parse urls.txt into (writer_name, url) tuples."""
    entries = []
    if not file_path.exists():
        logger.info("No urls.txt found. Skipping URL scraping.")
        return entries

    for line in file_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "|" in line:
            parts = line.split("|", 1)
            writer_name = parts[0].strip()
            url = parts[1].strip()
            entries.append((writer_name, url))
        else:
            logger.warning(f"Skipping malformed line in urls.txt: {line}")

    return entries


def fetch_article(url: str) -> str | None:
    """Fetch a URL and extract the main article text."""
    try:
        response = httpx.get(url, timeout=30, follow_redirects=True)
        response.raise_for_status()
    except httpx.HTTPError as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove noise elements
    for tag in soup(["nav", "footer", "header", "script", "style", "aside"]):
        tag.decompose()

    # Try common article containers
    article = (
        soup.find("article")
        or soup.find("div", class_=lambda c: c and "post-content" in c)
        or soup.find("div", class_=lambda c: c and "entry-content" in c)
        or soup.find("div", class_=lambda c: c and "body" in c)
        or soup.find("main")
    )

    if article:
        text = article.get_text(separator="\n", strip=True)
    else:
        # Fallback: extract from body
        body = soup.find("body")
        text = body.get_text(separator="\n", strip=True) if body else ""

    # Clean up excessive whitespace
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    cleaned = "\n".join(lines)

    if len(cleaned) < 100:
        logger.warning(f"Very short content extracted from {url} ({len(cleaned)} chars)")
        return None

    return cleaned


def scrape_urls() -> dict[str, list[PostRecord]]:
    """Scrape all URLs from urls.txt and return posts by writer.

    Returns: dict mapping writer_name -> list of PostRecords.
    """
    urls_file = settings.writers_dir / "urls.txt"
    entries = parse_urls_file(urls_file)

    if not entries:
        return {}

    posts_by_writer: dict[str, list[str]] = {}

    for writer_name, url in entries:
        logger.info(f"Scraping: {writer_name} <- {url}")
        text = fetch_article(url)
        if text:
            posts_by_writer.setdefault(writer_name, []).append(text)
        else:
            logger.warning(f"  No content extracted from {url}")

    # Ingest into storage
    result: dict[str, list[PostRecord]] = {}
    for writer_name, texts in posts_by_writer.items():
        records = ingest_posts(writer_name, texts)
        result[writer_name] = records
        logger.info(f"Scraped {len(records)} articles for {writer_name}")

    return result
