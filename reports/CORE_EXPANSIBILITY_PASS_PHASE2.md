# Core Expansibility Pass - Phase 2

## Purpose

Phase 2 does not add new product features.

Its goal is to make the current controlled write flows easier to extend and reason about by giving them a shared mutation contract.

The target was narrow:

- activity status update
- document lifecycle status update
- document reconciliation

## Mutation Contract Introduced

The new lightweight contract lives in `nexus/core/mutations.py`.

It introduces three small concepts:

- `MutationContext`
  - normalized actor, reason, cli id, timestamp, and workspace id
- `MutationResult[T]`
  - explicit mutation action, target type, target id, and typed payload returned to callers
- shared helpers for:
  - capability checks through the registry
  - status-transition validation
  - audit-log writing

This is intentionally not a command bus or framework.

It is a narrow normalization layer for the current controlled writes.

## How the Contract Applies to the Current Flows

### 1. Activity status update

`nexus.activities.update_activity_status_mutation(...)` now follows the explicit pattern:

1. resolve target activity
2. normalize actor/reason/cli metadata into `MutationContext`
3. validate status-transition capability and allowed transition
4. apply the update
5. write audit through the shared helper
6. return `MutationResult[ActivityRecord]`

The public `update_activity_status(...)` function remains compatible and still returns `ActivityRecord` for current CLI/API/cockpit callers.

### 2. Document lifecycle status update

`nexus.documents.update_document_status_mutation(...)` now follows the same contract with one extra capability check:

- the document type must support lifecycle
- the document type must support status transitions

The public `update_document_status(...)` function remains compatible and still returns `DocumentRecord`.

### 3. Document reconciliation

`nexus.documents.reconcile_document_mutation(...)` now uses the same mutation contract for:

1. target resolution
2. integrity capability check
3. safe reconcile validation
4. state update when a reconcile is actually needed
5. audit write through the shared helper
6. return `MutationResult[DocumentReconciliationResult]`

The public `reconcile_document(...)` function remains compatible and still returns `DocumentReconciliationResult`.

## Where the Registry Is Now Operationally Relevant

In Phase 1, the registry was primarily descriptive.

In Phase 2, it becomes operational in a conservative way:

- activity mutation path checks that the type supports status transitions
- document lifecycle mutation path checks lifecycle and transition support
- document reconciliation checks integrity support

This gives the registry a real role in mutation semantics without forcing every flow to route through it artificially.

## What Remains Intentionally Outside the Pattern

This pass does not move all writes to the mutation contract.

Still outside the pattern for now:

- create flows for entities, relations, documents, cycles, and activities
- any future writes not yet implemented
- presentation-layer result shaping in CLI/API/cockpit

That is intentional.

Phase 2 only standardizes the already controlled write paths that behave like platform mutations.

## Compatibility Strategy

The public MVP surface remains stable:

- CLI commands still call the same top-level mutation functions
- API endpoints still receive the same payloads and return the same shapes
- cockpit mutations still use the same API routes and get the same effective responses

The new mutation-result wrappers are internal architectural structure first.

## Result

The backend now has a clearer mutation pattern:

- resolve
- validate
- apply
- audit
- return

This should make later controlled mutations easier to add without re-implementing the same platform semantics in ad hoc ways.
