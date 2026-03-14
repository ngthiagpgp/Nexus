# NEXUS_ARCHITECTURE_REFERENCES
**Status:** Draft aligned to current repository state  
**Owner:** Thiago  
**Purpose:** Keep a practical architectural reference for Nexus, grounded in what is already implemented in this repository and explicit about what remains planned.

---

## 1. Why this document exists

The Nexus repository is intentionally spec-first, but the codebase is no longer only a planning scaffold. There is now a small executable core under `nexus/`, a working Typer CLI, a DuckDB bootstrap path, Markdown document persistence, and smoke tests covering the implemented flows.

This document exists to do three things at the same time:

1. preserve the architectural synthesis that guides Nexus as a governed local-first system;
2. describe the architecture that is actually implemented today;
3. prevent future sessions from treating planned layers as if they already exist.

It is a reference document, not a product spec and not a promise that every planned layer is already present.

---

## 2. Current repository baseline

As of the current implementation state, the repository contains:

- planning artifacts in `Plan/`;
- a Python package in `nexus/`;
- a local CLI exposed as `nexus`;
- a local DuckDB bootstrap using `Plan/NEXUS_MVP_SCHEMA.sql`;
- filesystem-backed document creation under `documents/`;
- audit writes for the implemented mutation flows;
- smoke tests in `tests/test_init_smoke.py`.

The current executable scope is narrow and local-only. The repository does **not** currently implement:

- FastAPI endpoints;
- a web cockpit or React frontend;
- session registry or execution registry;
- runtime adapters beyond the local CLI process itself;
- inbox ingestion flows;
- query language execution;
- document approval, sync, backup, restore, or conflict reconciliation flows.

That distinction matters. Architectural references should guide the next increments without overstating maturity.

---

## 3. External references and how Nexus uses them

### 3.1 OpenClaw

OpenClaw remains a useful conceptual reference for:

- separating a control plane from the executor;
- treating sessions, tools, and supervision as product concerns;
- keeping governance visible instead of implicit.

In the current Nexus repository, this influence is still mostly directional. The codebase does **not** yet implement an OpenClaw-like control plane. The present code only includes a minimal local status/bootstrap surface and some seeded `system_state` metadata.

Reference:
- https://github.com/openclaw/openclaw

### 3.2 Mastra

Mastra remains a useful conceptual reference for:

- explicit runtime boundaries;
- workflows and tool contracts;
- tracing and inspection as first-class concerns.

In the current Nexus repository, this influence is also still directional. There is no workflow runtime, no trace model, and no inspection studio implemented yet.

Reference:
- https://github.com/mastra-ai/mastra
- https://mastra.ai/docs

### 3.3 Practical interpretation for Nexus

The main architectural lesson that still applies is:

> the current executor surface is not the whole system.

For the repository as it exists today, that means:

- the CLI is the current operator surface, not the final architecture;
- DuckDB plus Markdown form the current operational substrate;
- richer control-plane, runtime, adapter, and cockpit layers remain planned, not delivered.

---

## 4. Architectural synthesis adopted by Nexus

The long-term architectural model is still:

**Nexus = Control Plane + Runtime + Knowledge/State Fabric + Adapters + Cockpit**

That model remains useful, but it must be read in two modes:

1. as a design target for future sequencing;
2. as a lens for classifying what the repository already contains.

Today, the codebase implements only a subset of that model. The strongest implemented layer is the local knowledge/state substrate, with a thin CLI surface and a very small amount of status metadata around it.

---

## 5. Current implemented architecture

### 5.1 Entry surface

The active operator surface is the Typer CLI defined in `nexus/cli.py`.

Implemented commands:

- `nexus init`
- `nexus status`
- `nexus entity create`
- `nexus entity list`
- `nexus relation create`
- `nexus relation list`
- `nexus document create`
- `nexus document list`
- `nexus cycle create`
- `nexus cycle list`
- `nexus activity create`
- `nexus activity list`

There is no HTTP layer, no background worker, and no UI layer in the current codebase.

### 5.2 Local substrate

The implemented substrate is local-first and split between filesystem and DuckDB:

- filesystem layout is defined in `nexus/workspace_contract.py`;
- workspace bootstrap and inspection live in `nexus/workspace.py`;
- the database file is `nexus.duckdb`;
- workspace config is `.nexus/config.yaml`;
- document roots are created under `documents/`;
- bootstrap also creates `.nexus/backups/` as a placeholder path.

This is the most concrete architectural boundary currently implemented in Nexus.

### 5.3 State model

`Plan/NEXUS_MVP_SCHEMA.sql` is used as the schema source for bootstrap. The implementation applies one conservative compatibility normalization before executing it, because the schema seeds `system_state.value` with `NULL`-like values even though the column is `NOT NULL`.

The schema creates more tables than the current CLI uses. In practice:

- actively used by implemented flows: `system_state`, `audit_log`, `entities`, `relations`, `documents`, `cycles`, `activities`;
- present in schema but not yet exercised by CLI flows: `outputs`, `inbox_items`.

This is an important distinction between available structure and implemented behavior.

### 5.4 Domain modules

The current application layer is simple and module-oriented:

- `nexus/workspace.py` handles workspace bootstrap, status inspection, schema loading, config generation, and DB connection helpers;
- `nexus/entities.py` handles entity create/list plus input normalization;
- `nexus/relations.py` handles relation create/list and entity reference resolution;
- `nexus/documents.py` handles draft document creation on disk plus document metadata insertion in DuckDB;
- `nexus/cycles.py` handles cycle creation/listing and deterministic cycle IDs;
- `nexus/activities.py` handles activity creation/listing and validates cycle existence.

There is no separate service layer, API layer, or runtime orchestration layer yet. The CLI calls these modules directly.

### 5.5 Audit and traceability

Auditability is partially implemented already:

- every implemented create flow writes a corresponding row to `audit_log`;
- workspace metadata is written to `system_state`;
- document creation records `content_hash`, `version`, and an initial JSON changelog;
- tests validate that audit rows are created for the implemented entity, relation, cycle, activity, and document flows.

This is still narrower than the planned Nexus control plane. What exists today is operation-level audit logging, not full session/execution tracing.

---

## 6. Layer status: implemented vs planned

### 6.1 Already implemented layers and components

| Layer | Current state in repo |
|---|---|
| Knowledge/State Fabric | Implemented in a first usable form: DuckDB bootstrap, filesystem workspace contract, Markdown draft creation, `system_state`, `audit_log`, and resource tables used by the CLI |
| CLI operator surface | Implemented as the only active interface, via Typer |
| Workspace bootstrap/status | Implemented through `nexus init` and `nexus status` |
| Resource flows | Implemented for create/list on entities, relations, documents, cycles, and activities |
| Validation/test coverage | Implemented as smoke coverage in `tests/test_init_smoke.py` |

### 6.2 Planned but not yet implemented layers and components

| Layer | Planned scope not yet in repo |
|---|---|
| Control Plane | session registry, execution registry, system events, richer health/status coordination, operational policies |
| Runtime | workflows, tool routing, adapter contracts, trace capture, evals, supervised automation |
| Adapters | executor abstraction beyond the local CLI process, MCP-facing or external connectors |
| Cockpit/UI | React or other web supervision layer, inspection panels, document editing UI, audit views |
| API | FastAPI endpoints described in `Plan/NEXUS_MVP_API_SPEC.md` |
| Extended CLI flows | show/edit/delete/approve/validate/query/inbox/backup/restore/config/audit commands from the broader CLI spec |

This distinction should remain explicit in future documentation and reviews.

---

## 7. What the current architecture does and does not prove

### 7.1 What is already proven

The repository now proves that Nexus can:

- bootstrap a deterministic local workspace;
- create a local DB from the MVP schema source;
- maintain separate roles for Markdown documents and operational DB state;
- perform a small set of auditable CLI mutations;
- keep the implementation narrow and testable.

### 7.2 What is still only architectural intent

The repository does **not** yet prove:

- the full control-plane model from the broader Nexus vision;
- runtime orchestration or governed automation;
- API/CLI parity beyond the implemented subset;
- inline editing, approval flow, Git-linked document lifecycle, or reconciliation logic;
- inbox ingestion, query execution, outputs management, or cockpit supervision.

Future sessions should not infer those capabilities just because the schema or specs mention them.

---

## 8. Practical guidance for future implementation and review

When evaluating a change against the current architecture, use these rules:

1. treat the local DuckDB plus Markdown substrate as the current core;
2. avoid documenting planned layers as implemented unless code and tests exist for them;
3. preserve the separation between document content in files and operational state in the DB;
4. keep new increments small enough to remain auditable and directly grounded in `Plan/`;
5. prefer extending the current local core before introducing API, runtime, or UI complexity.

For the current repository state, the most accurate architectural reading is:

> Nexus is currently a local CLI-driven substrate with auditable CRUD-style flows over DuckDB and Markdown, designed to grow later into a fuller governed system.

That statement is more precise than either extreme of:

- "Nexus is still only a spec repository"; or
- "Nexus already has its full control plane/runtime/cockpit architecture implemented."

---

## 9. Review heuristics for future PRs

Any future change should still answer:

1. Which current layer does this change extend?
2. Is the change implemented, or is it only updating a plan/spec?
3. What is the source of truth for the data involved?
4. Does the change preserve DB-vs-document separation?
5. Is the behavior auditable with the current architecture?
6. Does the change overstate maturity relative to the code that actually exists?

If a PR or spec update cannot answer those clearly, it is likely introducing architectural drift.

---

## 10. References

- `README.md`
- `AGENTS.md`
- `Plan/NEXUS_MVP_SPEC.md`
- `Plan/NEXUS_MVP_CLI_SPEC.md`
- `Plan/NEXUS_MVP_API_SPEC.md`
- `Plan/NEXUS_MVP_SCHEMA.sql`
- `Plan/NEXUS_IMPLEMENTATION_SEQUENCE.md`
- OpenClaw repository: https://github.com/openclaw/openclaw
- Mastra repository: https://github.com/mastra-ai/mastra
- Mastra documentation: https://mastra.ai/docs
