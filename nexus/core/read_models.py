from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from nexus.core.workspace import (
    WorkspaceBootstrapError,
    WorkspaceStatus,
    connect_workspace_database,
    inspect_workspace,
)


@dataclass(frozen=True)
class WorkspaceResourceCounts:
    entities: int
    documents: int
    draft_documents: int
    approved_documents: int
    archived_documents: int
    relations: int
    cycles: int
    active_cycles: int
    completed_cycles: int
    archived_cycles: int
    activities: int


@dataclass(frozen=True)
class WorkspaceActivitySummary:
    pending: int
    in_progress: int
    completed: int
    blocked: int


@dataclass(frozen=True)
class WorkspaceStatusReadModel:
    workspace_root: Path
    is_workspace: bool
    marker_dir: Path
    config_path: Path
    database_path: Path
    documents_dir: Path
    backups_dir: Path
    schema_version: str | None
    workspace_name: str | None
    initialized_at: str | None
    missing_paths: tuple[Path, ...]
    notes: tuple[str, ...]
    resource_counts: WorkspaceResourceCounts | None
    activity_summary: WorkspaceActivitySummary | None


def inspect_workspace_read_model(target: Path) -> WorkspaceStatusReadModel:
    status = inspect_workspace(target)
    resource_counts: WorkspaceResourceCounts | None = None
    activity_summary: WorkspaceActivitySummary | None = None
    notes = list(status.notes)

    if status.database_path.exists():
        try:
            connection = connect_workspace_database(status.database_path, read_only=True)
            try:
                resource_counts = fetch_workspace_resource_counts(connection)
                activity_summary = fetch_workspace_activity_summary(connection)
            finally:
                connection.close()
        except WorkspaceBootstrapError as exc:
            notes.append(str(exc))

    return WorkspaceStatusReadModel(
        workspace_root=status.workspace_root,
        is_workspace=status.is_workspace,
        marker_dir=status.marker_dir,
        config_path=status.config_path,
        database_path=status.database_path,
        documents_dir=status.documents_dir,
        backups_dir=status.backups_dir,
        schema_version=status.schema_version,
        workspace_name=status.workspace_name,
        initialized_at=status.initialized_at,
        missing_paths=status.missing_paths,
        notes=tuple(notes),
        resource_counts=resource_counts,
        activity_summary=activity_summary,
    )


def workspace_read_model_from_status(
    status: WorkspaceStatus,
) -> WorkspaceStatusReadModel:
    return inspect_workspace_read_model(status.workspace_root)


def fetch_workspace_resource_counts(connection) -> WorkspaceResourceCounts:
    counts = {
        "entities": fetch_table_count(connection, "entities"),
        "documents": fetch_table_count(connection, "documents"),
        "relations": fetch_table_count(connection, "relations"),
        "cycles": fetch_table_count(connection, "cycles"),
        "activities": fetch_table_count(connection, "activities"),
    }
    document_statuses = fetch_status_counts(connection, "documents", "status")
    cycle_statuses = fetch_status_counts(connection, "cycles", "status")
    return WorkspaceResourceCounts(
        entities=counts["entities"],
        documents=counts["documents"],
        draft_documents=document_statuses.get("draft", 0),
        approved_documents=document_statuses.get("approved", 0),
        archived_documents=document_statuses.get("archived", 0),
        relations=counts["relations"],
        cycles=counts["cycles"],
        active_cycles=cycle_statuses.get("active", 0),
        completed_cycles=cycle_statuses.get("completed", 0),
        archived_cycles=cycle_statuses.get("archived", 0),
        activities=counts["activities"],
    )


def fetch_workspace_activity_summary(connection) -> WorkspaceActivitySummary:
    statuses = fetch_status_counts(connection, "activities", "status")
    return WorkspaceActivitySummary(
        pending=statuses.get("pending", 0),
        in_progress=statuses.get("in_progress", 0),
        completed=statuses.get("completed", 0),
        blocked=statuses.get("blocked", 0),
    )


def fetch_table_count(connection, table: str) -> int:
    row = connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
    return 0 if row is None else int(row[0])


def fetch_status_counts(connection, table: str, column: str) -> dict[str, int]:
    rows = connection.execute(
        f"""
        SELECT {column}, COUNT(*)
        FROM {table}
        GROUP BY {column}
        """
    ).fetchall()
    return {str(row[0]): int(row[1]) for row in rows if row[0] is not None}
