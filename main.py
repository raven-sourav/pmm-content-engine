"""CLI utilities for the LinkedIn Content Engine.

Note: Content generation, research, critique, and theme suggestions
are handled directly by Claude Code via skills/ — not via CLI commands.
This CLI provides standalone utility commands only.
"""

import logging

import click
from rich.console import Console
from rich.logging import RichHandler

console = Console()

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(console=console, rich_tracebacks=True)],
)
logger = logging.getLogger(__name__)


@click.group()
def cli():
    """LinkedIn Content Engine -- Utility commands."""
    pass


@cli.command(name="init-db")
def init_db_cmd():
    """Initialize SQLite + ChromaDB storage."""
    from src.storage.database import init_db

    init_db()
    console.print("[green]Database initialized.[/green]")


@cli.command(name="parse-docs")
def parse_docs():
    """Parse all .docx files in data/user/ and data/writers/."""
    from src.ingestion.docx_parser import parse_all_docs

    posts_by_source = parse_all_docs()
    total = sum(len(p) for p in posts_by_source.values())
    console.print(f"Parsed [green]{total}[/green] posts from [green]{len(posts_by_source)}[/green] sources.")
    for source, posts in posts_by_source.items():
        console.print(f"  {source}: {len(posts)} posts")


@cli.command(name="scrape-urls")
def scrape_urls_cmd():
    """Scrape URLs listed in data/writers/urls.txt."""
    from src.ingestion.url_scraper import scrape_urls

    results = scrape_urls()
    total = sum(len(p) for p in results.values())
    console.print(f"Scraped [green]{total}[/green] articles from [green]{len(results)}[/green] sources.")


@cli.command(name="show-brain")
def show_brain():
    """Display a summary of the current PMM Brain."""
    from src.brain.brain_store import get_brain

    brain = get_brain()
    console.print(f"\n[bold]PMM Brain v{brain.version}[/bold] (updated: {brain.last_updated})")
    console.print(f"  Mental models: {len(brain.synthesized_mental_models)}")
    console.print(f"  Argumentation plays: {len(brain.argumentation_playbook)}")
    console.print(f"  Authority toolkit: {len(brain.authority_toolkit)}")
    console.print(f"  Insight patterns: {len(brain.insight_generation_patterns)}")
    console.print(f"  Quality bar examples: {len(brain.quality_bar_examples)}")
    console.print(f"  Writer DNA profiles: {len(brain.writer_dna_profiles)}")
    if brain.newsletter_insights:
        console.print(f"  Newsletter insights: {len(brain.newsletter_insights)}")


if __name__ == "__main__":
    cli()
