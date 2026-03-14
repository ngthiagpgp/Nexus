from __future__ import annotations

from pathlib import Path

import typer

from nexus.workspace import WorkspaceBootstrapError, initialize_workspace

app = typer.Typer(
    add_completion=False,
    help="Nexus local-first workspace CLI.",
    no_args_is_help=True,
)


@app.callback()
def app_callback() -> None:
    """Nexus command group."""


@app.command("init")
def init_command(
    target: Path = typer.Argument(
        Path("."),
        dir_okay=True,
        file_okay=False,
        exists=False,
        resolve_path=True,
        help="Directory to initialize as a Nexus workspace. Defaults to the current directory.",
    ),
) -> None:
    """Bootstrap a local Nexus workspace."""

    try:
        result = initialize_workspace(target)
    except WorkspaceBootstrapError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    typer.echo(f"Nexus workspace ready: {result.workspace_root}")
    typer.echo(f"Database: {result.database_path}")
    typer.echo(f"Config: {result.config_path}")

    if result.created_directories:
        typer.echo("Created directories:")
        for path in result.created_directories:
            typer.echo(f"  - {path}")

    if result.created_files:
        typer.echo("Created files:")
        for path in result.created_files:
            typer.echo(f"  - {path}")


def main() -> None:
    app()
