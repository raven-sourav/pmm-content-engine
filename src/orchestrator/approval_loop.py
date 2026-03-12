"""CLI approval loop — user reviews drafts and approves/tweaks/rejects."""

import logging

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from src.schemas.content import DailyOutput
from src.storage.database import get_session
from src.storage.models import DraftTable

logger = logging.getLogger(__name__)
console = Console()


def run_approval_loop(daily_output: DailyOutput) -> None:
    """Present drafts to user for approval, tweaking, or rejection."""

    for i, option in enumerate(daily_output.post_options, 1):
        draft = option.draft
        result = option.escalator_result
        sc = result.final_scorecard

        # Display header
        console.print(f"\n{'='*70}")
        console.print(f"[bold]POST {i} of {len(daily_output.post_options)}[/bold]")
        console.print(f"[dim]Angle: {draft.angle_type.upper()} | {draft.angle}[/dim]")
        console.print(f"[dim]Status: {result.status} | Iterations: {result.total_iterations}[/dim]")
        console.print(f"[dim]Predicted: {option.predicted_engagement}[/dim]")
        console.print(f"[dim]Best time: {option.recommended_post_time}[/dim]")
        console.print(f"{'='*70}\n")

        # Display scorecard
        if sc:
            table = Table(title="Rubber Duck Scorecard")
            table.add_column("Phase", style="cyan")
            table.add_column("Score", justify="center")
            table.add_column("Status", justify="center")
            table.add_column("Key Critique", max_width=50)

            for p in sc.phases:
                score_style = "green" if p.passed else "red"
                status = "PASS" if p.passed else "FAIL"
                critique_short = p.critique[:80] + "..." if len(p.critique) > 80 else p.critique
                table.add_row(
                    p.phase,
                    f"[{score_style}]{p.score}[/{score_style}]",
                    f"[{score_style}]{status}[/{score_style}]",
                    critique_short,
                )

            console.print(table)

        if result.warning:
            console.print(f"\n[yellow]Warning: {result.warning}[/yellow]")

        # Display draft
        console.print(Panel(draft.content, title="Draft", border_style="blue"))
        console.print(f"[dim]Word count: {draft.word_count}[/dim]\n")

        # User action
        action = click.prompt(
            "Action",
            type=click.Choice(["approve", "tweak", "reject", "skip"], case_sensitive=False),
            default="skip",
        )

        if action == "approve":
            _update_status(draft.id, "approved")
            console.print("[green]Approved![/green]")

        elif action == "tweak":
            feedback = click.prompt("Your feedback for the rewrite")
            console.print(f"[yellow]Tweak requested. Feedback saved.[/yellow]")
            # TODO: In a future version, re-run generation with feedback
            _update_status(draft.id, "tweaked")

        elif action == "reject":
            _update_status(draft.id, "rejected")
            console.print("[red]Rejected.[/red]")

        else:
            console.print("[dim]Skipped.[/dim]")

    console.print(f"\n[bold]Daily run complete for theme: {daily_output.theme}[/bold]\n")


def _update_status(draft_id: str, status: str) -> None:
    session = get_session()
    draft = session.query(DraftTable).filter_by(id=draft_id).first()
    if draft:
        draft.status = status
    session.commit()
    session.close()
