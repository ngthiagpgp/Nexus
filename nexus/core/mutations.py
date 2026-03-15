from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Generic, TypeVar
from uuid import uuid4

from nexus.core.registry import get_type_capabilities
from nexus.core.workspace import WorkspaceBootstrapError, fetch_system_state_value, utc_now
from nexus.entities import validate_required_text

T = TypeVar("T")


@dataclass(frozen=True)
class MutationContext:
    entity_type: str
    actor: str
    reason: str
    cli_id: str
    timestamp: str
    workspace_id: str


@dataclass(frozen=True)
class MutationResult(Generic[T]):
    entity_type: str
    entity_id: str
    action: str
    payload: T


def build_mutation_context(
    connection,
    *,
    entity_type: str,
    actor: str,
    reason: str,
    cli_id: str,
) -> MutationContext:
    normalized_entity_type = validate_required_text("Entity type", entity_type).lower()
    normalized_actor = validate_required_text("Actor", actor)
    normalized_reason = validate_required_text("Reason", reason)
    normalized_cli_id = validate_required_text("CLI id", cli_id)
    workspace_id = fetch_system_state_value(connection, "default_workspace") or "default"
    return MutationContext(
        entity_type=normalized_entity_type,
        actor=normalized_actor,
        reason=normalized_reason,
        cli_id=normalized_cli_id,
        timestamp=utc_now(),
        workspace_id=workspace_id,
    )


def ensure_type_supports_status_transitions(entity_type: str) -> None:
    capabilities = get_type_capabilities(entity_type)
    if not capabilities.has_status_transitions:
        raise WorkspaceBootstrapError(
            f"Type does not support status transitions: {capabilities.type_name}"
        )


def ensure_type_supports_lifecycle(entity_type: str) -> None:
    capabilities = get_type_capabilities(entity_type)
    if not capabilities.has_lifecycle:
        raise WorkspaceBootstrapError(
            f"Type does not support lifecycle transitions: {capabilities.type_name}"
        )


def ensure_type_supports_integrity(entity_type: str) -> None:
    capabilities = get_type_capabilities(entity_type)
    if not capabilities.has_integrity:
        raise WorkspaceBootstrapError(
            f"Type does not support integrity or reconciliation: {capabilities.type_name}"
        )


def validate_status_transition(
    *,
    entity_type: str,
    current_status: str,
    target_status: str,
    allowed_transitions: dict[str, set[str]],
    empty_message: str = "no further transitions",
) -> None:
    ensure_type_supports_status_transitions(entity_type)
    allowed_statuses = allowed_transitions.get(current_status, set())
    if target_status not in allowed_statuses:
        allowed_display = ", ".join(sorted(allowed_statuses)) or empty_message
        raise WorkspaceBootstrapError(
            f"Invalid {entity_type} status transition: "
            f"{current_status} -> {target_status}. Allowed: {allowed_display}."
        )


def write_mutation_audit(
    connection,
    *,
    context: MutationContext,
    action: str,
    entity_id: str,
    old_state: dict[str, object] | None,
    new_state: dict[str, object],
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
            context.entity_type,
            entity_id,
            None if old_state is None else json.dumps(old_state, ensure_ascii=True),
            json.dumps(new_state, ensure_ascii=True),
            context.actor,
            context.reason,
            context.timestamp,
            context.workspace_id,
            context.cli_id,
        ],
    )
