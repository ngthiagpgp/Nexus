# NEXUS Activity Status Transitions Note

## Purpose

Clarify the first controlled write slice for activity status updates without rewriting the main schema or broader specs.

## Context

The current schema defines the allowed activity statuses:

- `pending`
- `in_progress`
- `completed`
- `blocked`

The schema does not define explicit transition rules between those states.

## Conservative bootstrap rule

For the first controlled write flow, Nexus applies an explicit and narrow transition map in code:

- `pending` -> `in_progress`, `completed`, `blocked`
- `in_progress` -> `pending`, `completed`, `blocked`
- `blocked` -> `pending`, `in_progress`, `completed`
- `completed` -> `pending`, `in_progress`

Same-status updates are treated as idempotent no-ops.

## Rationale

- Keeps the write surface narrow and auditable.
- Supports basic operational supervision in CLI, API, and cockpit.
- Avoids inventing a richer workflow engine before the control and audit substrate is more mature.

## Non-goals

- full activity editing
- workflow automation
- assignment, reminders, or scheduling semantics
- hidden status mutation rules
