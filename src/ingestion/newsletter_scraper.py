"""Scrape newsletters from Substack and Beehiiv, ingest into storage + Brain.

Orchestrates the full pipeline:
  1. Detect platform (Substack or Beehiiv)
  2. Scrape posts via JSON API endpoints (no API keys needed)
  3. Store in SQLite + ChromaDB (via existing ingest_posts)
  4. Save raw JSON to data/scraped/ for audit trail
  5. Return structured data for Brain synthesis (done by Claude via /ingest skill)

Usage from CLI:
  python3 -m src.ingestion.newsletter_scraper --url "https://www.lennysnewsletter.com" --days 30
  python3 -m src.ingestion.newsletter_scraper --url "https://www.growthunhinged.com" --days 60
  python3 -m src.ingestion.newsletter_scraper --url "https://newsletter.substack.com" --full-content
"""

import argparse
import hashlib
import json
import logging
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import requests

from src.config.settings import settings
from src.schemas.engagement import PostRecord
from src.ingestion.docx_parser import ingest_posts

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "application/json",
    "Sec-Fetch-Dest": "empty",
}

SCRAPED_DIR = settings.data_dir / "scraped"


# ---------------------------------------------------------------------------
# Platform detection
# ---------------------------------------------------------------------------

def detect_platform(url: str) -> str:
    """Detect whether a URL is Substack, Beehiiv, or unknown."""
    url = url.rstrip("/")

    # Check Substack first (subdomain or custom domain with /api/v1/archive)
    if "substack.com" in url:
        return "substack"

    try:
        resp = requests.get(
            f"{url}/api/v1/archive?sort=new&limit=1&offset=0",
            headers=HEADERS, timeout=10,
        )
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, list):
                return "substack"
    except Exception:
        pass

    # Check Beehiiv (hidden /posts endpoint)
    try:
        resp = requests.get(
            f"{url}/posts?page=0&perPage=1",
            headers=HEADERS, timeout=10,
        )
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, dict) and "posts" in data:
                return "beehiiv"
    except Exception:
        pass

    # Check HTML source for platform hints
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            text = resp.text[:5000]
            if "beehiiv" in text.lower():
                return "beehiiv"
            if "substackcdn" in text.lower() or "substack" in text.lower():
                return "substack"
    except Exception:
        pass

    return "unknown"


# ---------------------------------------------------------------------------
# Substack scraper
# ---------------------------------------------------------------------------

def scrape_substack(base_url: str, max_posts: Optional[int] = None) -> list[dict]:
    """Fetch posts from Substack via /api/v1/archive."""
    base_url = base_url.rstrip("/")
    all_posts = []
    offset = 0
    page_size = 12

    while True:
        url = f"{base_url}/api/v1/archive?sort=new&limit={page_size}&offset={offset}"
        logger.info(f"Substack: fetching offset {offset}")

        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
            posts = resp.json()
        except Exception as e:
            logger.error(f"Failed to fetch {url}: {e}")
            break

        if not isinstance(posts, list) or len(posts) == 0:
            break

        all_posts.extend(posts)

        if max_posts and len(all_posts) >= max_posts:
            all_posts = all_posts[:max_posts]
            break
        if len(posts) < page_size:
            break

        offset += page_size

    return [_normalize_substack(p, base_url) for p in all_posts]


def fetch_substack_post_body(base_url: str, slug: str) -> Optional[str]:
    """Fetch full HTML body of a Substack post."""
    url = f"{base_url}/api/v1/posts/{slug}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        return data.get("body_html") or data.get("body") or data.get("truncated_body_text")
    except Exception as e:
        logger.warning(f"Could not fetch body for {slug}: {e}")
    return None


def _normalize_substack(post: dict, base_url: str) -> dict:
    slug = post.get("slug", "")
    canonical = post.get("canonical_url") or f"{base_url}/p/{slug}"
    bylines = post.get("publishedBylines", [])

    return {
        "platform": "substack",
        "title": post.get("title") or "",
        "subtitle": post.get("subtitle") or "",
        "slug": slug,
        "url": canonical,
        "date": post.get("post_date") or post.get("published_at") or "",
        "author": bylines[0].get("name", "") if bylines else "",
        "tags": [t.get("name", "") for t in post.get("postTags", [])],
        "image_url": post.get("cover_image") or post.get("social_image") or "",
        "word_count": post.get("wordcount") or 0,
        "reactions": post.get("reactions", {}).get("❤", 0) if isinstance(post.get("reactions"), dict) else 0,
        "comment_count": post.get("comment_count") or 0,
        "description": post.get("description") or post.get("truncated_body_text") or "",
        "is_paid": post.get("audience") == "only_paid",
    }


# ---------------------------------------------------------------------------
# Beehiiv scraper
# ---------------------------------------------------------------------------

def scrape_beehiiv(base_url: str, max_posts: Optional[int] = None) -> list[dict]:
    """Fetch posts from Beehiiv via /posts endpoint."""
    base_url = base_url.rstrip("/")
    all_posts = []
    seen_ids = set()
    page = 0
    page_size = 30

    while True:
        url = f"{base_url}/posts?page={page}&perPage={page_size}"
        logger.info(f"Beehiiv: fetching page {page + 1}")

        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            logger.error(f"Failed to fetch {url}: {e}")
            break

        posts = data.get("posts", [])
        pagination = data.get("pagination", {})

        if not posts:
            break

        # Deduplicate
        new_posts = [p for p in posts if p["id"] not in seen_ids]
        seen_ids.update(p["id"] for p in new_posts)
        all_posts.extend(new_posts)

        if max_posts and len(all_posts) >= max_posts:
            all_posts = all_posts[:max_posts]
            break

        total_pages = pagination.get("total_pages", 1)
        page += 1
        if page >= total_pages:
            break

    return [_normalize_beehiiv(p, base_url) for p in all_posts]


def _normalize_beehiiv(post: dict, base_url: str) -> dict:
    authors = post.get("authors", [])
    tags = [t.get("display", "") for t in post.get("content_tags", [])]

    return {
        "platform": "beehiiv",
        "title": post.get("web_title") or "",
        "subtitle": post.get("web_subtitle") or "",
        "slug": post.get("slug", ""),
        "url": f"{base_url}/p/{post.get('slug', '')}",
        "date": post.get("created_at") or "",
        "author": authors[0].get("name", "") if authors else "",
        "tags": tags,
        "image_url": post.get("image_url") or "",
        "word_count": 0,
        "reactions": 0,
        "comment_count": 0,
        "description": post.get("web_subtitle") or "",
        "is_paid": post.get("is_premium", False),
    }


# ---------------------------------------------------------------------------
# Filtering
# ---------------------------------------------------------------------------

def filter_posts(
    posts: list[dict],
    days: Optional[int] = None,
    keywords: Optional[list[str]] = None,
) -> list[dict]:
    """Filter posts by date and keywords."""
    filtered = posts

    if days is not None:
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        date_filtered = []
        for p in filtered:
            date_str = p.get("date", "")
            if not date_str:
                date_filtered.append(p)
                continue
            try:
                dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                if dt >= cutoff:
                    date_filtered.append(p)
            except ValueError:
                date_filtered.append(p)
        filtered = date_filtered

    if keywords:
        kw_lower = [k.lower() for k in keywords]
        filtered = [
            p for p in filtered
            if any(
                kw in f"{p.get('title', '')} {p.get('subtitle', '')} {p.get('description', '')} {' '.join(p.get('tags', []))}".lower()
                for kw in kw_lower
            )
        ]

    return filtered


# ---------------------------------------------------------------------------
# Full-content fetching
# ---------------------------------------------------------------------------

def fetch_full_content(posts: list[dict], base_url: str) -> None:
    """Fetch full body HTML for each post (modifies posts in place)."""
    for i, p in enumerate(posts):
        slug = p.get("slug", "")
        if not slug:
            continue

        logger.info(f"  [{i+1}/{len(posts)}] Fetching body: {slug}")

        if p["platform"] == "substack":
            body = fetch_substack_post_body(base_url, slug)
            if body:
                p["body_html"] = body
        # Beehiiv full content would require Remix context parsing — skip for now


# ---------------------------------------------------------------------------
# Storage pipeline
# ---------------------------------------------------------------------------

def _make_post_id(source: str, slug: str, title: str) -> str:
    hash_input = f"{source}:{slug}:{title[:100]}"
    return hashlib.sha256(hash_input.encode()).hexdigest()[:16]


def save_raw_json(source_name: str, posts: list[dict]) -> Path:
    """Save raw scraped data to data/scraped/ for audit trail."""
    SCRAPED_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = source_name.lower().replace(" ", "_").replace("'", "")
    filename = f"{slug}_{timestamp}.json"
    filepath = SCRAPED_DIR / filename

    filepath.write_text(json.dumps(posts, indent=2, default=str))
    logger.info(f"Raw data saved to {filepath}")
    return filepath


def store_posts(source_name: str, posts: list[dict]) -> list[PostRecord]:
    """Ingest scraped posts into SQLite + ChromaDB via existing pipeline.

    Builds text content from title + subtitle + description (or body if available)
    to create meaningful embeddings in ChromaDB.
    """
    texts = []
    for p in posts:
        # Build a rich text representation for embedding
        parts = []
        if p.get("title"):
            parts.append(p["title"])
        if p.get("subtitle"):
            parts.append(p["subtitle"])
        if p.get("body_html"):
            # Strip HTML tags for plain text
            import re
            plain = re.sub(r"<[^>]+>", " ", p["body_html"])
            plain = re.sub(r"\s+", " ", plain).strip()
            parts.append(plain)
        elif p.get("description"):
            parts.append(p["description"])

        if p.get("tags"):
            parts.append(f"Tags: {', '.join(p['tags'])}")

        text = "\n\n".join(parts)
        if len(text) > 50:
            texts.append(text)

    if not texts:
        logger.warning(f"No posts to store for {source_name}")
        return []

    records = ingest_posts(source_name, texts)
    logger.info(f"Stored {len(records)} posts for '{source_name}' in SQLite + ChromaDB")
    return records


def build_brain_synthesis_brief(source_name: str, posts: list[dict]) -> str:
    """Build a structured brief for Claude to synthesize into Brain updates.

    This output is designed to be consumed by the /ingest skill,
    which will analyze it and update the relevant Brain sections.
    """
    lines = [
        f"# Newsletter Ingestion Brief: {source_name}",
        f"Posts scraped: {len(posts)}",
        f"Platform: {posts[0]['platform'] if posts else 'unknown'}",
        f"Author: {posts[0].get('author', 'unknown') if posts else 'unknown'}",
        "",
        "## Posts (newest first)",
        "",
    ]

    for i, p in enumerate(posts[:30], 1):  # Cap at 30 for context window
        date = (p.get("date") or "")[:10]
        lines.append(f"### {i}. {p.get('title', 'Untitled')} ({date})")
        if p.get("subtitle"):
            lines.append(f"*{p['subtitle']}*")
        if p.get("tags"):
            lines.append(f"Tags: {', '.join(p['tags'])}")
        if p.get("word_count"):
            lines.append(f"Word count: {p['word_count']}")
        if p.get("reactions") or p.get("comment_count"):
            lines.append(f"Engagement: {p.get('reactions', 0)} reactions, {p.get('comment_count', 0)} comments")
        if p.get("body_html"):
            import re
            plain = re.sub(r"<[^>]+>", " ", p["body_html"])
            plain = re.sub(r"\s+", " ", plain).strip()
            lines.append(f"\n{plain[:2000]}")
        elif p.get("description"):
            lines.append(f"\n{p['description'][:500]}")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## Brain Synthesis Instructions",
        "",
        "Analyze the above posts and update the following PMM Brain sections:",
        "",
        "1. **newsletter_insights**: Add/update entry for this source with:",
        "   - focus, key_frameworks, key_data_points, contrarian_insights, useful_for",
        "",
        "2. **evidence_bank**: Extract any concrete stats, benchmarks, or data points",
        "",
        "3. **pmm_value_landscape**: Note any contested or emerging beliefs",
        "",
        "4. **synthesized_mental_models**: Extract any new mental models or frameworks",
        "",
        "5. **topic_depth_layers**: Add practitioner wisdom, common mistakes, key debates",
    ])

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------

def scrape_newsletter(
    url: str,
    source_name: Optional[str] = None,
    days: Optional[int] = None,
    max_posts: Optional[int] = None,
    keywords: Optional[list[str]] = None,
    full_content: bool = False,
    store: bool = True,
) -> dict:
    """Full pipeline: detect → scrape → filter → store → prepare brain brief.

    Returns a dict with:
        - posts: normalized post list
        - source_name: detected or provided source name
        - platform: substack|beehiiv
        - raw_file: path to saved JSON
        - records: list of PostRecords stored
        - brain_brief: text for Brain synthesis
    """
    url = url.rstrip("/")

    # Detect platform
    platform = detect_platform(url)
    if platform == "unknown":
        raise ValueError(
            f"Could not detect platform for {url}. "
            "Supported: Substack, Beehiiv (including custom domains)."
        )

    logger.info(f"Detected platform: {platform} for {url}")

    # Scrape
    if platform == "substack":
        posts = scrape_substack(url, max_posts=max_posts)
    else:
        posts = scrape_beehiiv(url, max_posts=max_posts)

    if not posts:
        raise ValueError(f"No posts found at {url}")

    # Auto-detect source name from first post's author
    if not source_name:
        source_name = posts[0].get("author") or url.split("//")[1].split("/")[0]

    logger.info(f"Scraped {len(posts)} posts from {source_name} ({platform})")

    # Filter
    posts = filter_posts(posts, days=days, keywords=keywords)
    logger.info(f"After filtering: {len(posts)} posts")

    # Fetch full content if requested
    if full_content:
        fetch_full_content(posts, url)

    result = {
        "posts": posts,
        "source_name": source_name,
        "platform": platform,
        "url": url,
        "raw_file": None,
        "records": [],
        "brain_brief": build_brain_synthesis_brief(source_name, posts),
    }

    if store:
        # Save raw JSON
        result["raw_file"] = str(save_raw_json(source_name, posts))

        # Store in SQLite + ChromaDB
        result["records"] = store_posts(source_name, posts)

    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    parser = argparse.ArgumentParser(
        description="Scrape newsletters and ingest into the PMM Brain pipeline",
    )
    parser.add_argument("--url", required=True, help="Newsletter URL")
    parser.add_argument("--name", help="Source name (auto-detected if omitted)")
    parser.add_argument("--days", type=int, help="Only include posts from last N days")
    parser.add_argument("--max-posts", type=int, help="Max posts to return")
    parser.add_argument("--keywords", help="Filter by keywords (comma-separated)")
    parser.add_argument("--full-content", action="store_true", help="Fetch full post bodies (slower)")
    parser.add_argument("--no-store", action="store_true", help="Skip storage, just print results")
    parser.add_argument("--output", choices=["summary", "json", "brain-brief"], default="summary")

    args = parser.parse_args()
    keywords = [k.strip() for k in args.keywords.split(",")] if args.keywords else None

    result = scrape_newsletter(
        url=args.url,
        source_name=args.name,
        days=args.days,
        max_posts=args.max_posts,
        keywords=keywords,
        full_content=args.full_content,
        store=not args.no_store,
    )

    posts = result["posts"]

    if args.output == "brain-brief":
        print(result["brain_brief"])
    elif args.output == "json":
        print(json.dumps(posts, indent=2, default=str))
    else:
        # Summary table
        print(f"\n{'='*80}")
        print(f"  {result['source_name']} ({result['platform']})")
        print(f"  {len(posts)} posts scraped | stored: {len(result['records'])}")
        if result["raw_file"]:
            print(f"  Raw data: {result['raw_file']}")
        print(f"{'='*80}\n")

        print(f"{'#':<4} {'Date':<12} {'Title'}")
        print("-" * 80)
        for i, p in enumerate(posts, 1):
            date = (p.get("date") or "")[:10]
            title = (p.get("title") or "")[:60]
            print(f"{i:<4} {date:<12} {title}")
            if p.get("subtitle"):
                print(f"{'':>17}{p['subtitle'][:60]}")

    # Print brain brief path hint
    if not args.no_store and args.output != "brain-brief":
        print(f"\n→ To synthesize into the PMM Brain, run:")
        print(f"  python3 -m src.ingestion.newsletter_scraper --url \"{args.url}\" --output brain-brief")
        print(f"  Then feed the output to the /ingest skill.")


if __name__ == "__main__":
    main()
