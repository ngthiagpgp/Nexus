from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
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
class DocumentRecord:
    id: str
    title: str
    type: str
    cycle_id: str | None
    status: str
    path: str
    content_hash: str
    version: str
    created_at: str
    created_by: str


def create_document(
    workspace_root: Path,
    *,
    document_type: str,
    title: str | None = None,
    cycle_id: str | None = None,
) -> DocumentRecord:
    workspace = require_workspace(workspace_root)
    normalized_type = validate_required_text("Document type", document_type).lower()
    normalized_title = normalize_optional_text(title) or default_title_for_type(normalized_type)
    normalized_cycle_id = normalize_optional_text(cycle_id)
    timestamp = utc_now()
    document_id = str(uuid4())
    cli_id = "local"
    created_by = "user"

    relative_path = build_document_relative_path(normalized_type, normalized_title)
    absolute_path = workspace.workspace_root / relative_path
    absolute_path.parent.mkdir(parents=True, exist_ok=True)

    if absolute_path.exists():
        raise WorkspaceBootstrapError(
            f"Document file already exists: {absolute_path}. Use a different title or type."
        )

    content = build_initial_markdown(normalized_title)
    content_hash = compute_content_hash(content)
    changelog = json.dumps(
        [{"version": "1.0", "changed": "Initial draft", "timestamp": timestamp}],
        ensure_ascii=True,
    )
    absolute_path.write_text(content, encoding="utf-8")

    with connect_workspace_database(workspace.database_path) as connection:
        workspace_id = fetch_system_state_value(connection, "default_workspace") or "default"
        connection.execute(
            """
            INSERT INTO documents (
                id,
                title,
                type,
                cycle_id,
                status,
                path,
                content_hash,
                version,
                approved_at,
                created_by,
                created_at,
                modified_by,
                modified_at,
                id_workspace,
                id_cli,
                changelog
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                document_id,
                normalized_title,
                normalized_type,
                normalized_cycle_id,
                "draft",
                relative_path.as_posix(),
                content_hash,
                "1.0",
                None,
                created_by,
                timestamp,
                created_by,
                timestamp,
                workspace_id,
                cli_id,
                changelog,
            ],
        )

        new_state = {
            "id": document_id,
            "title": normalized_title,
            "type": normalized_type,
            "cycle_id": normalized_cycle_id,
            "status": "draft",
            "path": relative_path.as_posix(),
            "content_hash": content_hash,
            "version": "1.0",
            "created_by": created_by,
            "created_at": timestamp,
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
                "document",
                document_id,
                None,
                json.dumps(new_state, ensure_ascii=True),
                created_by,
                "CLI document create",
                timestamp,
                workspace_id,
                cli_id,
            ],
        )

    return DocumentRecord(
        id=document_id,
        title=normalized_title,
        type=normalized_type,
        cycle_id=normalized_cycle_id,
        status="draft",
        path=relative_path.as_posix(),
        content_hash=content_hash,
        version="1.0",
        created_at=timestamp,
        created_by=created_by,
    )


def list_documents(
    workspace_root: Path,
    *,
    document_type: str | None = None,
    status: str | None = None,
) -> list[DocumentRecord]:
    workspace = require_workspace(workspace_root)
    query = """
        SELECT
            id,
            title,
            type,
            cycle_id,
            status,
            path,
            content_hash,
            version,
            created_at,
            created_by
        FROM documents
    """
    clauses: list[str] = []
    params: list[str] = []

    normalized_type = normalize_optional_text(document_type)
    normalized_status = normalize_optional_text(status)

    if normalized_type:
        clauses.append("type = ?")
        params.append(normalized_type.lower())

    if normalized_status:
        clauses.append("status = ?")
        params.append(normalized_status.lower())

    if clauses:
        query += " WHERE " + " AND ".join(clauses)

    query += " ORDER BY created_at DESC, title ASC"

    with connect_workspace_database(workspace.database_path, read_only=True) as connection:
        rows = connection.execute(query, params).fetchall()

    return [
        DocumentRecord(
            id=row[0],
            title=row[1],
            type=row[2],
            cycle_id=row[3],
            status=row[4],
            path=row[5],
            content_hash=row[6],
            version=row[7],
            created_at=str(row[8]),
            created_by=row[9],
        )
        for row in rows
    ]


def build_document_relative_path(document_type: str, title: str) -> Path:
    directory = Path("documents") / document_type
    filename = document_filename(document_type, title)
    return directory / f"{filename}.md"


def document_filename(document_type: str, title: str) -> str:
    if document_type == "daily":
        match = re.search(r"\d{4}-\d{2}-\d{2}", title)
        if match:
            return match.group(0)
    if document_type == "weekly":
        match = re.search(r"\d{4}-W\d{2}", title)
        if match:
            return match.group(0)
    if document_type == "monthly":
        match = re.search(r"\d{4}-\d{2}", title)
        if match:
            return match.group(0)

    slug = slugify(title)
    if not slug:
        raise WorkspaceBootstrapError("Document title produced an empty filename.")
    return slug


def default_title_for_type(document_type: str) -> str:
    now = datetime.now(timezone.utc)
    if document_type == "daily":
        return f"Daily {now.date().isoformat()}"
    if document_type == "weekly":
        iso_year, iso_week, _ = now.isocalendar()
        return f"Weekly {iso_year}-W{iso_week:02d}"
    if document_type == "monthly":
        return f"Monthly {now.strftime('%Y-%m')}"
    if document_type == "report":
        return f"Report {now.strftime('%Y-%m-%d')}"
    if document_type == "note":
        return f"Note {now.strftime('%Y-%m-%d')}"
    return f"{document_type.title()} {now.strftime('%Y-%m-%d')}"


def build_initial_markdown(title: str) -> str:
    return f"# {title}\n\n"


def compute_content_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def slugify(value: str) -> str:
    lowered = value.lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")
    return normalized
