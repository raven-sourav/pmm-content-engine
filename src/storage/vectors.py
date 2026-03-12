"""ChromaDB vector store setup and query helpers."""

import logging
from pathlib import Path

import chromadb

from src.config.settings import settings

logger = logging.getLogger(__name__)

_chroma_client = None


def get_chroma_client() -> chromadb.ClientAPI:
    global _chroma_client
    if _chroma_client is None:
        persist_dir = str(settings.chroma_path)
        Path(persist_dir).mkdir(parents=True, exist_ok=True)
        _chroma_client = chromadb.PersistentClient(path=persist_dir)
        logger.info(f"ChromaDB initialized at {persist_dir}")
    return _chroma_client


def get_posts_collection() -> chromadb.Collection:
    """Collection for all ingested posts (user + writers)."""
    client = get_chroma_client()
    return client.get_or_create_collection(
        name="posts",
        metadata={"description": "LinkedIn posts from user and reference writers"},
    )


def get_research_collection() -> chromadb.Collection:
    """Collection for research briefs and evidence anchors."""
    client = get_chroma_client()
    return client.get_or_create_collection(
        name="research",
        metadata={"description": "Research briefs and evidence anchors"},
    )


def add_posts(
    posts: list[dict],
    collection: chromadb.Collection | None = None,
) -> None:
    """Add posts to the vector store.

    Each post dict should have: id, content, metadata (source, post_date, etc.)
    """
    if not posts:
        return

    collection = collection or get_posts_collection()

    ids = [p["id"] for p in posts]
    documents = [p["content"] for p in posts]
    metadatas = [p.get("metadata", {}) for p in posts]

    collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
    logger.info(f"Upserted {len(posts)} posts to vector store.")


def query_posts(
    query_text: str,
    n_results: int = 10,
    source_filter: str | None = None,
    collection: chromadb.Collection | None = None,
) -> list[dict]:
    """Query posts by semantic similarity.

    Args:
        query_text: The search query.
        n_results: Max number of results.
        source_filter: Filter by source (e.g., "user" or a writer name).

    Returns:
        List of dicts with id, content, metadata, distance.
    """
    collection = collection or get_posts_collection()

    where = {"source": source_filter} if source_filter else None

    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        where=where,
    )

    output = []
    if results and results["ids"]:
        for i, doc_id in enumerate(results["ids"][0]):
            output.append({
                "id": doc_id,
                "content": results["documents"][0][i] if results["documents"] else "",
                "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                "distance": results["distances"][0][i] if results["distances"] else 0.0,
            })

    return output
