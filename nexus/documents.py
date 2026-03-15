from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from nexus.core.mutations import (
    MutationResult,
    build_mutation_context,
    ensure_type_supports_integrity,
    ensure_type_supports_lifecycle,
    validate_status_transition,
    write_mutation_audit,
)
from nexus.entities import normalize_optional_text, validate_required_text
from nexus.core.workspace import (
    WorkspaceBootstrapError,
    connect_workspace_database,
    fetch_system_state_value,
    require_workspace,
    utc_now,
)

ALLOWED_DOCUMENT_STATUSES = ("draft", "approved", "archived")
ALLOWED_DOCUMENT_STATUS_TRANSITIONS = {
    "draft": {"approved"},
    "approved": {"archived"},
    "archived": set(),
}


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
    modified_at: str
    approved_at: str | None


@dataclass(frozen=True)
class DocumentInspection:
    record: DocumentRecord
    absolute_path: Path
    content: str
    content_preview: str
    modified_at: str
    approved_at: str | None


@dataclass(frozen=True)
class DocumentIntegrityResult:
    document_id: str
    title: str
    type: str
    status: str
    path: str
    expected_path: str
    absolute_path: str
    expected_path_exists: bool
    db_record_exists: bool
    backing_file_exists: bool
    path_matches_expected: bool
    content_hash_matches: bool | None
    integrity_state: str
    issues: list[str]
    recorded_content_hash: str
    current_content_hash: str | None


@dataclass(frozen=True)
class DocumentReconciliationResult:
    record: DocumentRecord
    integrity: DocumentIntegrityResult
    reconciled_fields: list[str]


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
        modified_at=timestamp,
        approved_at=None,
    )


def list_documents(
    workspace_root: Path,
    *,
    document_type: str | None = None,
    status: str | None = None,
    cycle_id: str | None = None,
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
            created_by,
            modified_at,
            approved_at
        FROM documents
    """
    clauses: list[str] = []
    params: list[str] = []

    normalized_type = normalize_optional_text(document_type)
    normalized_status = normalize_optional_text(status)
    normalized_cycle_id = normalize_optional_text(cycle_id)

    if normalized_type:
        clauses.append("type = ?")
        params.append(normalized_type.lower())

    if normalized_status:
        clauses.append("status = ?")
        params.append(normalized_status.lower())

    if normalized_cycle_id:
        clauses.append("cycle_id = ?")
        params.append(normalized_cycle_id)

    if clauses:
        query += " WHERE " + " AND ".join(clauses)

    query += " ORDER BY created_at DESC, title ASC"

    with connect_workspace_database(workspace.database_path, read_only=True) as connection:
        rows = connection.execute(query, params).fetchall()

    return [
        document_record_from_row(row)
        for row in rows
    ]


def inspect_document(workspace_root: Path, *, selector: str) -> DocumentInspection:
    workspace = require_workspace(workspace_root)
    normalized_selector = validate_required_text("Document selector", selector)

    with connect_workspace_database(workspace.database_path, read_only=True) as connection:
        row = fetch_document_row(
            connection,
            normalized_selector,
            allow_title_lookup=True,
        )

    record = document_record_from_row(row)
    absolute_path = workspace.workspace_root / record.path
    if not absolute_path.exists():
        raise WorkspaceBootstrapError(
            f"Document backing file is missing: {absolute_path}"
        )

    try:
        content = absolute_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise WorkspaceBootstrapError(
            f"Failed to read document backing file: {absolute_path}: {exc}"
        ) from exc

    return DocumentInspection(
        record=record,
        absolute_path=absolute_path,
        content=content,
        content_preview=build_content_preview(content),
        modified_at=record.modified_at,
        approved_at=record.approved_at,
    )


def verify_document(
    workspace_root: Path,
    *,
    selector: str,
    allow_title_lookup: bool = True,
) -> DocumentIntegrityResult:
    workspace = require_workspace(workspace_root)
    normalized_selector = validate_required_text("Document selector", selector)

    with connect_workspace_database(workspace.database_path, read_only=True) as connection:
        row = fetch_document_row(
            connection,
            normalized_selector,
            allow_title_lookup=allow_title_lookup,
        )

    return build_document_integrity_result(
        document_record_from_row(row),
        workspace_root=workspace.workspace_root,
    )


def verify_documents(workspace_root: Path) -> list[DocumentIntegrityResult]:
    workspace = require_workspace(workspace_root)
    records = list_documents(workspace.workspace_root)
    return [
        build_document_integrity_result(record, workspace_root=workspace.workspace_root)
        for record in records
    ]


def reconcile_document(
    workspace_root: Path,
    *,
    selector: str,
    actor: str = "user",
    reason: str = "Document reconcile",
    cli_id: str = "local",
    allow_title_lookup: bool = True,
) -> DocumentReconciliationResult:
    return reconcile_document_mutation(
        workspace_root,
        selector=selector,
        actor=actor,
        reason=reason,
        cli_id=cli_id,
        allow_title_lookup=allow_title_lookup,
    ).payload


def reconcile_document_mutation(
    workspace_root: Path,
    *,
    selector: str,
    actor: str = "user",
    reason: str = "Document reconcile",
    cli_id: str = "local",
    allow_title_lookup: bool = True,
) -> MutationResult[DocumentReconciliationResult]:
    workspace = require_workspace(workspace_root)
    ensure_type_supports_integrity("document")
    normalized_selector = validate_required_text("Document selector", selector)

    with connect_workspace_database(workspace.database_path) as connection:
        mutation = build_mutation_context(
            connection,
            entity_type="document",
            actor=actor,
            reason=reason,
            cli_id=cli_id,
        )
        old_row = fetch_document_row(
            connection,
            normalized_selector,
            allow_title_lookup=allow_title_lookup,
        )
        old_record = document_record_from_row(old_row)
        actual_path = workspace.workspace_root / old_record.path
        expected_relative_path = build_document_relative_path(old_record.type, old_record.title)
        expected_path = workspace.workspace_root / expected_relative_path

        if not actual_path.exists():
            raise WorkspaceBootstrapError(
                f"Document backing file is missing: {actual_path}"
            )

        if (
            old_record.path != expected_relative_path.as_posix()
            and expected_path.exists()
            and actual_path.resolve() != expected_path.resolve()
        ):
            raise WorkspaceBootstrapError(
                "Document reconciliation is ambiguous because both the stored path and the "
                f"canonical path exist: {actual_path} | {expected_path}. Resolve manually."
            )

        try:
            current_content = actual_path.read_text(encoding="utf-8")
        except OSError as exc:
            raise WorkspaceBootstrapError(
                f"Failed to read document backing file: {actual_path}: {exc}"
            ) from exc

        reconciled_fields: list[str] = []
        updates: dict[str, object] = {
            "modified_by": mutation.actor,
            "modified_at": mutation.timestamp,
            "id_cli": mutation.cli_id,
        }
        current_content_hash = compute_content_hash(current_content)
        if current_content_hash != old_record.content_hash:
            updates["content_hash"] = current_content_hash
            reconciled_fields.append("content_hash")

        if (
            old_record.path != expected_relative_path.as_posix()
            and expected_path.exists()
            and actual_path.resolve() == expected_path.resolve()
        ):
            updates["path"] = expected_relative_path.as_posix()
            reconciled_fields.append("path")

        if not reconciled_fields:
            if old_record.path != expected_relative_path.as_posix():
                raise WorkspaceBootstrapError(
                    "Document reconciliation cannot safely update the stored path because the "
                    f"canonical file does not exist yet: {expected_path}"
                )
            integrity = build_document_integrity_result(
                old_record,
                workspace_root=workspace.workspace_root,
            )
            return MutationResult(
                entity_type="document",
                entity_id=old_record.id,
                action="reconcile",
                payload=DocumentReconciliationResult(
                    record=old_record,
                    integrity=integrity,
                    reconciled_fields=[],
                ),
            )

        set_clause = ", ".join(f"{column} = ?" for column in updates)
        params = list(updates.values()) + [old_record.id]
        connection.execute(
            f"UPDATE documents SET {set_clause} WHERE id = ?",
            params,
        )
        new_row = fetch_document_row(connection, old_record.id, allow_title_lookup=False)
        new_record = document_record_from_row(new_row)

        write_mutation_audit(
            connection,
            context=mutation,
            action="reconcile",
            entity_id=old_record.id,
            old_state=document_state_payload(old_record),
            new_state=document_state_payload(new_record),
        )

    integrity = build_document_integrity_result(
        new_record,
        workspace_root=workspace.workspace_root,
    )
    return MutationResult(
        entity_type="document",
        entity_id=new_record.id,
        action="reconcile",
        payload=DocumentReconciliationResult(
            record=new_record,
            integrity=integrity,
            reconciled_fields=reconciled_fields,
        ),
    )


def update_document_status(
    workspace_root: Path,
    *,
    selector: str,
    status: str,
    actor: str = "user",
    reason: str = "Document status update",
    cli_id: str = "local",
    allow_title_lookup: bool = True,
) -> DocumentRecord:
    return update_document_status_mutation(
        workspace_root,
        selector=selector,
        status=status,
        actor=actor,
        reason=reason,
        cli_id=cli_id,
        allow_title_lookup=allow_title_lookup,
    ).payload


def update_document_status_mutation(
    workspace_root: Path,
    *,
    selector: str,
    status: str,
    actor: str = "user",
    reason: str = "Document status update",
    cli_id: str = "local",
    allow_title_lookup: bool = True,
) -> MutationResult[DocumentRecord]:
    workspace = require_workspace(workspace_root)
    ensure_type_supports_lifecycle("document")
    normalized_selector = validate_required_text("Document selector", selector)
    normalized_status = validate_document_status(status)

    with connect_workspace_database(workspace.database_path) as connection:
        mutation = build_mutation_context(
            connection,
            entity_type="document",
            actor=actor,
            reason=reason,
            cli_id=cli_id,
        )
        old_row = fetch_document_row(
            connection,
            normalized_selector,
            allow_title_lookup=allow_title_lookup,
        )
        old_record = document_record_from_row(old_row)
        absolute_path = workspace.workspace_root / old_record.path
        if not absolute_path.exists():
            raise WorkspaceBootstrapError(
                f"Document backing file is missing: {absolute_path}"
            )

        if old_record.status == normalized_status:
            return MutationResult(
                entity_type="document",
                entity_id=old_record.id,
                action="update",
                payload=old_record,
            )

        validate_status_transition(
            entity_type="document",
            current_status=old_record.status,
            target_status=normalized_status,
            allowed_transitions=ALLOWED_DOCUMENT_STATUS_TRANSITIONS,
        )

        approved_at = old_record.approved_at
        if normalized_status == "approved":
            approved_at = mutation.timestamp

        connection.execute(
            """
            UPDATE documents
            SET status = ?, version = ?, approved_at = ?, modified_by = ?, modified_at = ?, id_cli = ?
            WHERE id = ?
            """,
            [
                normalized_status,
                bump_major_version(old_record.version),
                approved_at,
                mutation.actor,
                mutation.timestamp,
                mutation.cli_id,
                old_record.id,
            ],
        )

        new_row = fetch_document_row(connection, old_record.id, allow_title_lookup=False)
        new_record = document_record_from_row(new_row)

        write_mutation_audit(
            connection,
            context=mutation,
            action="update",
            entity_id=old_record.id,
            old_state=document_state_payload(old_record),
            new_state=document_state_payload(new_record),
        )

    return MutationResult(
        entity_type="document",
        entity_id=new_record.id,
        action="update",
        payload=new_record,
    )


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


def build_content_preview(content: str, *, max_lines: int = 8, max_chars: int = 400) -> str:
    stripped = content.strip()
    if not stripped:
        return "(empty document)"

    lines = stripped.splitlines()[:max_lines]
    preview = "\n".join(lines).strip()
    if len(preview) > max_chars:
        return preview[: max_chars - 3].rstrip() + "..."
    if len(stripped) > len(preview):
        return preview.rstrip() + "\n..."
    return preview


def compute_content_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def slugify(value: str) -> str:
    lowered = value.lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")
    return normalized


def bump_major_version(version: str) -> str:
    raw_version = validate_required_text("Document version", version)
    major_part, _, _ = raw_version.partition(".")
    try:
        major_value = int(major_part)
    except ValueError as exc:
        raise WorkspaceBootstrapError(
            f"Document version is not a supported major.minor value: {raw_version}"
        ) from exc
    return f"{major_value + 1}.0"


def build_document_integrity_result(
    record: DocumentRecord,
    *,
    workspace_root: Path,
) -> DocumentIntegrityResult:
    expected_path = build_document_relative_path(record.type, record.title).as_posix()
    absolute_path = workspace_root / record.path
    expected_absolute_path = workspace_root / expected_path
    issues: list[str] = []
    backing_file_exists = absolute_path.exists()
    expected_path_exists = expected_absolute_path.exists()
    path_matches_expected = record.path == expected_path
    content_hash_matches: bool | None = None
    current_content_hash: str | None = None

    if not path_matches_expected:
        issues.append("path_mismatch")

    if not backing_file_exists:
        issues.append("missing_backing_file")
    else:
        try:
            content = absolute_path.read_text(encoding="utf-8")
        except OSError:
            issues.append("backing_file_unreadable")
        else:
            current_content_hash = compute_content_hash(content)
            content_hash_matches = current_content_hash == record.content_hash
            if not content_hash_matches:
                issues.append("content_hash_mismatch")

    integrity_state = classify_document_integrity_issues(issues)

    return DocumentIntegrityResult(
        document_id=record.id,
        title=record.title,
        type=record.type,
        status=record.status,
        path=record.path,
        expected_path=expected_path,
        absolute_path=str(absolute_path),
        expected_path_exists=expected_path_exists,
        db_record_exists=True,
        backing_file_exists=backing_file_exists,
        path_matches_expected=path_matches_expected,
        content_hash_matches=content_hash_matches,
        integrity_state=integrity_state,
        issues=issues,
        recorded_content_hash=record.content_hash,
        current_content_hash=current_content_hash,
    )


def classify_document_integrity_issues(issues: Sequence[str]) -> str:
    if not issues:
        return "ok"
    if any(
        issue in {"missing_backing_file", "backing_file_unreadable", "content_hash_mismatch"}
        for issue in issues
    ):
        return "error"
    return "warning"


def fetch_document_row(
    connection,
    selector: str,
    *,
    allow_title_lookup: bool,
) -> Sequence[object]:
    base_query = """
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
            created_by,
            modified_at,
            approved_at
        FROM documents
    """
    row = connection.execute(
        base_query + " WHERE id = ?",
        [selector],
    ).fetchone()
    if row is None and allow_title_lookup:
        title_rows = connection.execute(
            base_query + " WHERE title = ?",
            [selector],
        ).fetchall()
        if len(title_rows) > 1:
            raise WorkspaceBootstrapError(
                f"Document selector is ambiguous: {selector}. Use the document id."
            )
        row = title_rows[0] if title_rows else None
    if row is None:
        raise WorkspaceBootstrapError(f"Document not found: {selector}")
    return row


def validate_document_status(status: str) -> str:
    normalized_status = validate_required_text("Document status", status).lower()
    if normalized_status not in ALLOWED_DOCUMENT_STATUSES:
        allowed_display = ", ".join(ALLOWED_DOCUMENT_STATUSES)
        raise WorkspaceBootstrapError(
            f"Invalid document status: {normalized_status}. Allowed: {allowed_display}."
        )
    return normalized_status


def document_state_payload(record: DocumentRecord) -> dict[str, object]:
    return {
        "id": record.id,
        "title": record.title,
        "type": record.type,
        "cycle_id": record.cycle_id,
        "status": record.status,
        "path": record.path,
        "content_hash": record.content_hash,
        "version": record.version,
        "created_at": record.created_at,
        "created_by": record.created_by,
        "modified_at": record.modified_at,
        "approved_at": record.approved_at,
    }


def document_record_from_row(row: Sequence[object]) -> DocumentRecord:
    return DocumentRecord(
        id=str(row[0]),
        title=str(row[1]),
        type=str(row[2]),
        cycle_id=None if row[3] is None else str(row[3]),
        status=str(row[4]),
        path=str(row[5]),
        content_hash=str(row[6]),
        version=str(row[7]),
        created_at=str(row[8]),
        created_by=str(row[9]),
        modified_at=str(row[10]),
        approved_at=None if row[11] is None else str(row[11]),
    )
