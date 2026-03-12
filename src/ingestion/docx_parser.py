"""Parse .docx files into individual posts.

Expects one .docx per source (user or writer).
Posts within a doc should be separated by:
  - Three or more dashes (---) or equals (===) on their own line
  - OR a page break
  - OR three or more blank lines
"""

import hashlib
import logging
import re
from datetime import datetime
from pathlib import Path

from docx import Document

from src.config.settings import settings
from src.schemas.engagement import PostRecord
from src.storage.database import get_session
from src.storage.models import PostTable
from src.storage import vectors

logger = logging.getLogger(__name__)

# Separators between posts within a single doc
POST_SEPARATOR = re.compile(r"\n\s*[-=]{3,}\s*\n|\n{3,}")


def extract_text_from_docx(file_path: Path) -> str:
    """Extract all text from a .docx file, preserving paragraph breaks."""
    doc = Document(str(file_path))
    paragraphs = []
    for para in doc.paragraphs:
        text = para.text.strip()
        paragraphs.append(text)
    return "\n".join(paragraphs)


def split_into_posts(full_text: str) -> list[str]:
    """Split a document's text into individual posts using separators."""
    posts = POST_SEPARATOR.split(full_text)
    # Filter out empty or very short fragments
    cleaned = []
    for post in posts:
        text = post.strip()
        if len(text) > 50:  # Minimum viable post length
            cleaned.append(text)
    return cleaned


def make_post_id(source: str, content: str) -> str:
    """Generate a deterministic ID for a post."""
    hash_input = f"{source}:{content[:200]}"
    return hashlib.sha256(hash_input.encode()).hexdigest()[:16]


def ingest_posts(source: str, posts_text: list[str]) -> list[PostRecord]:
    """Store posts in SQLite + ChromaDB and return PostRecords."""
    session = get_session()
    records = []
    vector_docs = []

    for text in posts_text:
        post_id = make_post_id(source, text)
        record = PostRecord(
            id=post_id,
            source=source,
            content=text,
            word_count=len(text.split()),
            ingested_at=datetime.now(),
        )
        records.append(record)

        # SQLite
        existing = session.query(PostTable).filter_by(id=post_id).first()
        if not existing:
            session.add(PostTable(
                id=post_id,
                source=source,
                content=text,
                word_count=record.word_count,
                ingested_at=record.ingested_at,
            ))

        # ChromaDB
        vector_docs.append({
            "id": post_id,
            "content": text,
            "metadata": {"source": source, "word_count": record.word_count},
        })

    session.commit()
    session.close()

    vectors.add_posts(vector_docs)
    logger.info(f"Ingested {len(records)} posts from '{source}'")
    return records


def parse_all_docs() -> dict[str, list[PostRecord]]:
    """Parse all .docx files from user/ and writers/ directories.

    Returns: dict mapping source name -> list of PostRecords.
    """
    posts_by_source: dict[str, list[PostRecord]] = {}

    # User's posts
    user_dir = settings.user_posts_dir
    for docx_file in user_dir.glob("*.docx"):
        logger.info(f"Parsing user doc: {docx_file.name}")
        full_text = extract_text_from_docx(docx_file)
        posts = split_into_posts(full_text)
        records = ingest_posts("user", posts)
        posts_by_source["user"] = records
        logger.info(f"  Found {len(records)} posts in {docx_file.name}")

    # Reference writers
    writers_dir = settings.writers_dir
    for docx_file in writers_dir.glob("*.docx"):
        writer_name = docx_file.stem.replace("_", " ").title()
        logger.info(f"Parsing writer doc: {docx_file.name} -> '{writer_name}'")
        full_text = extract_text_from_docx(docx_file)
        posts = split_into_posts(full_text)
        records = ingest_posts(writer_name, posts)
        posts_by_source[writer_name] = records
        logger.info(f"  Found {len(records)} posts for {writer_name}")

    return posts_by_source
