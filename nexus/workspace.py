from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import duckdb

DEFAULT_DATABASE_NAME = "nexus.duckdb"
DEFAULT_CONFIG_PATH = Path(".nexus") / "config.yaml"
DEFAULT_DOCUMENT_DIRECTORIES = (
    Path("documents"),
    Path("documents") / "daily",
    Path("documents") / "weekly",
    Path("documents") / "monthly",
)
DEFAULT_INTERNAL_DIRECTORIES = (
    Path(".nexus"),
    Path(".nexus") / "backups",
)


class WorkspaceBootstrapError(RuntimeError):
    """Raised when the local Nexus workspace cannot be initialized safely."""


@dataclass(frozen=True)
class WorkspaceInitResult:
    workspace_root: Path
    database_path: Path
    config_path: Path
    created_directories: tuple[Path, ...]
    created_files: tuple[Path, ...]


def initialize_workspace(target: Path) -> WorkspaceInitResult:
    """Initialize a local Nexus workspace in the target directory."""

    workspace_root = target.expanduser().resolve()
    created_directories: list[Path] = []
    created_files: list[Path] = []

    if workspace_root.exists() and not workspace_root.is_dir():
        raise WorkspaceBootstrapError(
            f"Target path is not a directory: {workspace_root}"
        )

    if not workspace_root.exists():
        workspace_root.mkdir(parents=True, exist_ok=True)
        created_directories.append(workspace_root)

    for relative_path in (*DEFAULT_INTERNAL_DIRECTORIES, *DEFAULT_DOCUMENT_DIRECTORIES):
        directory = workspace_root / relative_path
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
            created_directories.append(directory)

    database_path = workspace_root / DEFAULT_DATABASE_NAME
    database_existed = database_path.exists()

    connection = duckdb.connect(str(database_path))
    try:
        schema_sql = load_schema_sql()
        execute_sql_script(connection, schema_sql)
        ensure_workspace_system_state(connection, workspace_root)
    except duckdb.Error as exc:
        raise WorkspaceBootstrapError(f"Failed to initialize DuckDB schema: {exc}") from exc
    finally:
        connection.close()

    if not database_existed and database_path.exists():
        created_files.append(database_path)

    config_path = workspace_root / DEFAULT_CONFIG_PATH
    if not config_path.exists():
        config_path.write_text(build_config_yaml(workspace_root), encoding="utf-8")
        created_files.append(config_path)

    return WorkspaceInitResult(
        workspace_root=workspace_root,
        database_path=database_path,
        config_path=config_path,
        created_directories=tuple(created_directories),
        created_files=tuple(created_files),
    )


def load_schema_sql() -> str:
    schema_path = Path(__file__).resolve().parents[1] / "Plan" / "NEXUS_MVP_SCHEMA.sql"
    if not schema_path.exists():
        raise WorkspaceBootstrapError(f"Schema file not found: {schema_path}")
    return normalize_schema_sql(schema_path.read_text(encoding="utf-8"))


def normalize_schema_sql(schema_sql: str) -> str:
    """Apply conservative compatibility fixes without rewriting the source spec."""

    replacements = {
        "VALUES ('last_backup', NULL)": "VALUES ('last_backup', '')",
        "VALUES ('last_sync', NULL)": "VALUES ('last_sync', '')",
    }
    normalized = schema_sql
    for source, target in replacements.items():
        normalized = normalized.replace(source, target)
    return normalized


def execute_sql_script(connection: duckdb.DuckDBPyConnection, schema_sql: str) -> None:
    for statement in split_sql_statements(schema_sql):
        connection.execute(statement)


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
    connection: duckdb.DuckDBPyConnection, workspace_root: Path
) -> None:
    now = utc_now()
    values = {
        "workspace_root": str(workspace_root),
        "workspace_config_path": str(DEFAULT_CONFIG_PATH).replace("\\", "/"),
        "workspace_database_path": DEFAULT_DATABASE_NAME,
    }

    for key, value in values.items():
        connection.execute(
            """
            INSERT OR REPLACE INTO system_state (key, value, last_updated)
            VALUES (?, ?, ?)
            """,
            [key, value, now],
        )


def build_config_yaml(workspace_root: Path) -> str:
    initialized_at = utc_now()
    lines = [
        "workspace: default",
        f"name: {workspace_root.name}",
        f"database: {DEFAULT_DATABASE_NAME}",
        "documents_root: documents",
        "backups_root: .nexus/backups",
        f"initialized_at: {initialized_at}",
        "",
    ]
    return "\n".join(lines)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )
