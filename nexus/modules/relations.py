from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from nexus.modules.entities import normalize_optional_text, validate_required_text
from nexus.core.workspace import (
    WorkspaceBootstrapError,
    connect_workspace_database,
    fetch_system_state_value,
    require_workspace,
    utc_now,
)


@dataclass(frozen=True)
class RelationRecord:
    id: str
    entity_a_id: str
    entity_b_id: str
    relation_type: str
    weight: float
    context: str | None
    created_at: str
    created_by: str


def create_relation(
    workspace_root: Path,
    *,
    from_entity: str,
    to_entity: str,
    relation_type: str,
    context: str | None,
) -> RelationRecord:
    workspace = require_workspace(workspace_root)
    normalized_from = validate_required_text("From entity", from_entity)
    normalized_to = validate_required_text("To entity", to_entity)
    normalized_type = validate_required_text("Relation type", relation_type)
    normalized_context = normalize_optional_text(context)
    timestamp = utc_now()
    relation_id = str(uuid4())
    workspace_id = "default"
    cli_id = "local"
    actor = "user"

    with connect_workspace_database(workspace.database_path) as connection:
        workspace_id = fetch_system_state_value(connection, "default_workspace") or "default"
        entity_a_id = resolve_entity_reference(connection, normalized_from)
        entity_b_id = resolve_entity_reference(connection, normalized_to)

        connection.execute(
            """
            INSERT INTO relations (
                id,
                entity_a_id,
                entity_b_id,
                relation_type,
                weight,
                context,
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
                relation_id,
                entity_a_id,
                entity_b_id,
                normalized_type,
                0.5,
                normalized_context,
                actor,
                timestamp,
                actor,
                timestamp,
                workspace_id,
                cli_id,
            ],
        )

        new_state = {
            "id": relation_id,
            "entity_a_id": entity_a_id,
            "entity_b_id": entity_b_id,
            "relation_type": normalized_type,
            "weight": 0.5,
            "context": normalized_context,
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
                "relation",
                relation_id,
                None,
                json.dumps(new_state, ensure_ascii=True),
                actor,
                "CLI relation create",
                timestamp,
                workspace_id,
                cli_id,
            ],
        )

    return RelationRecord(
        id=relation_id,
        entity_a_id=entity_a_id,
        entity_b_id=entity_b_id,
        relation_type=normalized_type,
        weight=0.5,
        context=normalized_context,
        created_at=timestamp,
        created_by=actor,
    )


def list_relations(
    workspace_root: Path,
    *,
    from_entity: str | None = None,
    to_entity: str | None = None,
    relation_type: str | None = None,
) -> list[RelationRecord]:
    workspace = require_workspace(workspace_root)
    query = """
        SELECT
            id,
            entity_a_id,
            entity_b_id,
            relation_type,
            weight,
            context,
            created_at,
            created_by
        FROM relations
    """
    clauses: list[str] = []
    params: list[str] = []

    with connect_workspace_database(workspace.database_path, read_only=True) as connection:
        normalized_from = normalize_optional_text(from_entity)
        normalized_to = normalize_optional_text(to_entity)
        normalized_type = normalize_optional_text(relation_type)

        if normalized_from:
            clauses.append("entity_a_id = ?")
            params.append(resolve_entity_reference(connection, normalized_from))

        if normalized_to:
            clauses.append("entity_b_id = ?")
            params.append(resolve_entity_reference(connection, normalized_to))

        if normalized_type:
            clauses.append("relation_type = ?")
            params.append(normalized_type)

        if clauses:
            query += " WHERE " + " AND ".join(clauses)

        query += " ORDER BY created_at DESC, relation_type ASC"
        rows = connection.execute(query, params).fetchall()

    return [
        relation_record_from_row(row)
        for row in rows
    ]


def relation_display_map(workspace_root: Path) -> dict[str, str]:
    workspace = require_workspace(workspace_root)
    with connect_workspace_database(workspace.database_path, read_only=True) as connection:
        rows = connection.execute("SELECT id, name FROM entities").fetchall()
    return {row[0]: row[1] for row in rows}


def resolve_entity_reference(connection, reference: str) -> str:
    by_id = connection.execute(
        "SELECT id FROM entities WHERE id = ?",
        [reference],
    ).fetchall()
    if len(by_id) == 1:
        return by_id[0][0]

    by_name = connection.execute(
        "SELECT id FROM entities WHERE name = ? ORDER BY created_at ASC",
        [reference],
    ).fetchall()
    if len(by_name) == 1:
        return by_name[0][0]
    if len(by_name) > 1:
        raise WorkspaceBootstrapError(
            f"Entity reference is ambiguous: {reference}. Use the entity id instead."
        )

    raise WorkspaceBootstrapError(f"Entity not found: {reference}")


def relation_record_from_row(row: Sequence[object]) -> RelationRecord:
    return RelationRecord(
        id=str(row[0]),
        entity_a_id=str(row[1]),
        entity_b_id=str(row[2]),
        relation_type=str(row[3]),
        weight=float(row[4]),
        context=None if row[5] is None else str(row[5]),
        created_at=str(row[6]),
        created_by=str(row[7]),
    )
