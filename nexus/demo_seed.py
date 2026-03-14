from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from nexus.activities import create_activity, update_activity_status
from nexus.cycles import create_cycle
from nexus.documents import create_document, reconcile_document, update_document_status
from nexus.entities import create_entity
from nexus.relations import create_relation
from nexus.workspace import (
    WorkspaceBootstrapError,
    connect_workspace_database,
    fetch_system_state_value,
    require_workspace,
    utc_now,
)

DEMO_SEED_VERSION = "1"


@dataclass(frozen=True)
class DemoSeedResult:
    created: bool
    cycle_count: int
    activity_count: int
    entity_count: int
    document_count: int
    relation_count: int
    workspace_root: Path


def seed_demo_workspace(workspace_root: Path) -> DemoSeedResult:
    workspace = require_workspace(workspace_root)

    with connect_workspace_database(workspace.database_path) as connection:
        existing_version = fetch_system_state_value(connection, "demo_seed_version")
        if existing_version == DEMO_SEED_VERSION:
            return DemoSeedResult(
                created=False,
                cycle_count=_count_rows(connection, "cycles"),
                activity_count=_count_rows(connection, "activities"),
                entity_count=_count_rows(connection, "entities"),
                document_count=_count_rows(connection, "documents"),
                relation_count=_count_rows(connection, "relations"),
                workspace_root=workspace.workspace_root,
            )

        if any(
            _count_rows(connection, table) > 0
            for table in ("cycles", "activities", "entities", "documents", "relations")
        ):
            raise WorkspaceBootstrapError(
                "Demo seed can only run on an empty workspace or a workspace already seeded "
                "by this command."
            )

    cycle = create_cycle(
        workspace.workspace_root,
        cycle_type="daily",
        start="2026-03-14",
    )

    project = create_entity(
        workspace.workspace_root,
        name="Nexus MVP",
        entity_type="project",
        context="Local-first operational workspace bootstrap",
    )
    owner = create_entity(
        workspace.workspace_root,
        name="Thiago Gardin",
        entity_type="person",
        context="Primary operator and reviewer",
    )
    concept = create_entity(
        workspace.workspace_root,
        name="Operational Review",
        entity_type="concept",
        context="Cycle-based supervision and document governance",
    )

    create_relation(
        workspace.workspace_root,
        from_entity=owner.id,
        to_entity=project.id,
        relation_type="owner_of",
        context="Thiago is supervising the MVP workspace",
    )
    create_relation(
        workspace.workspace_root,
        from_entity=project.id,
        to_entity=concept.id,
        relation_type="references",
        context="The project is organized around explicit operational review",
    )

    create_activity(
        workspace.workspace_root,
        title="Review current workspace status",
        cycle_id=cycle.id,
    )
    in_progress_activity = create_activity(
        workspace.workspace_root,
        title="Approve weekly operating note",
        cycle_id=cycle.id,
    )
    completed_activity = create_activity(
        workspace.workspace_root,
        title="Archive previous retrospective",
        cycle_id=cycle.id,
    )

    update_activity_status(
        workspace.workspace_root,
        activity_id=in_progress_activity.id,
        status="in_progress",
        actor="user",
        reason="CLI demo seed activity status update",
        cli_id="seed",
    )
    update_activity_status(
        workspace.workspace_root,
        activity_id=completed_activity.id,
        status="completed",
        actor="user",
        reason="CLI demo seed activity status update",
        cli_id="seed",
    )

    draft_document = create_document(
        workspace.workspace_root,
        document_type="daily",
        title="Daily 2026-03-14",
        cycle_id=cycle.id,
    )
    approved_document = create_document(
        workspace.workspace_root,
        document_type="note",
        title="Operating Brief",
        cycle_id=cycle.id,
    )
    archived_document = create_document(
        workspace.workspace_root,
        document_type="report",
        title="Previous Retrospective",
        cycle_id=cycle.id,
    )

    _write_document_content(
        workspace.workspace_root / draft_document.path,
        "# Daily 2026-03-14\n\n## Focus\n- Review current workspace status\n- Check cycle activity mix\n",
    )
    _write_document_content(
        workspace.workspace_root / approved_document.path,
        "# Operating Brief\n\n## Current State\n- Cockpit is serving local supervision\n- Document lifecycle is available\n",
    )
    _write_document_content(
        workspace.workspace_root / archived_document.path,
        "# Previous Retrospective\n\n## Closed Items\n- Early bootstrap slice completed\n- Local inspection surface stabilized\n",
    )

    for document_id in (draft_document.id, approved_document.id, archived_document.id):
        reconcile_document(
            workspace.workspace_root,
            selector=document_id,
            actor="user",
            reason="CLI demo seed document reconcile",
            cli_id="seed",
            allow_title_lookup=False,
        )

    update_document_status(
        workspace.workspace_root,
        selector=approved_document.id,
        status="approved",
        actor="user",
        reason="CLI demo seed document status update",
        cli_id="seed",
        allow_title_lookup=False,
    )
    update_document_status(
        workspace.workspace_root,
        selector=archived_document.id,
        status="approved",
        actor="user",
        reason="CLI demo seed document status update",
        cli_id="seed",
        allow_title_lookup=False,
    )
    update_document_status(
        workspace.workspace_root,
        selector=archived_document.id,
        status="archived",
        actor="user",
        reason="CLI demo seed document status update",
        cli_id="seed",
        allow_title_lookup=False,
    )

    with connect_workspace_database(workspace.database_path) as connection:
        now = utc_now()
        connection.execute(
            """
            INSERT OR REPLACE INTO system_state (key, value, last_updated)
            VALUES (?, ?, ?)
            """,
            ["demo_seed_version", DEMO_SEED_VERSION, now],
        )
        connection.execute(
            """
            INSERT OR REPLACE INTO system_state (key, value, last_updated)
            VALUES (?, ?, ?)
            """,
            ["demo_seed_applied_at", now, now],
        )
        return DemoSeedResult(
            created=True,
            cycle_count=_count_rows(connection, "cycles"),
            activity_count=_count_rows(connection, "activities"),
            entity_count=_count_rows(connection, "entities"),
            document_count=_count_rows(connection, "documents"),
            relation_count=_count_rows(connection, "relations"),
            workspace_root=workspace.workspace_root,
        )


def _count_rows(connection, table: str) -> int:
    row = connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
    return 0 if row is None else int(row[0])


def _write_document_content(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")
