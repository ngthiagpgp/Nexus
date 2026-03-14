from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from nexus.entities import validate_required_text
from nexus.workspace import (
    WorkspaceBootstrapError,
    connect_workspace_database,
    fetch_system_state_value,
    require_workspace,
    utc_now,
)

ALLOWED_ACTIVITY_STATUSES = ("pending", "in_progress", "completed", "blocked")
ALLOWED_ACTIVITY_STATUS_TRANSITIONS = {
    "pending": {"in_progress", "completed", "blocked"},
    "in_progress": {"pending", "completed", "blocked"},
    "completed": {"pending", "in_progress"},
    "blocked": {"pending", "in_progress", "completed"},
}


@dataclass(frozen=True)
class ActivityRecord:
    id: str
    title: str
    cycle_id: str
    cycle_type: str | None
    cycle_start_date: str | None
    status: str
    priority: int
    activity_type: str | None
    description: str | None
    created_at: str
    created_by: str


def create_activity(workspace_root: Path, *, title: str, cycle_id: str) -> ActivityRecord:
    workspace = require_workspace(workspace_root)
    normalized_title = validate_required_text("Activity title", title)
    normalized_cycle_id = validate_required_text("Cycle id", cycle_id)
    timestamp = utc_now()
    activity_id = str(uuid4())
    actor = "user"
    cli_id = "local"
    workspace_id = "default"

    with connect_workspace_database(workspace.database_path) as connection:
        workspace_id = fetch_system_state_value(connection, "default_workspace") or "default"
        cycle_type, cycle_start_date = fetch_cycle_details(connection, normalized_cycle_id)

        connection.execute(
            """
            INSERT INTO activities (
                id,
                title,
                cycle_id,
                status,
                priority,
                type,
                description,
                created_by,
                created_at,
                modified_by,
                modified_at,
                id_workspace,
                id_cli
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                activity_id,
                normalized_title,
                normalized_cycle_id,
                "pending",
                3,
                None,
                None,
                actor,
                timestamp,
                actor,
                timestamp,
                workspace_id,
                cli_id,
            ],
        )

        new_state = {
            "id": activity_id,
            "title": normalized_title,
            "cycle_id": normalized_cycle_id,
            "status": "pending",
            "priority": 3,
            "type": None,
            "description": None,
            "created_by": actor,
            "created_at": timestamp,
            "modified_by": actor,
            "modified_at": timestamp,
            "id_workspace": workspace_id,
            "id_cli": cli_id,
        }
        connection.execute(
            """
            INSERT INTO audit_log (
                id,
                action,
                entity_type,
                entity_id,
                old_state,
                new_state,
                agent,
                reason,
                timestamp,
                id_workspace,
                id_cli
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                str(uuid4()),
                "create",
                "activity",
                activity_id,
                None,
                json.dumps(new_state, ensure_ascii=True),
                actor,
                "CLI activity create",
                timestamp,
                workspace_id,
                cli_id,
            ],
        )

    return ActivityRecord(
        id=activity_id,
        title=normalized_title,
        cycle_id=normalized_cycle_id,
        cycle_type=cycle_type,
        cycle_start_date=cycle_start_date,
        status="pending",
        priority=3,
        activity_type=None,
        description=None,
        created_at=timestamp,
        created_by=actor,
    )


def list_activities(
    workspace_root: Path,
    *,
    cycle_id: str | None = None,
    status: str | None = None,
) -> list[ActivityRecord]:
    workspace = require_workspace(workspace_root)
    rows = fetch_activity_rows(
        workspace.database_path,
        cycle_id=cycle_id,
        status=status,
    )
    return [activity_record_from_row(row) for row in rows]


def get_activity(workspace_root: Path, *, activity_id: str) -> ActivityRecord:
    workspace = require_workspace(workspace_root)
    normalized_activity_id = validate_required_text("Activity id", activity_id)
    with connect_workspace_database(workspace.database_path, read_only=True) as connection:
        row = fetch_activity_row(connection, normalized_activity_id)
    return activity_record_from_row(row)


def update_activity_status(
    workspace_root: Path,
    *,
    activity_id: str,
    status: str,
    actor: str = "user",
    reason: str = "Activity status update",
    cli_id: str = "local",
) -> ActivityRecord:
    workspace = require_workspace(workspace_root)
    normalized_activity_id = validate_required_text("Activity id", activity_id)
    normalized_status = validate_activity_status(status)
    normalized_actor = validate_required_text("Actor", actor)
    normalized_reason = validate_required_text("Reason", reason)
    timestamp = utc_now()

    with connect_workspace_database(workspace.database_path) as connection:
        workspace_id = fetch_system_state_value(connection, "default_workspace") or "default"
        old_row = fetch_activity_row(connection, normalized_activity_id)
        old_record = activity_record_from_row(old_row)

        if old_record.status == normalized_status:
            return old_record

        allowed_statuses = ALLOWED_ACTIVITY_STATUS_TRANSITIONS.get(old_record.status, set())
        if normalized_status not in allowed_statuses:
            allowed_display = ", ".join(sorted(allowed_statuses))
            raise WorkspaceBootstrapError(
                "Invalid activity status transition: "
                f"{old_record.status} -> {normalized_status}. "
                f"Allowed: {allowed_display}."
            )

        connection.execute(
            """
            UPDATE activities
            SET status = ?, modified_by = ?, modified_at = ?, id_cli = ?
            WHERE id = ?
            """,
            [
                normalized_status,
                normalized_actor,
                timestamp,
                cli_id,
                normalized_activity_id,
            ],
        )

        new_row = fetch_activity_row(connection, normalized_activity_id)
        new_record = activity_record_from_row(new_row)

        connection.execute(
            """
            INSERT INTO audit_log (
                id,
                action,
                entity_type,
                entity_id,
                old_state,
                new_state,
                agent,
                reason,
                timestamp,
                id_workspace,
                id_cli
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                str(uuid4()),
                "update",
                "activity",
                normalized_activity_id,
                json.dumps(activity_state_payload(old_record), ensure_ascii=True),
                json.dumps(activity_state_payload(new_record), ensure_ascii=True),
                normalized_actor,
                normalized_reason,
                timestamp,
                workspace_id,
                cli_id,
            ],
        )

    return new_record


def fetch_activity_rows(
    database_path: Path,
    *,
    cycle_id: str | None = None,
    status: str | None = None,
    activity_id: str | None = None,
) -> list[Sequence[object]]:
    query = """
        SELECT
            a.id,
            a.title,
            a.cycle_id,
            c.type,
            c.start_date,
            a.status,
            a.priority,
            a.type,
            a.description,
            a.created_at,
            a.created_by
        FROM activities a
        JOIN cycles c ON c.id = a.cycle_id
    """
    clauses: list[str] = []
    params: list[str] = []

    if activity_id:
        clauses.append("a.id = ?")
        params.append(validate_required_text("Activity id", activity_id))

    if cycle_id:
        clauses.append("a.cycle_id = ?")
        params.append(validate_required_text("Cycle id", cycle_id))

    if status:
        clauses.append("a.status = ?")
        params.append(validate_required_text("Activity status", status))

    if clauses:
        query += " WHERE " + " AND ".join(clauses)

    query += " ORDER BY c.start_date DESC, a.priority ASC, a.created_at DESC, a.title ASC"

    with connect_workspace_database(database_path, read_only=True) as connection:
        return connection.execute(query, params).fetchall()


def fetch_activity_row(connection, activity_id: str) -> Sequence[object]:
    row = connection.execute(
        """
        SELECT
            a.id,
            a.title,
            a.cycle_id,
            c.type,
            c.start_date,
            a.status,
            a.priority,
            a.type,
            a.description,
            a.created_at,
            a.created_by
        FROM activities a
        JOIN cycles c ON c.id = a.cycle_id
        WHERE a.id = ?
        """,
        [activity_id],
    ).fetchone()
    if row is None:
        raise WorkspaceBootstrapError(f"Activity not found: {activity_id}")
    return row


def fetch_cycle_details(connection, cycle_id: str) -> tuple[str, str]:
    row = connection.execute(
        "SELECT type, start_date FROM cycles WHERE id = ?",
        [cycle_id],
    ).fetchone()
    if row is None:
        raise WorkspaceBootstrapError(f"Cycle not found: {cycle_id}")
    return row[0], str(row[1])


def activity_record_from_row(row: Sequence[object]) -> ActivityRecord:
    return ActivityRecord(
        id=str(row[0]),
        title=str(row[1]),
        cycle_id=str(row[2]),
        cycle_type=None if row[3] is None else str(row[3]),
        cycle_start_date=None if row[4] is None else str(row[4]),
        status=str(row[5]),
        priority=int(row[6]),
        activity_type=None if row[7] is None else str(row[7]),
        description=None if row[8] is None else str(row[8]),
        created_at=str(row[9]),
        created_by=str(row[10]),
    )


def validate_activity_status(status: str) -> str:
    normalized_status = validate_required_text("Activity status", status).lower()
    if normalized_status not in ALLOWED_ACTIVITY_STATUSES:
        allowed_display = ", ".join(ALLOWED_ACTIVITY_STATUSES)
        raise WorkspaceBootstrapError(
            f"Invalid activity status: {normalized_status}. Allowed: {allowed_display}."
        )
    return normalized_status


def activity_state_payload(record: ActivityRecord) -> dict[str, object]:
    return {
        "id": record.id,
        "title": record.title,
        "cycle_id": record.cycle_id,
        "cycle_type": record.cycle_type,
        "cycle_start_date": record.cycle_start_date,
        "status": record.status,
        "priority": record.priority,
        "type": record.activity_type,
        "description": record.description,
        "created_at": record.created_at,
        "created_by": record.created_by,
    }
