from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from nexus.entities import validate_required_text
from nexus.workspace import (
    WorkspaceBootstrapError,
    connect_workspace_database,
    require_workspace,
)

MAX_AUDIT_LOG_LIMIT = 200


@dataclass(frozen=True)
class AuditLogRecord:
    id: str
    action: str
    entity_type: str
    entity_id: str | None
    agent: str
    reason: str | None
    timestamp: str


def list_audit_log(workspace_root: Path, *, limit: int = 50) -> list[AuditLogRecord]:
    workspace = require_workspace(workspace_root)
    normalized_limit = validate_audit_limit(limit)

    with connect_workspace_database(workspace.database_path, read_only=True) as connection:
        rows = connection.execute(
            """
            SELECT
                id,
                action,
                entity_type,
                entity_id,
                agent,
                reason,
                timestamp
            FROM audit_log
            ORDER BY timestamp DESC, id DESC
            LIMIT ?
            """,
            [normalized_limit],
        ).fetchall()

    return [audit_log_record_from_row(row) for row in rows]


def validate_audit_limit(limit: int) -> int:
    try:
        normalized_limit = int(limit)
    except (TypeError, ValueError) as exc:
        raise WorkspaceBootstrapError(f"Audit limit must be an integer: {limit}") from exc

    if normalized_limit < 1 or normalized_limit > MAX_AUDIT_LOG_LIMIT:
        raise WorkspaceBootstrapError(
            f"Audit limit must be between 1 and {MAX_AUDIT_LOG_LIMIT}: {normalized_limit}"
        )

    return normalized_limit


def audit_log_record_from_row(row: Sequence[object]) -> AuditLogRecord:
    return AuditLogRecord(
        id=validate_required_text("Audit id", str(row[0])),
        action=validate_required_text("Audit action", str(row[1])),
        entity_type=validate_required_text("Audit entity type", str(row[2])),
        entity_id=None if row[3] is None else str(row[3]),
        agent=validate_required_text("Audit agent", str(row[4])),
        reason=None if row[5] is None else str(row[5]),
        timestamp=validate_required_text("Audit timestamp", str(row[6])),
    )
