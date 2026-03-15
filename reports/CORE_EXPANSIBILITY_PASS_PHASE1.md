# Core Expansibility Pass - Phase 1

## Purpose

This pass does not expand the Nexus product surface.

Its goal is to make the current MVP backend easier to extend without turning the codebase into a pile of tightly coupled feature flows.

The main architectural move is to separate three concerns more explicitly:

- stable platform core
- domain primitives
- presentation surfaces

It also introduces a lightweight read-model foundation and a minimal type/capability registry.

## Boundary Model

### Core platform

Core platform code now lives explicitly under `nexus/core/`.

Phase 1 defines three platform concerns there:

- `nexus/core/workspace.py`
  - workspace bootstrap
  - workspace contract validation
  - schema loading
  - DB connection helpers
  - low-level workspace metadata inspection
- `nexus/core/read_models.py`
  - aggregated, UI-facing, read-heavy workspace views
  - counts
  - operational summaries
- `nexus/core/registry.py`
  - explicit metadata about current supported domain types and capabilities

This is the stable substrate that later derived modules should attach to.

### Domain primitives

Current domain primitives remain simple and explicit:

- `nexus/entities.py`
- `nexus/relations.py`
- `nexus/documents.py`
- `nexus/cycles.py`
- `nexus/activities.py`
- `nexus/audit.py`

These modules still own their local persistence and mutation logic.

The Phase 1 goal is not to turn them into a heavy service layer.
It is to keep them narrow and make clear that they depend on the core platform rather than defining it.

### Presentation surfaces

The current surfaces remain:

- `nexus/cli.py`
- `nexus/api.py`
- `nexus/cockpit.py`

These are presentation adapters over the same local substrate.

They should consume domain reads and core read models, not build independent aggregation logic.

### Future derived modules

Future derived modules should be treated as additive layers on top of the core substrate, not as places to redefine workspace/bootstrap/integrity foundations.

Examples:

- project-management read models
- CRM-oriented views
- semantic retrieval modules
- BI / cognitive observability modules

They should attach through:

- domain primitives already persisted in DuckDB and Markdown
- core read models
- explicit type/capability metadata

## Role of the Read-Model Layer

The read-model layer introduced in this pass is intentionally small.

It is not a CQRS framework.

Its role is to centralize aggregated reads that are:

- presentation-facing
- summary-oriented
- composed from multiple low-level records

Phase 1 moves workspace-level operational aggregation into `nexus/core/read_models.py`.

That includes:

- total resource counts
- document status counts
- cycle status counts
- activity status rollups
- composed workspace overview reads

This keeps the core workspace module focused on substrate concerns and prevents CLI/API/cockpit from reassembling the same operational summary in multiple places.

## Role of the Type/Capability Registry

The new registry in `nexus/core/registry.py` makes the current MVP object model more explicit without introducing a heavy metamodel.

For each current supported domain type, it records:

- category
- whether it has lifecycle semantics
- whether it has integrity semantics
- whether it has status transitions
- whether it is primarily read-heavy

In the current MVP, this registry is internal metadata.

Its purpose is to support:

- safer future expansion
- clearer reasoning about derived modules
- clearer distinction between lifecycle-bearing and integrity-bearing objects
- future read-model/view registration without hidden assumptions

## What Is Explicitly Core vs Derived

### Core

Consider these core:

- workspace contract
- workspace bootstrap
- schema loading
- DB connection and workspace validation
- operational read-model composition
- type/capability metadata

### Not core

Consider these not core:

- individual CLI commands
- API route declarations
- cockpit HTML/JS rendering
- future vertical modules
- any derived dashboard or specialized observational layer

### Derived but current

The existing domain modules are current first-party primitives, but they are not the whole platform core.

They sit above the substrate and below presentation.

That distinction matters for future expansion.

## Compatibility Strategy

To keep the product surface stable in this phase:

- legacy imports from `nexus.workspace` and `nexus.workspace_contract` still work through compatibility shims
- CLI/API/cockpit behavior stays the same
- the refactor changes internal placement and composition first

This keeps the pass conservative and traceable.

## Follow-up Direction

Phase 1 is only a foundation pass.

Likely next low-risk follow-ups:

- move additional presentation-facing rollups into read models where duplication appears
- standardize mutation contract helpers without hiding domain behavior
- let future derived modules register read-heavy capabilities explicitly against the lightweight registry
