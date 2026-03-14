# NEXUS Document Status Transitions Note

## Purpose

Clarify the first controlled write slice for document lifecycle updates without rewriting the main schema or broader specs.

## Context

The current schema defines the core document statuses:

- `draft`
- `approved`
- `archived`

The schema and current bootstrap do not define a richer reopening or review workflow.

## Conservative bootstrap rule

For the first controlled document lifecycle flow, Nexus applies an explicit and narrow transition map in code:

- `draft` -> `approved`
- `approved` -> `archived`
- `archived` -> no further transitions

Same-status updates are treated as idempotent no-ops.

## Additional handling

- Document status updates require the Markdown backing file to exist.
- Entering `approved` sets `approved_at`.
- Each lifecycle transition increments the document major version conservatively.

## Rationale

- Keeps document lifecycle forward-only and auditable.
- Preserves the filesystem plus DuckDB split already defined in the specs.
- Avoids inventing reopening semantics before document editing and review flows exist.

## Non-goals

- full document editing
- review comments or multi-step approval
- automatic git commits on approval
- reopening archived documents
