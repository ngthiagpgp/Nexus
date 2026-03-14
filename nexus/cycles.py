from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, datetime, time
from pathlib import Path
from uuid import uuid4

from nexus.entities import normalize_optional_text, validate_required_text
from nexus.workspace import (
    WorkspaceBootstrapError,
    connect_workspace_database,
    fetch_system_state_value,
    require_workspace,
    utc_now,
)


@dataclass(frozen=True)
class CycleRecord:
    id: str
    type: str
    start_date: str
    end_date: str | None
    status: str
    description: str | None
    created_at: str
    created_by: str
    activity_count: int
    pending_count: int
    in_progress_count: int
    completed_count: int
    blocked_count: int


def create_cycle(
    workspace_root: Path,
    *,
    cycle_type: str,
    start: str,
    end: str | None = None,
) -> CycleRecord:
    workspace = require_workspace(workspace_root)
    normalized_type = validate_required_text("Cycle type", cycle_type)
    start_dt = parse_required_cycle_datetime("Cycle start", start)
    end_dt = parse_optional_cycle_datetime("Cycle end", end)
    cycle_id = build_cycle_id(normalized_type, start_dt)
    timestamp = utc_now()
    actor = "user"
    cli_id = "local"
    workspace_id = "default"

    with connect_workspace_database(workspace.database_path) as connection:
        workspace_id = fetch_system_state_value(connection, "default_workspace") or "default"
        existing_row = connection.execute(
            "SELECT id FROM cycles WHERE id = ?",
            [cycle_id],
        ).fetchone()
        if existing_row is not None:
            raise WorkspaceBootstrapError(f"Cycle already exists: {cycle_id}")

        connection.execute(
            """
            INSERT INTO cycles (
                id,
                type,
                start_date,
                end_date,
                status,
                description,
                created_by,
                created_at,
                modified_by,
                modified_at,
                id_workspace,
                id_cli
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                cycle_id,
                normalized_type,
                format_cycle_datetime(start_dt),
                format_cycle_datetime(end_dt) if end_dt else None,
                "active",
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
            "id": cycle_id,
            "type": normalized_type,
            "start_date": format_cycle_datetime(start_dt),
            "end_date": format_cycle_datetime(end_dt) if end_dt else None,
            "status": "active",
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
                "cycle",
                cycle_id,
                None,
                json.dumps(new_state, ensure_ascii=True),
                actor,
                "CLI cycle create",
                timestamp,
                workspace_id,
                cli_id,
            ],
        )

    return CycleRecord(
        id=cycle_id,
        type=normalized_type,
        start_date=format_cycle_datetime(start_dt),
        end_date=format_cycle_datetime(end_dt) if end_dt else None,
        status="active",
        description=None,
        created_at=timestamp,
        created_by=actor,
        activity_count=0,
        pending_count=0,
        in_progress_count=0,
        completed_count=0,
        blocked_count=0,
    )


def list_cycles(
    workspace_root: Path,
    *,
    cycle_type: str | None = None,
    status: str | None = None,
) -> list[CycleRecord]:
    workspace = require_workspace(workspace_root)
    query = """
        SELECT
            c.id,
            c.type,
            c.start_date,
            c.end_date,
            c.status,
            c.description,
            c.created_at,
            c.created_by,
            COUNT(a.id) AS activity_count,
            COALESCE(SUM(CASE WHEN a.status = 'pending' THEN 1 ELSE 0 END), 0) AS pending_count,
            COALESCE(SUM(CASE WHEN a.status = 'in_progress' THEN 1 ELSE 0 END), 0) AS in_progress_count,
            COALESCE(SUM(CASE WHEN a.status = 'completed' THEN 1 ELSE 0 END), 0) AS completed_count,
            COALESCE(SUM(CASE WHEN a.status = 'blocked' THEN 1 ELSE 0 END), 0) AS blocked_count
        FROM cycles c
        LEFT JOIN activities a ON a.cycle_id = c.id
    """
    clauses: list[str] = []
    params: list[str] = []

    normalized_type = normalize_optional_text(cycle_type)
    if normalized_type:
        clauses.append("c.type = ?")
        params.append(normalized_type)

    normalized_status = normalize_optional_text(status)
    if normalized_status:
        clauses.append("c.status = ?")
        params.append(normalized_status)

    if clauses:
        query += " WHERE " + " AND ".join(clauses)

    query += """
        GROUP BY
            c.id,
            c.type,
            c.start_date,
            c.end_date,
            c.status,
            c.description,
            c.created_at,
            c.created_by
    """
    query += " ORDER BY c.start_date DESC, c.type ASC"

    with connect_workspace_database(workspace.database_path, read_only=True) as connection:
        rows = connection.execute(query, params).fetchall()

    return [
        CycleRecord(
            id=row[0],
            type=row[1],
            start_date=str(row[2]),
            end_date=str(row[3]) if row[3] is not None else None,
            status=row[4],
            description=row[5],
            created_at=str(row[6]),
            created_by=row[7],
            activity_count=int(row[8]),
            pending_count=int(row[9]),
            in_progress_count=int(row[10]),
            completed_count=int(row[11]),
            blocked_count=int(row[12]),
        )
        for row in rows
    ]


def build_cycle_id(cycle_type: str, start_dt: datetime) -> str:
    return f"cycle-{cycle_type}-{start_dt.date().isoformat()}"


def parse_required_cycle_datetime(label: str, value: str) -> datetime:
    normalized = validate_required_text(label, value)
    return parse_cycle_datetime(label, normalized)


def parse_optional_cycle_datetime(label: str, value: str | None) -> datetime | None:
    normalized = normalize_optional_text(value)
    if not normalized:
        return None
    return parse_cycle_datetime(label, normalized)


def parse_cycle_datetime(label: str, value: str) -> datetime:
    try:
        if "T" in value or " " in value:
            return datetime.fromisoformat(value)
        parsed_date = date.fromisoformat(value)
        return datetime.combine(parsed_date, time(0, 0, 0))
    except ValueError as exc:
        raise WorkspaceBootstrapError(
            f"{label} must be an ISO date or datetime: {value}"
        ) from exc


def format_cycle_datetime(value: datetime) -> str:
    return value.strftime("%Y-%m-%d %H:%M:%S")
