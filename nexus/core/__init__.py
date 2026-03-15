"""Platform core for the Nexus local-first substrate.

This package holds stable backend concerns that are not presentation-specific:

- workspace contract and bootstrap
- aggregated read models
- lightweight type/capability metadata
"""

from nexus.core.read_models import (
    WorkspaceActivitySummary,
    WorkspaceResourceCounts,
    WorkspaceStatusReadModel,
    inspect_workspace_read_model,
)
from nexus.core.mutations import (
    MutationContext,
    MutationResult,
    build_mutation_context,
    ensure_type_supports_integrity,
    ensure_type_supports_lifecycle,
    ensure_type_supports_status_transitions,
    validate_status_transition,
    write_mutation_audit,
)
from nexus.core.registry import (
    TypeCapabilities,
    get_type_capabilities,
    list_registered_types,
)
from nexus.core.workspace import (
    SCHEMA_COMPATIBILITY_NOTE,
    WorkspaceBootstrapError,
    WorkspaceInitResult,
    WorkspaceStatus,
    connect_workspace_database,
    ensure_workspace_system_state,
    execute_sql_script,
    fetch_config_value,
    fetch_system_state_value,
    initialize_workspace,
    inspect_workspace,
    load_schema_sql,
    normalize_schema_sql,
    require_workspace,
    split_sql_statements,
    utc_now,
)
from nexus.core.workspace_contract import (
    BACKUPS_DIRNAME,
    DATABASE_FILENAME,
    DOCUMENT_CYCLE_DIRS,
    DOCUMENTS_DIRNAME,
    WORKSPACE_CONFIG_FILENAME,
    WORKSPACE_MARKER_DIRNAME,
    WorkspaceLayout,
    workspace_layout,
)

__all__ = [
    "BACKUPS_DIRNAME",
    "DATABASE_FILENAME",
    "DOCUMENTS_DIRNAME",
    "DOCUMENT_CYCLE_DIRS",
    "MutationContext",
    "MutationResult",
    "SCHEMA_COMPATIBILITY_NOTE",
    "TypeCapabilities",
    "WORKSPACE_CONFIG_FILENAME",
    "WORKSPACE_MARKER_DIRNAME",
    "WorkspaceActivitySummary",
    "WorkspaceBootstrapError",
    "WorkspaceInitResult",
    "WorkspaceLayout",
    "WorkspaceResourceCounts",
    "WorkspaceStatus",
    "WorkspaceStatusReadModel",
    "connect_workspace_database",
    "ensure_workspace_system_state",
    "ensure_type_supports_integrity",
    "ensure_type_supports_lifecycle",
    "ensure_type_supports_status_transitions",
    "execute_sql_script",
    "fetch_config_value",
    "fetch_system_state_value",
    "build_mutation_context",
    "get_type_capabilities",
    "initialize_workspace",
    "inspect_workspace",
    "inspect_workspace_read_model",
    "list_registered_types",
    "load_schema_sql",
    "normalize_schema_sql",
    "require_workspace",
    "split_sql_statements",
    "utc_now",
    "validate_status_transition",
    "write_mutation_audit",
    "workspace_layout",
]
