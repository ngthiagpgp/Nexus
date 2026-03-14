from __future__ import annotations

import json
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

    if cycle_id:
        clauses.append("cycle_id = ?")
        params.append(validate_required_text("Cycle id", cycle_id))

    if status:
        clauses.append("status = ?")
        params.append(validate_required_text("Activity status", status))

    if clauses:
        query += " WHERE " + " AND ".join(clauses)

    query += " ORDER BY c.start_date DESC, a.priority ASC, a.created_at DESC, a.title ASC"

    with connect_workspace_database(workspace.database_path, read_only=True) as connection:
        rows = connection.execute(query, params).fetchall()

    return [
        ActivityRecord(
            id=row[0],
            title=row[1],
            cycle_id=row[2],
            cycle_type=row[3],
            cycle_start_date=str(row[4]),
            status=row[5],
            priority=int(row[6]),
            activity_type=row[7],
            description=row[8],
            created_at=str(row[9]),
            created_by=row[10],
        )
        for row in rows
    ]


def fetch_cycle_details(connection, cycle_id: str) -> tuple[str, str]:
    row = connection.execute(
        "SELECT type, start_date FROM cycles WHERE id = ?",
        [cycle_id],
    ).fetchone()
    if row is None:
        raise WorkspaceBootstrapError(f"Cycle not found: {cycle_id}")
    return row[0], str(row[1])
