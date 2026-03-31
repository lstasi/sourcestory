"""SourceStory CLI — entry point powered by Typer."""

from __future__ import annotations

from typing import Annotated

import typer
from rich.console import Console

from sourcestory import __version__

app = typer.Typer(
    name="sourcestory",
    help="Turning complex source code into engaging narratives.",
    add_completion=False,
)
console = Console()

# ── Formats & backends available ────────────────────────────────────────────

FORMATS = ("book_chapter", "podcast", "summary", "readme")
BACKENDS = ("ollama", "llamacpp", "hf")


def _version_callback(value: bool) -> None:
    if value:
        console.print(f"sourcestory {__version__}")
        raise typer.Exit


@app.callback()
def main(
    version: Annotated[
        bool | None,
        typer.Option(
            "--version",
            "-V",
            help="Show version and exit.",
            callback=_version_callback,
            is_eager=True,
        ),
    ] = None,
) -> None:
    """SourceStory — turning complex source code into engaging narratives."""


@app.command()
def generate(
    source: Annotated[
        str,
        typer.Argument(help="Path to a file, directory, or Git URL to analyse."),
    ],
    fmt: Annotated[
        str,
        typer.Option(
            "--format",
            "-f",
            help="Output narrative format.",
        ),
    ] = "book_chapter",
    model: Annotated[
        str,
        typer.Option("--model", "-m", help="LLM model name."),
    ] = "mistral",
    backend: Annotated[
        str,
        typer.Option("--backend", "-b", help="LLM backend to use."),
    ] = "ollama",
    output: Annotated[
        str | None,
        typer.Option("--output", "-o", help="Output file path (default: stdout)."),
    ] = None,
) -> None:
    """Generate a narrative from source code."""
    if fmt not in FORMATS:
        console.print(
            f"[red]Error:[/red] Unknown format '{fmt}'. Available: {', '.join(FORMATS)}"
        )
        raise typer.Exit(code=1)

    if backend not in BACKENDS:
        console.print(
            f"[red]Error:[/red] Unknown backend '{backend}'. "
            f"Available: {', '.join(BACKENDS)}"
        )
        raise typer.Exit(code=1)

    console.print(
        f"[bold green]sourcestory[/bold green] — generating "
        f"[cyan]{fmt}[/cyan] from [yellow]{source}[/yellow] "
        f"using [magenta]{model}[/magenta] ({backend})"
    )
    # TODO: Wire up ingestion → chunking → LLM → formatter pipeline.
    console.print(
        "[dim]Pipeline not yet implemented. See TODO.md for the roadmap.[/dim]"
    )


@app.command("list-formats")
def list_formats() -> None:
    """List available output narrative formats."""
    for f in FORMATS:
        console.print(f"  • {f}")


@app.command("list-backends")
def list_backends() -> None:
    """List available LLM backends."""
    for b in BACKENDS:
        console.print(f"  • {b}")
