from __future__ import annotations

from pathlib import Path

import typer

from nexus.documents import create_document, list_documents
from nexus.entities import create_entity, list_entities, validate_required_text
from nexus.workspace import (
    SCHEMA_COMPATIBILITY_NOTE,
    WorkspaceBootstrapError,
    initialize_workspace,
    inspect_workspace,
)

app = typer.Typer(
    add_completion=False,
    help="Nexus local-first workspace CLI.",
    no_args_is_help=True,
)
entity_app = typer.Typer(help="Manage Nexus entities.")
document_app = typer.Typer(help="Manage Nexus documents.")


@app.callback()
def app_callback() -> None:
    """Nexus command group."""


app.add_typer(entity_app, name="entity")
app.add_typer(document_app, name="document")


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
    if result.schema_compatibility_applied:
        typer.echo(f"Schema note: {SCHEMA_COMPATIBILITY_NOTE}")

    if result.created_directories:
        typer.echo("Created directories:")
        for path in result.created_directories:
            typer.echo(f"  - {path}")

    if result.created_files:
        typer.echo("Created files:")
        for path in result.created_files:
            typer.echo(f"  - {path}")


@app.command("status")
def status_command() -> None:
    """Show minimal local workspace status for the current directory."""

    try:
        status = inspect_workspace(Path.cwd())
    except WorkspaceBootstrapError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    typer.echo("Nexus workspace status")
    typer.echo(f"Root: {status.workspace_root}")
    typer.echo(f"Initialized: {'yes' if status.is_workspace else 'no'}")
    typer.echo(
        f"Database: {status.database_path} "
        f"({'present' if status.database_path.exists() else 'missing'})"
    )
    typer.echo(
        f"Config: {status.config_path} "
        f"({'present' if status.config_path.exists() else 'missing'})"
    )
    typer.echo(
        f"Documents: {status.documents_dir} "
        f"({'present' if status.documents_dir.exists() else 'missing'})"
    )
    typer.echo(
        f"Backups: {status.backups_dir} "
        f"({'present' if status.backups_dir.exists() else 'missing'})"
    )
    typer.echo(f"Schema version: {status.schema_version or 'unknown'}")
    typer.echo(f"Workspace name: {status.workspace_name or 'unknown'}")
    typer.echo(f"Initialized at: {status.initialized_at or 'unknown'}")

    if status.missing_paths:
        typer.echo("Missing paths:")
        for path in status.missing_paths:
            typer.echo(f"  - {path}")

    if status.notes:
        typer.echo("Notes:")
        for note in status.notes:
            typer.echo(f"  - {note}")


@entity_app.command("create")
def entity_create_command(
    name: str = typer.Option(..., "--name", help="Entity name."),
    entity_type: str = typer.Option(..., "--type", help="Entity type, e.g. project or person."),
    context: str | None = typer.Option(None, "--context", help="Optional short context for the entity."),
) -> None:
    """Create a new entity in the current Nexus workspace."""

    try:
        record = create_entity(
            Path.cwd(),
            name=validate_required_text("Entity name", name),
            entity_type=validate_required_text("Entity type", entity_type),
            context=context,
        )
    except WorkspaceBootstrapError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    typer.echo(f"Entity created: {record.id}")
    typer.echo(f"Name: {record.name}")
    typer.echo(f"Type: {record.type}")
    if record.context:
        typer.echo(f"Context: {record.context}")


@entity_app.command("list")
def entity_list_command(
    entity_type: str | None = typer.Option(None, "--type", help="Filter entities by type."),
) -> None:
    """List entities in the current Nexus workspace."""

    try:
        records = list_entities(Path.cwd(), entity_type=entity_type)
    except WorkspaceBootstrapError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    if not records:
        typer.echo("No entities found.")
        return

    typer.echo("ID | Name | Type | Context")
    for record in records:
        typer.echo(
            f"{record.id} | {record.name} | {record.type} | {record.context or '-'}"
        )


@document_app.command("create")
def document_create_command(
    document_type: str = typer.Option(
        ...,
        "--type",
        help="Document type, e.g. daily, weekly, monthly, report or note.",
    ),
    title: str | None = typer.Option(
        None,
        "--title",
        help="Optional explicit document title. A default title is generated when omitted.",
    ),
    cycle_id: str | None = typer.Option(
        None,
        "--cycle-id",
        help="Optional cycle identifier to link the document to an existing cycle later.",
    ),
) -> None:
    """Create a new document in the current Nexus workspace."""

    try:
        record = create_document(
            Path.cwd(),
            document_type=document_type,
            title=title,
            cycle_id=cycle_id,
        )
    except WorkspaceBootstrapError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    typer.echo(f"Document created: {record.id}")
    typer.echo(f"Title: {record.title}")
    typer.echo(f"Type: {record.type}")
    typer.echo(f"Status: {record.status}")
    typer.echo(f"Path: {record.path}")


@document_app.command("list")
def document_list_command(
    document_type: str | None = typer.Option(None, "--type", help="Filter documents by type."),
    status: str | None = typer.Option(None, "--status", help="Filter documents by status."),
) -> None:
    """List documents in the current Nexus workspace."""

    try:
        records = list_documents(Path.cwd(), document_type=document_type, status=status)
    except WorkspaceBootstrapError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    if not records:
        typer.echo("No documents found.")
        return

    typer.echo("ID | Title | Type | Status | Path")
    for record in records:
        typer.echo(
            f"{record.id} | {record.title} | {record.type} | {record.status} | {record.path}"
        )


def main() -> None:
    app()
