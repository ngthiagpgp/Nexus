from __future__ import annotations

from pathlib import Path
from typing import Callable, TypeVar

import typer

from nexus.activities import create_activity, list_activities, update_activity_status
from nexus.audit import list_audit_log
from nexus.core.read_models import inspect_workspace_read_model
from nexus.core.workspace import (
    SCHEMA_COMPATIBILITY_NOTE,
    WorkspaceBootstrapError,
    initialize_workspace,
)
from nexus.cycles import create_cycle, list_cycles
from nexus.demo_seed import seed_demo_workspace
from nexus.demo_seed_rich import seed_rich_demo_workspace
from nexus.documents import (
    create_document,
    inspect_document,
    list_documents,
    reconcile_document,
    update_document_status,
    verify_document,
    verify_documents,
)
from nexus.entities import create_entity, list_entities, validate_required_text
from nexus.relations import create_relation, list_relations, relation_display_map

app = typer.Typer(
    add_completion=False,
    help="Nexus local-first workspace CLI.",
    no_args_is_help=True,
)
entity_app = typer.Typer(help="Manage Nexus entities.")
document_app = typer.Typer(help="Manage Nexus documents.")
relation_app = typer.Typer(help="Manage Nexus relations.")
activity_app = typer.Typer(help="Manage Nexus activities.")
cycle_app = typer.Typer(help="Manage Nexus cycles.")
T = TypeVar("T")


@app.callback()
def app_callback() -> None:
    """Nexus command group."""


app.add_typer(entity_app, name="entity")
app.add_typer(document_app, name="document")
app.add_typer(relation_app, name="relation")
app.add_typer(activity_app, name="activity")
app.add_typer(cycle_app, name="cycle")


def _run_or_exit(operation: Callable[[], T]) -> T:
    try:
        return operation()
    except WorkspaceBootstrapError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1) from exc


def _print_table(headers: list[str], rows: list[list[str]]) -> None:
    header_line = " | ".join(headers)
    typer.echo(header_line)
    typer.echo("-" * len(header_line))
    for row in rows:
        typer.echo(" | ".join(row))


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

    result = _run_or_exit(lambda: initialize_workspace(target))

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
    """Show a compact operational status for the current directory."""

    status = _run_or_exit(lambda: inspect_workspace_read_model(Path.cwd()))

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

    if status.resource_counts:
        typer.echo("Resources:")
        typer.echo(f"  Entities: {status.resource_counts.entities}")
        typer.echo(
            "  Documents: "
            f"{status.resource_counts.documents} "
            f"(draft {status.resource_counts.draft_documents}, "
            f"approved {status.resource_counts.approved_documents}, "
            f"archived {status.resource_counts.archived_documents})"
        )
        typer.echo(f"  Relations: {status.resource_counts.relations}")
        typer.echo(
            "  Cycles: "
            f"{status.resource_counts.cycles} "
            f"(active {status.resource_counts.active_cycles}, "
            f"completed {status.resource_counts.completed_cycles}, "
            f"archived {status.resource_counts.archived_cycles})"
        )
        typer.echo(f"  Activities: {status.resource_counts.activities}")

    if status.activity_summary and status.resource_counts:
        typer.echo("Operational summary:")
        typer.echo(
            "  Open activities: "
            f"{status.activity_summary.pending + status.activity_summary.in_progress}"
        )
        typer.echo(
            "  Activity statuses: "
            f"pending {status.activity_summary.pending}, "
            f"in_progress {status.activity_summary.in_progress}, "
            f"completed {status.activity_summary.completed}, "
            f"blocked {status.activity_summary.blocked}"
        )
        typer.echo(f"  Active cycles: {status.resource_counts.active_cycles}")

    if status.missing_paths:
        typer.echo("Missing paths:")
        for path in status.missing_paths:
            typer.echo(f"  - {path}")

    if status.notes:
        typer.echo("Notes:")
        for note in status.notes:
            typer.echo(f"  - {note}")


@app.command("serve")
def serve_command(
    host: str = typer.Option("127.0.0.1", "--host", help="Host interface for the local Nexus API."),
    port: int = typer.Option(3000, "--port", min=1, max=65535, help="Port for the local Nexus API."),
) -> None:
    """Serve the local Nexus API and cockpit for the current workspace."""
    from nexus.adapters.api.api import create_app
    import uvicorn

    workspace_status = _run_or_exit(lambda: inspect_workspace_read_model(Path.cwd()))
    if not workspace_status.is_workspace:
        typer.echo(
            f"Error: Current directory is not a Nexus workspace: {workspace_status.workspace_root}. Run `nexus init` first.",
            err=True,
        )
        raise typer.Exit(code=1)

    typer.echo(f"Nexus serve: {workspace_status.workspace_root}")
    typer.echo(f"API: http://{host}:{port}/api/health")
    typer.echo(f"Cockpit: http://{host}:{port}/")
    uvicorn.run(create_app(workspace_root=workspace_status.workspace_root), host=host, port=port)


@app.command("demo-seed")
def demo_seed_command() -> None:
    """Create a small coherent demo dataset in the current Nexus workspace."""

    result = _run_or_exit(lambda: seed_demo_workspace(Path.cwd()))

    if result.created:
        typer.echo(f"Demo seed ready: {result.workspace_root}")
    else:
        typer.echo(f"Demo seed already present: {result.workspace_root}")
    typer.echo(
        "Counts: "
        f"cycles {result.cycle_count}, "
        f"activities {result.activity_count}, "
        f"entities {result.entity_count}, "
        f"documents {result.document_count}, "
        f"relations {result.relation_count}"
    )


@app.command("demo-seed-rich")
def demo_seed_rich_command() -> None:
    """Create a richer demonstration dataset in the current Nexus workspace."""

    result = _run_or_exit(lambda: seed_rich_demo_workspace(Path.cwd()))

    if result.created:
        typer.echo(f"Rich demo seed ready: {result.workspace_root}")
    else:
        typer.echo(f"Rich demo seed already present: {result.workspace_root}")
    typer.echo(
        "Counts: "
        f"cycles {result.cycle_count}, "
        f"activities {result.activity_count}, "
        f"entities {result.entity_count}, "
        f"documents {result.document_count}, "
        f"relations {result.relation_count}"
    )


@app.command("audit")
def audit_command(
    limit: int = typer.Option(
        20,
        "--limit",
        min=1,
        help="How many audit rows to show. Max 200.",
    ),
) -> None:
    """Show recent audit_log entries for the current Nexus workspace."""

    records = _run_or_exit(lambda: list_audit_log(Path.cwd(), limit=limit))

    if not records:
        typer.echo("No audit entries found.")
        return

    _print_table(
        ["Timestamp", "Action", "Entity Type", "Entity ID", "Agent"],
        [
            [
                record.timestamp,
                record.action,
                record.entity_type,
                record.entity_id or "-",
                record.agent,
            ]
            for record in records
        ],
    )


@entity_app.command("create")
def entity_create_command(
    name: str = typer.Option(..., "--name", help="Entity name."),
    entity_type: str = typer.Option(..., "--type", help="Entity type, e.g. project or person."),
    context: str | None = typer.Option(None, "--context", help="Optional short context for the entity."),
) -> None:
    """Create a new entity in the current Nexus workspace."""

    record = _run_or_exit(
        lambda: create_entity(
            Path.cwd(),
            name=validate_required_text("Entity name", name),
            entity_type=validate_required_text("Entity type", entity_type),
            context=context,
        )
    )

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

    records = _run_or_exit(lambda: list_entities(Path.cwd(), entity_type=entity_type))

    if not records:
        typer.echo("No entities found.")
        return

    _print_table(
        ["ID", "Name", "Type", "Context"],
        [
            [record.id, record.name, record.type, record.context or "-"]
            for record in records
        ],
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

    record = _run_or_exit(
        lambda: create_document(
            Path.cwd(),
            document_type=document_type,
            title=title,
            cycle_id=cycle_id,
        )
    )

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

    records = _run_or_exit(
        lambda: list_documents(Path.cwd(), document_type=document_type, status=status)
    )

    if not records:
        typer.echo("No documents found.")
        return

    _print_table(
        ["ID", "Title", "Type", "Status", "Path"],
        [
            [record.id, record.title, record.type, record.status, record.path]
            for record in records
        ],
    )


@document_app.command("show")
def document_show_command(
    selector: str = typer.Argument(
        ...,
        help="Document id or exact title.",
    ),
) -> None:
    """Inspect one document from DB metadata plus the backing Markdown file."""

    inspection = _run_or_exit(lambda: inspect_document(Path.cwd(), selector=selector))

    typer.echo(f"Document: {inspection.record.title}")
    typer.echo(f"ID: {inspection.record.id}")
    typer.echo(f"Type: {inspection.record.type}")
    typer.echo(f"Status: {inspection.record.status}")
    typer.echo(f"Cycle: {inspection.record.cycle_id or '-'}")
    typer.echo(f"Path: {inspection.record.path}")
    typer.echo(f"Backing file: {inspection.absolute_path}")
    typer.echo(f"Version: {inspection.record.version}")
    typer.echo(f"Created: {inspection.record.created_at}")
    typer.echo(f"Modified: {inspection.modified_at}")
    if inspection.approved_at:
        typer.echo(f"Approved: {inspection.approved_at}")
    typer.echo("Preview:")
    typer.echo(inspection.content_preview)


@document_app.command("set-status")
def document_set_status_command(
    selector: str = typer.Argument(
        ...,
        help="Document id or exact title.",
    ),
    status: str = typer.Option(
        ...,
        "--status",
        help="Target status: approved or archived, depending on current state.",
    ),
) -> None:
    """Update only the lifecycle status of one document in the current Nexus workspace."""

    record = _run_or_exit(
        lambda: update_document_status(
            Path.cwd(),
            selector=selector,
            status=status,
            actor="user",
            reason="CLI document status update",
            cli_id="local",
            allow_title_lookup=True,
        )
    )

    typer.echo(f"Document status updated: {record.id}")
    typer.echo(f"Title: {record.title}")
    typer.echo(f"Status: {record.status}")
    typer.echo(f"Version: {record.version}")
    if record.approved_at:
        typer.echo(f"Approved: {record.approved_at}")


@document_app.command("verify")
def document_verify_command(
    selector: str | None = typer.Argument(
        None,
        help="Document id or exact title.",
    ),
    verify_all: bool = typer.Option(
        False,
        "--all",
        help="Verify all document records in the current workspace.",
    ),
) -> None:
    """Verify document integrity against the current workspace filesystem."""

    if verify_all:
        if selector is not None:
            typer.echo("Error: Provide either a document selector or --all, not both.", err=True)
            raise typer.Exit(code=1)
        results = _run_or_exit(lambda: verify_documents(Path.cwd()))
        if not results:
            typer.echo("No documents found.")
            return
        _print_table(
            ["ID", "Title", "Status", "Integrity", "File", "Hash", "Issues"],
            [
                [
                    result.document_id,
                    result.title,
                    result.status,
                    result.integrity_state,
                    "present" if result.backing_file_exists else "missing",
                    (
                        "match"
                        if result.content_hash_matches is True
                        else "mismatch"
                        if result.content_hash_matches is False
                        else "n/a"
                    ),
                    ", ".join(result.issues) or "-",
                ]
                for result in results
            ],
        )
        return

    if selector is None:
        typer.echo("Error: Provide a document selector or use --all.", err=True)
        raise typer.Exit(code=1)

    result = _run_or_exit(
        lambda: verify_document(
            Path.cwd(),
            selector=selector,
            allow_title_lookup=True,
        )
    )

    typer.echo(f"Document integrity: {result.title}")
    typer.echo(f"ID: {result.document_id}")
    typer.echo(f"Status: {result.status}")
    typer.echo(f"Integrity: {result.integrity_state}")
    typer.echo(f"Path: {result.path}")
    typer.echo(f"Expected path: {result.expected_path}")
    typer.echo(
        f"Backing file: {result.absolute_path} "
        f"({'present' if result.backing_file_exists else 'missing'})"
    )
    hash_status = (
        "match"
        if result.content_hash_matches is True
        else "mismatch"
        if result.content_hash_matches is False
        else "not available"
    )
    typer.echo(f"Content hash: {hash_status}")
    typer.echo(f"Issues: {', '.join(result.issues) or 'none'}")


@document_app.command("reconcile")
def document_reconcile_command(
    selector: str = typer.Argument(
        ...,
        help="Document id or exact title.",
    ),
) -> None:
    """Reconcile safe document metadata drift against the current backing Markdown file."""

    result = _run_or_exit(
        lambda: reconcile_document(
            Path.cwd(),
            selector=selector,
            actor="user",
            reason="CLI document reconcile",
            cli_id="local",
            allow_title_lookup=True,
        )
    )

    if result.reconciled_fields:
        typer.echo(f"Document reconciled: {result.record.id}")
        typer.echo(f"Title: {result.record.title}")
        typer.echo(f"Reconciled fields: {', '.join(result.reconciled_fields)}")
    else:
        typer.echo(f"Document already aligned: {result.record.id}")
        typer.echo(f"Title: {result.record.title}")
    typer.echo(f"Integrity: {result.integrity.integrity_state}")
    typer.echo(f"Issues: {', '.join(result.integrity.issues) or 'none'}")


@relation_app.command("create")
def relation_create_command(
    from_entity: str = typer.Option(
        ...,
        "--from",
        help="Source entity id or exact name.",
    ),
    to_entity: str = typer.Option(
        ...,
        "--to",
        help="Target entity id or exact name.",
    ),
    relation_type: str = typer.Option(
        ...,
        "--type",
        help="Relation type, e.g. depende_de.",
    ),
    context: str | None = typer.Option(
        None,
        "--context",
        help="Optional short context for the relation.",
    ),
) -> None:
    """Create a new relation in the current Nexus workspace."""

    record = _run_or_exit(
        lambda: create_relation(
            Path.cwd(),
            from_entity=from_entity,
            to_entity=to_entity,
            relation_type=relation_type,
            context=context,
        )
    )

    typer.echo(f"Relation created: {record.id}")
    typer.echo(f"From: {record.entity_a_id}")
    typer.echo(f"To: {record.entity_b_id}")
    typer.echo(f"Type: {record.relation_type}")
    typer.echo(f"Weight: {record.weight:.1f}")
    if record.context:
        typer.echo(f"Context: {record.context}")


@relation_app.command("list")
def relation_list_command(
    from_entity: str | None = typer.Option(
        None,
        "--from",
        help="Filter by source entity id or exact name.",
    ),
    relation_type: str | None = typer.Option(
        None,
        "--type",
        help="Filter by relation type.",
    ),
) -> None:
    """List relations in the current Nexus workspace."""

    records = _run_or_exit(
        lambda: list_relations(
            Path.cwd(),
            from_entity=from_entity,
            relation_type=relation_type,
        )
    )

    if not records:
        typer.echo("No relations found.")
        return

    display_names = _run_or_exit(lambda: relation_display_map(Path.cwd()))
    _print_table(
        ["ID", "From", "To", "Type", "Weight", "Context"],
        [
            [
                record.id,
                display_names.get(record.entity_a_id, record.entity_a_id),
                display_names.get(record.entity_b_id, record.entity_b_id),
                record.relation_type,
                f"{record.weight:.1f}",
                record.context or "-",
            ]
            for record in records
        ],
    )


@activity_app.command("create")
def activity_create_command(
    title: str = typer.Option(..., "--title", help="Activity title."),
    cycle_id: str = typer.Option(
        ...,
        "--cycle-id",
        help="Existing cycle identifier for this activity.",
    ),
) -> None:
    """Create a new activity in the current Nexus workspace."""

    record = _run_or_exit(
        lambda: create_activity(
            Path.cwd(),
            title=title,
            cycle_id=cycle_id,
        )
    )

    typer.echo(f"Activity created: {record.id}")
    typer.echo(f"Title: {record.title}")
    typer.echo(f"Cycle: {record.cycle_id}")
    typer.echo(f"Status: {record.status}")
    typer.echo(f"Priority: {record.priority}")


@activity_app.command("list")
def activity_list_command(
    cycle_id: str | None = typer.Option(
        None,
        "--cycle-id",
        help="Filter activities by cycle id.",
    ),
    status: str | None = typer.Option(
        None,
        "--status",
        help="Filter activities by status.",
    ),
) -> None:
    """List activities in the current Nexus workspace."""

    records = _run_or_exit(
        lambda: list_activities(Path.cwd(), cycle_id=cycle_id, status=status)
    )

    if not records:
        typer.echo("No activities found.")
        return

    _print_table(
        ["ID", "Title", "Cycle", "Cycle Type", "Cycle Start", "Status", "Priority"],
        [
            [
                record.id,
                record.title,
                record.cycle_id,
                record.cycle_type or "-",
                record.cycle_start_date or "-",
                record.status,
                str(record.priority),
            ]
            for record in records
        ],
    )


@activity_app.command("set-status")
def activity_set_status_command(
    activity_id: str = typer.Argument(..., help="Activity identifier."),
    status: str = typer.Option(
        ...,
        "--status",
        help="Target status: pending, in_progress, completed, or blocked.",
    ),
) -> None:
    """Update only the status of one activity in the current Nexus workspace."""

    record = _run_or_exit(
        lambda: update_activity_status(
            Path.cwd(),
            activity_id=activity_id,
            status=status,
            actor="user",
            reason="CLI activity status update",
            cli_id="local",
        )
    )

    typer.echo(f"Activity status updated: {record.id}")
    typer.echo(f"Title: {record.title}")
    typer.echo(f"Cycle: {record.cycle_id}")
    typer.echo(f"Status: {record.status}")


@cycle_app.command("create")
def cycle_create_command(
    cycle_type: str = typer.Option(..., "--type", help="Cycle type, e.g. daily or weekly."),
    start: str = typer.Option(
        ...,
        "--start",
        help="Cycle start as ISO date or datetime.",
    ),
    end: str | None = typer.Option(
        None,
        "--end",
        help="Optional cycle end as ISO date or datetime.",
    ),
) -> None:
    """Create a new cycle in the current Nexus workspace."""

    record = _run_or_exit(
        lambda: create_cycle(
            Path.cwd(),
            cycle_type=cycle_type,
            start=start,
            end=end,
        )
    )

    typer.echo(f"Cycle created: {record.id}")
    typer.echo(f"Type: {record.type}")
    typer.echo(f"Start: {record.start_date}")
    typer.echo(f"Status: {record.status}")
    if record.end_date:
        typer.echo(f"End: {record.end_date}")


@cycle_app.command("list")
def cycle_list_command(
    cycle_type: str | None = typer.Option(None, "--type", help="Filter cycles by type."),
    status: str | None = typer.Option(None, "--status", help="Filter cycles by status."),
) -> None:
    """List cycles in the current Nexus workspace."""

    records = _run_or_exit(
        lambda: list_cycles(Path.cwd(), cycle_type=cycle_type, status=status)
    )

    if not records:
        typer.echo("No cycles found.")
        return

    _print_table(
        [
            "ID",
            "Type",
            "Start",
            "Status",
            "Activities",
            "Pending",
            "In Progress",
            "Completed",
            "Blocked",
        ],
        [
            [
                record.id,
                record.type,
                record.start_date,
                record.status,
                str(record.activity_count),
                str(record.pending_count),
                str(record.in_progress_count),
                str(record.completed_count),
                str(record.blocked_count),
            ]
            for record in records
        ],
    )


def main() -> None:
    app()
