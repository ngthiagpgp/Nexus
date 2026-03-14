from __future__ import annotations

import os
from dataclasses import asdict
from pathlib import Path
from typing import Any

from fastapi import Body, FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse

from nexus.activities import ActivityRecord, get_activity, list_activities, update_activity_status
from nexus.cockpit import render_cockpit_page
from nexus.cycles import CycleRecord, get_cycle, list_cycles
from nexus.documents import DocumentInspection, inspect_document, list_documents
from nexus.entities import EntityRecord, get_entity, list_entities
from nexus.relations import RelationRecord, list_relations
from nexus.workspace import WorkspaceBootstrapError, inspect_workspace

API_PREFIX = "/api"


class NexusApiException(Exception):
    def __init__(self, *, status_code: int, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.message = message


def create_app(*, workspace_root: Path | None = None) -> FastAPI:
    app = FastAPI(
        title="Nexus MVP API",
        version="0.1.0",
        docs_url=None,
        redoc_url=None,
    )

    def resolve_workspace_root() -> Path:
        if workspace_root is not None:
            return workspace_root
        configured_root = os.getenv("NEXUS_WORKSPACE")
        if configured_root:
            return Path(configured_root).expanduser().resolve()
        return Path.cwd()

    @app.exception_handler(NexusApiException)
    async def handle_api_exception(
        request: Request, exc: NexusApiException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"status": "error", "message": exc.message},
        )

    @app.get("/", response_class=HTMLResponse)
    def cockpit() -> str:
        return render_cockpit_page()

    @app.get(f"{API_PREFIX}/health")
    def health() -> dict[str, object]:
        root = resolve_workspace_root()
        return {
            "status": "ok",
            "data": {
                "service": "nexus-api",
                "workspace_root": str(root),
            },
        }

    @app.get(f"{API_PREFIX}/system/status")
    def workspace_status() -> dict[str, object]:
        status = inspect_workspace(resolve_workspace_root())
        counts = status.resource_counts
        activity_summary = status.activity_summary
        return {
            "status": "ok",
            "data": {
                "workspace_root": str(status.workspace_root),
                "is_workspace": status.is_workspace,
                "schema_version": status.schema_version,
                "workspace_name": status.workspace_name,
                "initialized_at": status.initialized_at,
                "paths": {
                    "marker_dir": str(status.marker_dir),
                    "config_path": str(status.config_path),
                    "database_path": str(status.database_path),
                    "documents_dir": str(status.documents_dir),
                    "backups_dir": str(status.backups_dir),
                },
                "db_present": status.database_path.exists(),
                "missing_paths": [str(path) for path in status.missing_paths],
                "notes": list(status.notes),
                "counts": None
                if counts is None
                else {
                    "entities": counts.entities,
                    "documents": counts.documents,
                    "draft_documents": counts.draft_documents,
                    "approved_documents": counts.approved_documents,
                    "archived_documents": counts.archived_documents,
                    "relations": counts.relations,
                    "cycles": counts.cycles,
                    "active_cycles": counts.active_cycles,
                    "completed_cycles": counts.completed_cycles,
                    "archived_cycles": counts.archived_cycles,
                    "activities": counts.activities,
                },
                "activity_summary": None
                if activity_summary is None
                else {
                    "pending": activity_summary.pending,
                    "in_progress": activity_summary.in_progress,
                    "completed": activity_summary.completed,
                    "blocked": activity_summary.blocked,
                },
            },
        }

    @app.get(f"{API_PREFIX}/entities")
    def entity_list(
        entity_type: str | None = Query(None, alias="type")
    ) -> dict[str, object]:
        records = api_call(
            lambda: list_entities(resolve_workspace_root(), entity_type=entity_type)
        )
        return {"status": "ok", "data": [serialize_entity(record) for record in records]}

    @app.get(f"{API_PREFIX}/entities/{{entity_id}}")
    def entity_read(entity_id: str) -> dict[str, object]:
        record = api_call(lambda: get_entity(resolve_workspace_root(), entity_id=entity_id))
        return {"status": "ok", "data": serialize_entity(record)}

    @app.get(f"{API_PREFIX}/documents")
    def document_list(
        document_type: str | None = Query(None, alias="type"),
        status: str | None = Query(None),
        cycle_id: str | None = Query(None),
    ) -> dict[str, object]:
        records = api_call(
            lambda: list_documents(
                resolve_workspace_root(),
                document_type=document_type,
                status=status,
                cycle_id=cycle_id,
            )
        )
        return {"status": "ok", "data": [serialize_document_list_item(record) for record in records]}

    @app.get(f"{API_PREFIX}/documents/{{document_id}}")
    def document_read(document_id: str) -> dict[str, object]:
        inspection = api_call(lambda: inspect_document(resolve_workspace_root(), selector=document_id))
        return {"status": "ok", "data": serialize_document_inspection(inspection)}

    @app.get(f"{API_PREFIX}/relations")
    def relation_list(
        entity_a: str | None = Query(None),
        entity_b: str | None = Query(None),
        relation_type: str | None = Query(None, alias="type"),
    ) -> dict[str, object]:
        records = api_call(
            lambda: list_relations(
                resolve_workspace_root(),
                from_entity=entity_a,
                to_entity=entity_b,
                relation_type=relation_type,
            )
        )
        return {"status": "ok", "data": [serialize_relation(record) for record in records]}

    @app.get(f"{API_PREFIX}/cycles")
    def cycle_list(
        cycle_type: str | None = Query(None, alias="type"),
        status: str | None = Query(None),
    ) -> dict[str, object]:
        records = api_call(
            lambda: list_cycles(resolve_workspace_root(), cycle_type=cycle_type, status=status)
        )
        return {"status": "ok", "data": [serialize_cycle(record) for record in records]}

    @app.get(f"{API_PREFIX}/cycles/{{cycle_id}}")
    def cycle_read(cycle_id: str) -> dict[str, object]:
        record = api_call(lambda: get_cycle(resolve_workspace_root(), cycle_id=cycle_id))
        return {"status": "ok", "data": serialize_cycle(record)}

    @app.get(f"{API_PREFIX}/activities")
    def activity_list(
        cycle_id: str | None = Query(None),
        status: str | None = Query(None),
    ) -> dict[str, object]:
        records = api_call(
            lambda: list_activities(resolve_workspace_root(), cycle_id=cycle_id, status=status)
        )
        return {"status": "ok", "data": [serialize_activity(record) for record in records]}

    @app.get(f"{API_PREFIX}/activities/{{activity_id}}")
    def activity_read(activity_id: str) -> dict[str, object]:
        record = api_call(lambda: get_activity(resolve_workspace_root(), activity_id=activity_id))
        return {"status": "ok", "data": serialize_activity(record)}

    @app.patch(f"{API_PREFIX}/activities/{{activity_id}}")
    def activity_status_update(
        activity_id: str,
        payload: dict[str, object] = Body(...),
    ) -> dict[str, object]:
        raw_status = payload.get("status")
        if not isinstance(raw_status, str) or not raw_status.strip():
            raise NexusApiException(
                status_code=400,
                message="Field 'status' is required for activity updates.",
            )
        record = api_call(
            lambda: update_activity_status(
                resolve_workspace_root(),
                activity_id=activity_id,
                status=raw_status,
                actor="user",
                reason="API activity status update",
                cli_id="api",
            )
        )
        return {"status": "ok", "data": serialize_activity(record)}

    return app


def api_call(operation):
    try:
        return operation()
    except WorkspaceBootstrapError as exc:
        raise to_http_exception(exc) from exc


def to_http_exception(exc: WorkspaceBootstrapError) -> NexusApiException:
    message = str(exc)
    if "not a Nexus workspace" in message or "backing file is missing" in message:
        status_code = 409
    elif "not found" in message:
        status_code = 404
    else:
        status_code = 400
    return NexusApiException(status_code=status_code, message=message)


def serialize_entity(record: EntityRecord) -> dict[str, Any]:
    return asdict(record)


def serialize_document_list_item(record) -> dict[str, Any]:
    return asdict(record)


def serialize_document_inspection(inspection: DocumentInspection) -> dict[str, Any]:
    data = asdict(inspection.record)
    data.update(
        {
            "absolute_path": str(inspection.absolute_path),
            "content_preview": inspection.content_preview,
            "content": inspection.content,
            "modified_at": inspection.modified_at,
            "approved_at": inspection.approved_at,
        }
    )
    return data


def serialize_relation(record: RelationRecord) -> dict[str, Any]:
    return asdict(record)


def serialize_cycle(record: CycleRecord) -> dict[str, Any]:
    return asdict(record)


def serialize_activity(record: ActivityRecord) -> dict[str, Any]:
    return asdict(record)


app = create_app()
