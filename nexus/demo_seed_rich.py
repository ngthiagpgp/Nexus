from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

from nexus.activities import create_activity, update_activity_status
from nexus.core.workspace import (
    WorkspaceBootstrapError,
    connect_workspace_database,
    fetch_system_state_value,
    require_workspace,
    utc_now,
)
from nexus.cycles import create_cycle
from nexus.demo_seed import DemoSeedResult
from nexus.documents import create_document, reconcile_document, update_document_status
from nexus.entities import create_entity
from nexus.relations import create_relation

RICH_DEMO_SEED_VERSION = "1"
RICH_DEMO_SEED_MARKER = "demo_seed_rich_version"


def seed_rich_demo_workspace(workspace_root: Path) -> DemoSeedResult:
    workspace = require_workspace(workspace_root)

    with connect_workspace_database(workspace.database_path) as connection:
        existing_version = fetch_system_state_value(connection, RICH_DEMO_SEED_MARKER)
        if existing_version == RICH_DEMO_SEED_VERSION:
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
                "Rich demo seed can only run on an empty workspace or a workspace already "
                "seeded by this command."
            )

    cycle_execution = create_cycle(
        workspace.workspace_root,
        cycle_type="weekly",
        start="2026-03-16",
    )
    cycle_today = create_cycle(
        workspace.workspace_root,
        cycle_type="daily",
        start="2026-03-15",
    )
    cycle_completed = create_cycle(
        workspace.workspace_root,
        cycle_type="weekly",
        start="2026-03-09",
    )
    cycle_archived = create_cycle(
        workspace.workspace_root,
        cycle_type="weekly",
        start="2026-03-02",
    )

    _update_cycle_state(
        workspace.workspace_root,
        cycle_id=cycle_execution.id,
        description="Primary operating window for the upcoming human walkthrough and decision review.",
        reason="Rich demo seed cycle staging",
    )
    _update_cycle_state(
        workspace.workspace_root,
        cycle_id=cycle_today.id,
        description="Daily execution slice used to validate what is visible right now in the cockpit.",
        reason="Rich demo seed cycle staging",
    )
    _update_cycle_state(
        workspace.workspace_root,
        cycle_id=cycle_completed.id,
        status="completed",
        description="Recently closed weekly cycle with accepted UI and supervision decisions.",
        reason="Rich demo seed cycle staging",
    )
    _update_cycle_state(
        workspace.workspace_root,
        cycle_id=cycle_archived.id,
        status="archived",
        description="Older recovery cycle retained for context, not for active operational focus.",
        reason="Rich demo seed cycle staging",
    )

    project = create_entity(
        workspace.workspace_root,
        name="Nexus Product Delivery",
        entity_type="project",
        context="Shared local-first supervision workspace for the MVP.",
    )
    sprint = create_entity(
        workspace.workspace_root,
        name="Human Test Sprint",
        entity_type="project",
        context="Focused delivery slice for operator comprehension and demo readiness.",
    )
    owner = create_entity(
        workspace.workspace_root,
        name="Thiago Gardin",
        entity_type="person",
        context="Primary operator and reviewer of the workspace.",
    )
    reviewer = create_entity(
        workspace.workspace_root,
        name="Maria Review",
        entity_type="person",
        context="Secondary reviewer focused on human legibility and evidence quality.",
    )
    integrity = create_entity(
        workspace.workspace_root,
        name="Document Integrity",
        entity_type="concept",
        context="Confidence signal for whether file-backed records are trustworthy.",
    )
    readability = create_entity(
        workspace.workspace_root,
        name="Cockpit Readability",
        entity_type="concept",
        context="North-star concern for cycle-first human supervision.",
    )
    evidence_packet = create_entity(
        workspace.workspace_root,
        name="Evidence Packet",
        entity_type="resource",
        context="Supporting notes and proof required to close blocked work safely.",
    )

    create_relation(
        workspace.workspace_root,
        from_entity=owner.id,
        to_entity=sprint.id,
        relation_type="owner_of",
        context="Thiago is driving the current human test sprint.",
    )
    create_relation(
        workspace.workspace_root,
        from_entity=sprint.id,
        to_entity=project.id,
        relation_type="supports",
        context="This sprint exists to improve the Nexus product surface.",
    )
    create_relation(
        workspace.workspace_root,
        from_entity=reviewer.id,
        to_entity=sprint.id,
        relation_type="reviews",
        context="Secondary reviewer validates legibility and trust signals.",
    )
    create_relation(
        workspace.workspace_root,
        from_entity=integrity.id,
        to_entity=sprint.id,
        relation_type="constrains",
        context="Integrity problems block safe operator trust.",
    )
    create_relation(
        workspace.workspace_root,
        from_entity=evidence_packet.id,
        to_entity=integrity.id,
        relation_type="supports",
        context="Evidence packet is required to resolve integrity-sensitive blockers.",
    )
    create_relation(
        workspace.workspace_root,
        from_entity=readability.id,
        to_entity=sprint.id,
        relation_type="guides",
        context="Readability is the decision frame for this seed scenario.",
    )
    create_relation(
        workspace.workspace_root,
        from_entity=sprint.id,
        to_entity=evidence_packet.id,
        relation_type="depends_on",
        context="Current sprint still depends on missing proof and updated notes.",
    )

    activities = {
        "copy": create_activity(
            workspace.workspace_root,
            title="Approve operator-facing copy before the walkthrough",
            cycle_id=cycle_execution.id,
        ),
        "evidence": create_activity(
            workspace.workspace_root,
            title="Resolve evidence gap before human review",
            cycle_id=cycle_execution.id,
        ),
        "screenshots": create_activity(
            workspace.workspace_root,
            title="Refresh screenshot set for release notes",
            cycle_id=cycle_execution.id,
        ),
        "reconcile": create_activity(
            workspace.workspace_root,
            title="Reconcile the drifted handoff memo",
            cycle_id=cycle_execution.id,
        ),
        "walkthrough": create_activity(
            workspace.workspace_root,
            title="Run local walkthrough on the seeded workspace",
            cycle_id=cycle_today.id,
        ),
        "blocked-check": create_activity(
            workspace.workspace_root,
            title="Verify blocked work is obvious in the cockpit",
            cycle_id=cycle_today.id,
        ),
        "audit-check": create_activity(
            workspace.workspace_root,
            title="Confirm audit stays secondary on the main surface",
            cycle_id=cycle_today.id,
        ),
        "close-notes": create_activity(
            workspace.workspace_root,
            title="Close previous comprehension patch notes",
            cycle_id=cycle_completed.id,
        ),
        "archive-guidance": create_activity(
            workspace.workspace_root,
            title="Archive superseded operator guidance",
            cycle_id=cycle_completed.id,
        ),
        "snapshot": create_activity(
            workspace.workspace_root,
            title="Snapshot earlier recovery assumptions for reference",
            cycle_id=cycle_archived.id,
        ),
    }

    _update_activity_details(
        workspace.workspace_root,
        activity_id=activities["copy"].id,
        priority=1,
        activity_type="writing",
        description="Time-sensitive copy gate before the operator walkthrough starts.",
        reason="Rich demo seed activity staging",
    )
    _update_activity_details(
        workspace.workspace_root,
        activity_id=activities["evidence"].id,
        priority=1,
        activity_type="review",
        description="Blocked until supporting evidence and document alignment are resolved.",
        reason="Rich demo seed activity staging",
    )
    _update_activity_details(
        workspace.workspace_root,
        activity_id=activities["screenshots"].id,
        priority=2,
        activity_type="output",
        description="Screenshot set is mid-refresh for release and demo material.",
        reason="Rich demo seed activity staging",
    )
    _update_activity_details(
        workspace.workspace_root,
        activity_id=activities["reconcile"].id,
        priority=2,
        activity_type="maintenance",
        description="Uses the current reconcile flow to restore confidence in a supporting memo.",
        reason="Rich demo seed activity staging",
    )
    _update_activity_details(
        workspace.workspace_root,
        activity_id=activities["walkthrough"].id,
        priority=2,
        activity_type="review",
        description="Daily execution activity confirming the cockpit can be walked end to end.",
        reason="Rich demo seed activity staging",
    )
    _update_activity_details(
        workspace.workspace_root,
        activity_id=activities["blocked-check"].id,
        priority=2,
        activity_type="review",
        description="Checks whether tension is visually legible without reading source code.",
        reason="Rich demo seed activity staging",
    )
    _update_activity_details(
        workspace.workspace_root,
        activity_id=activities["audit-check"].id,
        priority=3,
        activity_type="review",
        description="Ensures audit signals remain available but do not dominate the main flow.",
        reason="Rich demo seed activity staging",
    )
    _update_activity_details(
        workspace.workspace_root,
        activity_id=activities["close-notes"].id,
        priority=3,
        activity_type="writing",
        description="Recently completed closure work from the previous pass.",
        reason="Rich demo seed activity staging",
    )
    _update_activity_details(
        workspace.workspace_root,
        activity_id=activities["archive-guidance"].id,
        priority=4,
        activity_type="maintenance",
        description="Low urgency archive of older guidance kept for historical context.",
        reason="Rich demo seed activity staging",
    )
    _update_activity_details(
        workspace.workspace_root,
        activity_id=activities["snapshot"].id,
        priority=4,
        activity_type="analysis",
        description="Archived recovery snapshot that still provides structural context.",
        reason="Rich demo seed activity staging",
    )

    update_activity_status(
        workspace.workspace_root,
        activity_id=activities["evidence"].id,
        status="blocked",
        actor="user",
        reason="Rich demo seed activity status update",
        cli_id="seed-rich",
    )
    update_activity_status(
        workspace.workspace_root,
        activity_id=activities["screenshots"].id,
        status="in_progress",
        actor="user",
        reason="Rich demo seed activity status update",
        cli_id="seed-rich",
    )
    update_activity_status(
        workspace.workspace_root,
        activity_id=activities["walkthrough"].id,
        status="completed",
        actor="user",
        reason="Rich demo seed activity status update",
        cli_id="seed-rich",
    )
    update_activity_status(
        workspace.workspace_root,
        activity_id=activities["blocked-check"].id,
        status="in_progress",
        actor="user",
        reason="Rich demo seed activity status update",
        cli_id="seed-rich",
    )
    update_activity_status(
        workspace.workspace_root,
        activity_id=activities["close-notes"].id,
        status="completed",
        actor="user",
        reason="Rich demo seed activity status update",
        cli_id="seed-rich",
    )
    update_activity_status(
        workspace.workspace_root,
        activity_id=activities["archive-guidance"].id,
        status="completed",
        actor="user",
        reason="Rich demo seed activity status update",
        cli_id="seed-rich",
    )
    update_activity_status(
        workspace.workspace_root,
        activity_id=activities["snapshot"].id,
        status="completed",
        actor="user",
        reason="Rich demo seed activity status update",
        cli_id="seed-rich",
    )

    documents = {
        "weekly_active": create_document(
            workspace.workspace_root,
            document_type="weekly",
            title="Weekly 2026-W12",
            cycle_id=cycle_execution.id,
        ),
        "handoff": create_document(
            workspace.workspace_root,
            document_type="note",
            title="Operator Handoff Memo",
            cycle_id=cycle_execution.id,
        ),
        "evidence": create_document(
            workspace.workspace_root,
            document_type="report",
            title="Evidence Gap Register",
            cycle_id=cycle_execution.id,
        ),
        "watchlist": create_document(
            workspace.workspace_root,
            document_type="note",
            title="Stakeholder Watchlist",
            cycle_id=cycle_execution.id,
        ),
        "daily": create_document(
            workspace.workspace_root,
            document_type="daily",
            title="Daily 2026-03-15",
            cycle_id=cycle_today.id,
        ),
        "walkthrough": create_document(
            workspace.workspace_root,
            document_type="note",
            title="Cockpit Walkthrough Script",
            cycle_id=cycle_today.id,
        ),
        "weekly_completed": create_document(
            workspace.workspace_root,
            document_type="weekly",
            title="Weekly 2026-W11",
            cycle_id=cycle_completed.id,
        ),
        "archive": create_document(
            workspace.workspace_root,
            document_type="report",
            title="UI Readout Archive",
            cycle_id=cycle_completed.id,
        ),
        "snapshot": create_document(
            workspace.workspace_root,
            document_type="note",
            title="Recovery Snapshot",
            cycle_id=cycle_archived.id,
        ),
    }

    _write_document_content(
        workspace.workspace_root / documents["weekly_active"].path,
        "# Weekly 2026-W12\n\n## Operational focus\n- Human walkthrough is the primary gate.\n- Blocked work must stay legible in the cockpit.\n- Supporting evidence is still incomplete for one high-risk activity.\n",
    )
    _write_document_content(
        workspace.workspace_root / documents["handoff"].path,
        "# Operator Handoff Memo\n\n## Current read\n- Start from the active weekly cycle.\n- Inspect blocked work before approving any supporting memo.\n- Use the audit section only after understanding the work flow.\n",
    )
    _write_document_content(
        workspace.workspace_root / documents["evidence"].path,
        "# Evidence Gap Register\n\n## Missing evidence\n- Final reviewer note is still missing.\n- One supporting memo needs reconcile before approval.\n- Screenshot evidence is still being refreshed.\n",
    )
    _write_document_content(
        workspace.workspace_root / documents["watchlist"].path,
        "# Stakeholder Watchlist\n\n## Current concerns\n- Reviewer attention is concentrated on blocked work.\n- Readability regressions are more important than feature count.\n",
    )
    _write_document_content(
        workspace.workspace_root / documents["daily"].path,
        "# Daily 2026-03-15\n\n## Execution snapshot\n- Demo workspace was created successfully.\n- Walkthrough started with cycle-first orientation.\n- Secondary surfaces stayed visible but calm.\n",
    )
    _write_document_content(
        workspace.workspace_root / documents["walkthrough"].path,
        "# Cockpit Walkthrough Script\n\n## Steps\n1. Open the active weekly cycle.\n2. Inspect the blocked activity.\n3. Open the supporting memo and observe the integrity warning.\n4. Expand audit only after the main work path is clear.\n",
    )
    _write_document_content(
        workspace.workspace_root / documents["weekly_completed"].path,
        "# Weekly 2026-W11\n\n## Accepted outcomes\n- Previous comprehension patch shipped.\n- Activity and document inspection became more stable.\n",
    )
    _write_document_content(
        workspace.workspace_root / documents["archive"].path,
        "# UI Readout Archive\n\n## Archived note\n- Older readout kept for comparison only.\n- Not part of the current operating window.\n",
    )
    _write_document_content(
        workspace.workspace_root / documents["snapshot"].path,
        "# Recovery Snapshot\n\n## Archived reference\n- Earlier assumptions remain available for background context.\n- Do not treat this note as current operational guidance.\n",
    )

    for key, document in documents.items():
        reconcile_document(
            workspace.workspace_root,
            selector=document.id,
            actor="user",
            reason="Rich demo seed document reconcile",
            cli_id="seed-rich",
            allow_title_lookup=False,
        )
        if key in {"weekly_active", "handoff", "daily", "weekly_completed", "archive", "snapshot"}:
            update_document_status(
                workspace.workspace_root,
                selector=document.id,
                status="approved",
                actor="user",
                reason="Rich demo seed document status update",
                cli_id="seed-rich",
                allow_title_lookup=False,
            )
        if key in {"archive", "snapshot"}:
            update_document_status(
                workspace.workspace_root,
                selector=document.id,
                status="archived",
                actor="user",
                reason="Rich demo seed document status update",
                cli_id="seed-rich",
                allow_title_lookup=False,
            )

    _write_document_content(
        workspace.workspace_root / documents["handoff"].path,
        "# Operator Handoff Memo\n\n## Current read\n- Start from the active weekly cycle.\n- Inspect blocked work before approving any supporting memo.\n- Use the audit section only after understanding the work flow.\n- Drift note: one line was updated after approval and now needs reconcile.\n",
    )

    with connect_workspace_database(workspace.database_path) as connection:
        now = utc_now()
        connection.execute(
            """
            INSERT OR REPLACE INTO system_state (key, value, last_updated)
            VALUES (?, ?, ?)
            """,
            [RICH_DEMO_SEED_MARKER, RICH_DEMO_SEED_VERSION, now],
        )
        connection.execute(
            """
            INSERT OR REPLACE INTO system_state (key, value, last_updated)
            VALUES (?, ?, ?)
            """,
            ["demo_seed_rich_applied_at", now, now],
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


def _update_cycle_state(
    workspace_root: Path,
    *,
    cycle_id: str,
    status: str | None = None,
    description: str | None = None,
    reason: str,
) -> None:
    workspace = require_workspace(workspace_root)
    with connect_workspace_database(workspace.database_path) as connection:
        workspace_id = fetch_system_state_value(connection, "default_workspace") or "default"
        row = connection.execute(
            """
            SELECT id, type, start_date, end_date, status, description, created_by, created_at
            FROM cycles
            WHERE id = ?
            """,
            [cycle_id],
        ).fetchone()
        if row is None:
            raise WorkspaceBootstrapError(f"Cycle not found: {cycle_id}")

        old_state = {
            "id": str(row[0]),
            "type": str(row[1]),
            "start_date": str(row[2]),
            "end_date": None if row[3] is None else str(row[3]),
            "status": str(row[4]),
            "description": None if row[5] is None else str(row[5]),
            "created_by": str(row[6]),
            "created_at": str(row[7]),
        }
        new_status = status or old_state["status"]
        new_description = description if description is not None else old_state["description"]
        if new_status == old_state["status"] and new_description == old_state["description"]:
            return

        timestamp = utc_now()
        connection.execute(
            """
            UPDATE cycles
            SET status = ?, description = ?, modified_by = ?, modified_at = ?, id_cli = ?
            WHERE id = ?
            """,
            [new_status, new_description, "user", timestamp, "seed-rich", cycle_id],
        )
        new_state = {
            **old_state,
            "status": new_status,
            "description": new_description,
            "modified_by": "user",
            "modified_at": timestamp,
            "id_cli": "seed-rich",
        }
        _write_audit_row(
            connection,
            action="update",
            entity_type="cycle",
            entity_id=cycle_id,
            old_state=old_state,
            new_state=new_state,
            reason=reason,
            workspace_id=workspace_id,
        )


def _update_activity_details(
    workspace_root: Path,
    *,
    activity_id: str,
    priority: int,
    activity_type: str | None,
    description: str | None,
    reason: str,
) -> None:
    workspace = require_workspace(workspace_root)
    with connect_workspace_database(workspace.database_path) as connection:
        workspace_id = fetch_system_state_value(connection, "default_workspace") or "default"
        row = connection.execute(
            """
            SELECT id, title, cycle_id, status, priority, type, description, created_by, created_at
            FROM activities
            WHERE id = ?
            """,
            [activity_id],
        ).fetchone()
        if row is None:
            raise WorkspaceBootstrapError(f"Activity not found: {activity_id}")

        old_state = {
            "id": str(row[0]),
            "title": str(row[1]),
            "cycle_id": str(row[2]),
            "status": str(row[3]),
            "priority": int(row[4]),
            "type": None if row[5] is None else str(row[5]),
            "description": None if row[6] is None else str(row[6]),
            "created_by": str(row[7]),
            "created_at": str(row[8]),
        }
        if (
            old_state["priority"] == priority
            and old_state["type"] == activity_type
            and old_state["description"] == description
        ):
            return

        timestamp = utc_now()
        connection.execute(
            """
            UPDATE activities
            SET priority = ?, type = ?, description = ?, modified_by = ?, modified_at = ?, id_cli = ?
            WHERE id = ?
            """,
            [priority, activity_type, description, "user", timestamp, "seed-rich", activity_id],
        )
        new_state = {
            **old_state,
            "priority": priority,
            "type": activity_type,
            "description": description,
            "modified_by": "user",
            "modified_at": timestamp,
            "id_cli": "seed-rich",
        }
        _write_audit_row(
            connection,
            action="update",
            entity_type="activity",
            entity_id=activity_id,
            old_state=old_state,
            new_state=new_state,
            reason=reason,
            workspace_id=workspace_id,
        )


def _write_audit_row(
    connection,
    *,
    action: str,
    entity_type: str,
    entity_id: str,
    old_state: dict[str, object] | None,
    new_state: dict[str, object] | None,
    reason: str,
    workspace_id: str,
) -> None:
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
            action,
            entity_type,
            entity_id,
            None if old_state is None else json.dumps(old_state, ensure_ascii=True),
            None if new_state is None else json.dumps(new_state, ensure_ascii=True),
            "user",
            reason,
            utc_now(),
            workspace_id,
            "seed-rich",
        ],
    )


def _count_rows(connection, table: str) -> int:
    row = connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
    return 0 if row is None else int(row[0])


def _write_document_content(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")
