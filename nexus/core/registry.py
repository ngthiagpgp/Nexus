from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TypeCapabilities:
    type_name: str
    category: str
    has_lifecycle: bool
    has_integrity: bool
    has_status_transitions: bool
    read_heavy: bool


_TYPE_CAPABILITIES: dict[str, TypeCapabilities] = {
    "entity": TypeCapabilities(
        type_name="entity",
        category="domain_primitive",
        has_lifecycle=False,
        has_integrity=False,
        has_status_transitions=False,
        read_heavy=False,
    ),
    "relation": TypeCapabilities(
        type_name="relation",
        category="domain_primitive",
        has_lifecycle=False,
        has_integrity=False,
        has_status_transitions=False,
        read_heavy=True,
    ),
    "document": TypeCapabilities(
        type_name="document",
        category="domain_primitive",
        has_lifecycle=True,
        has_integrity=True,
        has_status_transitions=True,
        read_heavy=True,
    ),
    "cycle": TypeCapabilities(
        type_name="cycle",
        category="domain_primitive",
        has_lifecycle=True,
        has_integrity=False,
        has_status_transitions=False,
        read_heavy=True,
    ),
    "activity": TypeCapabilities(
        type_name="activity",
        category="domain_primitive",
        has_lifecycle=False,
        has_integrity=False,
        has_status_transitions=True,
        read_heavy=True,
    ),
}


def get_type_capabilities(type_name: str) -> TypeCapabilities:
    normalized = type_name.strip().lower()
    return _TYPE_CAPABILITIES[normalized]


def list_registered_types() -> tuple[TypeCapabilities, ...]:
    return tuple(_TYPE_CAPABILITIES[key] for key in sorted(_TYPE_CAPABILITIES))
