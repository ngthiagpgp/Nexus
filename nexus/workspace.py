"""Compatibility shim for workspace imports.

The explicit platform-core implementation now lives under ``nexus.core``.
The legacy module path stays available to preserve the current MVP surface.
"""

from pathlib import Path

from nexus.core.read_models import (
    WorkspaceActivitySummary,
    WorkspaceResourceCounts,
    WorkspaceStatusReadModel,
    inspect_workspace_read_model,
)
from nexus.core.workspace import *  # noqa: F401,F403

WorkspaceStatus = WorkspaceStatusReadModel


def inspect_workspace(target: Path) -> WorkspaceStatusReadModel:
    return inspect_workspace_read_model(target)


__all__ = [
    "SCHEMA_COMPATIBILITY_NOTE",
    "SchemaBootstrapPayload",
    "WorkspaceActivitySummary",
    "WorkspaceBootstrapError",
    "WorkspaceInitResult",
    "WorkspaceResourceCounts",
    "WorkspaceStatus",
    "connect_workspace_database",
    "ensure_workspace_system_state",
    "execute_sql_script",
    "fetch_config_value",
    "fetch_system_state_value",
    "initialize_workspace",
    "inspect_workspace",
    "inspect_workspace_read_model",
    "load_schema_sql",
    "normalize_schema_sql",
    "require_workspace",
    "split_sql_statements",
    "utc_now",
]
