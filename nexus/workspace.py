from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import duckdb

from nexus.workspace_contract import (
    DATABASE_FILENAME,
    WorkspaceLayout,
    workspace_layout,
)

SCHEMA_COMPATIBILITY_NOTE = (
    "Bootstrap compatibility applied for system_state.value: "
    "the schema declares NOT NULL but seeds last_backup/last_sync with NULL-like values."
)
SCHEMA_COMPATIBILITY_REPLACEMENTS = {
    "VALUES ('last_backup', NULL)": "VALUES ('last_backup', '')",
    "VALUES ('last_sync', NULL)": "VALUES ('last_sync', '')",
}


class WorkspaceBootstrapError(RuntimeError):
    """Raised when the local Nexus workspace cannot be initialized safely."""


@dataclass(frozen=True)
class WorkspaceInitResult:
    workspace_root: Path
    database_path: Path
    config_path: Path
    created_directories: tuple[Path, ...]
    created_files: tuple[Path, ...]
    schema_compatibility_applied: bool


@dataclass(frozen=True)
class WorkspaceStatus:
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
    resource_counts: "WorkspaceResourceCounts | None"
    activity_summary: "WorkspaceActivitySummary | None"


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
class SchemaBootstrapPayload:
    sql: str
    compatibility_applied: bool


def initialize_workspace(target: Path) -> WorkspaceInitResult:
    """Initialize a local Nexus workspace in the target directory."""

    layout = workspace_layout(target)
    created_directories: list[Path] = []
    created_files: list[Path] = []

    if layout.root.exists() and not layout.root.is_dir():
        raise WorkspaceBootstrapError(f"Target path is not a directory: {layout.root}")

    if not layout.root.exists():
        layout.root.mkdir(parents=True, exist_ok=True)
        created_directories.append(layout.root)

    for directory in layout.required_directories:
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
            created_directories.append(directory)

    database_existed = layout.database_path.exists()
    schema_payload = load_schema_sql()

    connection = connect_workspace_database(layout.database_path)
    try:
        execute_sql_script(connection, schema_payload.sql)
        ensure_workspace_system_state(connection, layout)
    finally:
        connection.close()

    if not database_existed and layout.database_path.exists():
        created_files.append(layout.database_path)

    if not layout.config_path.exists():
        layout.config_path.write_text(build_config_yaml(layout), encoding="utf-8")
        created_files.append(layout.config_path)

    return WorkspaceInitResult(
        workspace_root=layout.root,
        database_path=layout.database_path,
        config_path=layout.config_path,
        created_directories=tuple(created_directories),
        created_files=tuple(created_files),
        schema_compatibility_applied=schema_payload.compatibility_applied,
    )


def inspect_workspace(target: Path) -> WorkspaceStatus:
    layout = workspace_layout(target)
    missing_paths = [
        path
        for path in (
            layout.marker_dir,
            layout.config_path,
            layout.database_path,
            layout.documents_dir,
            layout.backups_dir,
            *layout.document_cycle_dirs,
        )
        if not path.exists()
    ]

    schema_version: str | None = None
    workspace_name: str | None = None
    initialized_at: str | None = None
    notes: list[str] = []
    resource_counts: WorkspaceResourceCounts | None = None
    activity_summary: WorkspaceActivitySummary | None = None

    if layout.database_path.exists():
        try:
            connection = connect_workspace_database(layout.database_path, read_only=True)
            try:
                schema_version = fetch_system_state_value(connection, "schema_version")
                resource_counts = fetch_workspace_resource_counts(connection)
                activity_summary = fetch_workspace_activity_summary(connection)
            finally:
                connection.close()
        except WorkspaceBootstrapError as exc:
            notes.append(str(exc))

    workspace_name = fetch_config_value(layout.config_path, "name")
    initialized_at = fetch_config_value(layout.config_path, "initialized_at")

    is_workspace = (
        layout.marker_dir.exists()
        and layout.config_path.exists()
        and layout.database_path.exists()
        and layout.documents_dir.exists()
    )
    if not is_workspace:
        notes.append("Current directory does not satisfy the minimal Nexus workspace contract.")

    return WorkspaceStatus(
        workspace_root=layout.root,
        is_workspace=is_workspace,
        marker_dir=layout.marker_dir,
        config_path=layout.config_path,
        database_path=layout.database_path,
        documents_dir=layout.documents_dir,
        backups_dir=layout.backups_dir,
        schema_version=schema_version,
        workspace_name=workspace_name,
        initialized_at=initialized_at,
        missing_paths=tuple(missing_paths),
        notes=tuple(notes),
        resource_counts=resource_counts,
        activity_summary=activity_summary,
    )


def require_workspace(target: Path) -> WorkspaceStatus:
    status = inspect_workspace(target)
    if not status.is_workspace:
        raise WorkspaceBootstrapError(
            f"Current directory is not a Nexus workspace: {status.workspace_root}. "
            "Run `nexus init` first."
        )
    return status


def load_schema_sql() -> SchemaBootstrapPayload:
    schema_path = Path(__file__).resolve().parents[1] / "Plan" / "NEXUS_MVP_SCHEMA.sql"
    if not schema_path.exists():
        raise WorkspaceBootstrapError(f"Schema file not found: {schema_path}")
    return normalize_schema_sql(schema_path.read_text(encoding="utf-8"))


def normalize_schema_sql(schema_sql: str) -> SchemaBootstrapPayload:
    """Apply a single conservative bootstrap compatibility layer for schema seed data."""

    normalized = schema_sql
    compatibility_applied = False
    for source, target in SCHEMA_COMPATIBILITY_REPLACEMENTS.items():
        if source in normalized:
            compatibility_applied = True
            normalized = normalized.replace(source, target)
    return SchemaBootstrapPayload(
        sql=normalized,
        compatibility_applied=compatibility_applied,
    )


def connect_workspace_database(
    database_path: Path, *, read_only: bool = False
) -> duckdb.DuckDBPyConnection:
    try:
        return duckdb.connect(str(database_path), read_only=read_only)
    except duckdb.Error as exc:
        mode = "read-only" if read_only else "read-write"
        raise WorkspaceBootstrapError(
            f"Failed to open DuckDB database in {mode} mode: {database_path}: {exc}"
        ) from exc


def execute_sql_script(connection: duckdb.DuckDBPyConnection, schema_sql: str) -> None:
    try:
        for statement in split_sql_statements(schema_sql):
            connection.execute(statement)
    except duckdb.Error as exc:
        raise WorkspaceBootstrapError(f"Failed to initialize DuckDB schema: {exc}") from exc


def split_sql_statements(schema_sql: str) -> list[str]:
    statements: list[str] = []
    current: list[str] = []
    in_single_quote = False
    in_line_comment = False

    for index, char in enumerate(schema_sql):
        next_char = schema_sql[index + 1] if index + 1 < len(schema_sql) else ""

        if in_line_comment:
            if char == "\n":
                in_line_comment = False
            continue

        if not in_single_quote and char == "-" and next_char == "-":
            in_line_comment = True
            continue

        if char == "'" and not in_line_comment:
            in_single_quote = not in_single_quote
            current.append(char)
            continue

        if char == ";" and not in_single_quote:
            statement = "".join(current).strip()
            if statement:
                statements.append(statement)
            current = []
            continue

        current.append(char)

    trailing_statement = "".join(current).strip()
    if trailing_statement:
        statements.append(trailing_statement)

    return statements


def ensure_workspace_system_state(
    connection: duckdb.DuckDBPyConnection, layout: WorkspaceLayout
) -> None:
    now = utc_now()
    values = {
        "workspace_root": str(layout.root),
        "workspace_config_path": str(layout.config_path.relative_to(layout.root)).replace(
            "\\", "/"
        ),
        "workspace_database_path": DATABASE_FILENAME,
    }

    for key, value in values.items():
        connection.execute(
            """
            INSERT OR REPLACE INTO system_state (key, value, last_updated)
            VALUES (?, ?, ?)
            """,
            [key, value, now],
        )


def build_config_yaml(layout: WorkspaceLayout) -> str:
    initialized_at = utc_now()
    lines = [
        "workspace: default",
        f"name: {layout.root.name}",
        f"database: {DATABASE_FILENAME}",
        f"documents_root: {layout.documents_dir.relative_to(layout.root).as_posix()}",
        f"backups_root: {layout.backups_dir.relative_to(layout.root).as_posix()}",
        f"initialized_at: {initialized_at}",
        "",
    ]
    return "\n".join(lines)


def fetch_system_state_value(
    connection: duckdb.DuckDBPyConnection, key: str
) -> str | None:
    row = connection.execute(
        "SELECT value FROM system_state WHERE key = ?",
        [key],
    ).fetchone()
    return None if row is None else row[0]


def fetch_workspace_resource_counts(
    connection: duckdb.DuckDBPyConnection,
) -> WorkspaceResourceCounts:
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


def fetch_workspace_activity_summary(
    connection: duckdb.DuckDBPyConnection,
) -> WorkspaceActivitySummary:
    statuses = fetch_status_counts(connection, "activities", "status")
    return WorkspaceActivitySummary(
        pending=statuses.get("pending", 0),
        in_progress=statuses.get("in_progress", 0),
        completed=statuses.get("completed", 0),
        blocked=statuses.get("blocked", 0),
    )


def fetch_table_count(connection: duckdb.DuckDBPyConnection, table: str) -> int:
    row = connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
    return 0 if row is None else int(row[0])


def fetch_status_counts(
    connection: duckdb.DuckDBPyConnection, table: str, column: str
) -> dict[str, int]:
    rows = connection.execute(
        f"""
        SELECT {column}, COUNT(*)
        FROM {table}
        GROUP BY {column}
        """
    ).fetchall()
    return {str(row[0]): int(row[1]) for row in rows if row[0] is not None}


def fetch_config_value(config_path: Path, key: str) -> str | None:
    if not config_path.exists():
        return None

    prefix = f"{key}:"
    for line in config_path.read_text(encoding="utf-8").splitlines():
        if line.startswith(prefix):
            return line.partition(":")[2].strip()
    return None


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )
