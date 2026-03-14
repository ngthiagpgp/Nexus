from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from nexus.workspace import (
    WorkspaceBootstrapError,
    connect_workspace_database,
    fetch_system_state_value,
    require_workspace,
    utc_now,
)


@dataclass(frozen=True)
class EntityRecord:
    id: str
    name: str
    type: str
    context: str | None
    created_at: str
    created_by: str
    modified_at: str
    modified_by: str
    id_workspace: str
    id_cli: str


def create_entity(workspace_root: Path, *, name: str, entity_type: str, context: str | None) -> EntityRecord:
    workspace = require_workspace(workspace_root)
    timestamp = utc_now()
    entity_id = str(uuid4())

    with connect_workspace_database(workspace.database_path) as connection:
        workspace_id = fetch_system_state_value(connection, "default_workspace") or "default"
        cli_id = "local"
        normalized_context = normalize_optional_text(context)

        connection.execute(
            """
            INSERT INTO entities (
                id,
                name,
                type,
                context,
                created_by,
                created_at,
                modified_by,
                modified_at,
                id_workspace,
                id_cli
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                entity_id,
                name,
                entity_type,
                normalized_context,
                "user",
                timestamp,
                "user",
                timestamp,
                workspace_id,
                cli_id,
            ],
        )

        new_state = {
            "id": entity_id,
            "name": name,
            "type": entity_type,
            "context": normalized_context,
            "created_by": "user",
            "created_at": timestamp,
            "modified_by": "user",
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
                "entity",
                entity_id,
                None,
                json.dumps(new_state, ensure_ascii=True),
                "user",
                "CLI entity create",
                timestamp,
                workspace_id,
                cli_id,
            ],
        )

    return EntityRecord(
        id=entity_id,
        name=name,
        type=entity_type,
        context=normalized_context,
        created_at=timestamp,
        created_by="user",
        modified_at=timestamp,
        modified_by="user",
        id_workspace=workspace_id,
        id_cli=cli_id,
    )


def list_entities(workspace_root: Path, *, entity_type: str | None = None) -> list[EntityRecord]:
    workspace = require_workspace(workspace_root)
    query = """
        SELECT
            id,
            name,
            type,
            context,
            created_at,
            created_by,
            modified_at,
            modified_by,
            id_workspace,
            id_cli
        FROM entities
    """
    params: list[str] = []

    if entity_type:
        query += " WHERE type = ?"
        params.append(entity_type)

    query += " ORDER BY name ASC, created_at ASC"

    with connect_workspace_database(workspace.database_path, read_only=True) as connection:
        rows = connection.execute(query, params).fetchall()

    return [
        entity_record_from_row(row)
        for row in rows
    ]


def get_entity(workspace_root: Path, *, entity_id: str) -> EntityRecord:
    workspace = require_workspace(workspace_root)
    normalized_entity_id = validate_required_text("Entity id", entity_id)

    with connect_workspace_database(workspace.database_path, read_only=True) as connection:
        row = connection.execute(
            """
            SELECT
                id,
                name,
                type,
                context,
                created_at,
                created_by,
                modified_at,
                modified_by,
                id_workspace,
                id_cli
            FROM entities
            WHERE id = ?
            """,
            [normalized_entity_id],
        ).fetchone()

    if row is None:
        raise WorkspaceBootstrapError(f"Entity not found: {normalized_entity_id}")

    return entity_record_from_row(row)


def validate_required_text(label: str, value: str | None) -> str:
    normalized = normalize_optional_text(value)
    if not normalized:
        raise WorkspaceBootstrapError(f"{label} is required and cannot be blank.")
    return normalized


def normalize_optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    return normalized or None


def entity_record_from_row(row: Sequence[object]) -> EntityRecord:
    return EntityRecord(
        id=str(row[0]),
        name=str(row[1]),
        type=str(row[2]),
        context=None if row[3] is None else str(row[3]),
        created_at=str(row[4]),
        created_by=str(row[5]),
        modified_at=str(row[6]),
        modified_by=str(row[7]),
        id_workspace=str(row[8]),
        id_cli=str(row[9]),
    )
