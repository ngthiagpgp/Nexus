# NEXUS_IMPLEMENTATION_SEQUENCE

**Status:** Draft  
**Owner:** Thiago  
**Purpose:** Definir a ordem exata de build do Nexus MVP para transformar o bootstrap documental atual em uma sequencia de implementacao executavel, incremental e auditavel.

---

## 1. Why this document exists

The current repository already defines:

- product intent in `Plan/NEXUS_MVP_SPEC.md`
- API contracts in `Plan/NEXUS_MVP_API_SPEC.md`
- CLI contracts in `Plan/NEXUS_MVP_CLI_SPEC.md`
- initial data model in `Plan/NEXUS_MVP_SCHEMA.sql`
- architectural guardrails in `Plan/NEXUS_ARCHITECTURE_REFERENCES.md`
- implementation discipline in `AGENTS.md`

What is still missing is the exact build order.

Without that sequence, later implementation sessions are likely to:

- start by building interfaces before there is stable state;
- add runtime complexity before the control plane exists;
- collapse Markdown and DB into a single storage role;
- implement endpoints or commands without a coherent substrate;
- produce large changes that are hard to audit or review.

This document closes that gap.

Its role in the bootstrap is practical:

1. define the recommended order of implementation;
2. identify the smallest coherent slices that should be shipped first;
3. constrain future Codex sessions to narrow, reviewable increments;
4. reduce architecture drift while the repository is still mostly specs.

This is not a replacement for the MVP spec.  
It is the execution map that sits between the specs and the codebase.

---

## 2. Implementation principles

### 2.1 Spec-first
Implementation should begin from repository specs, not from opportunistic coding.

Every implementation session should explicitly anchor itself in:

- the user prompt;
- the relevant file in `Plan/`;
- the current repository state.

If a proposed implementation is not clearly traceable to those sources, it is probably too early or too broad.

### 2.2 Smallest viable increment
Each session should ship the smallest complete slice that:

- creates a stable boundary;
- can be validated locally;
- leaves the repository easier to understand than before.

The Nexus should not be bootstrapped through broad scaffolding with fake completeness.

### 2.3 Auditability first
Important system behavior must become inspectable early.

That means early slices should prefer:

- deterministic file layout;
- stable local state;
- explicit logging;
- audit records for mutations;
- readable commit history.

Observability is not a polish step. It is part of the substrate.

### 2.4 Control plane before aggressive automation
The system should know what session is active, what execution is running, and what changed before it tries to automate complex behavior.

Do not start by building:

- autonomous ingestion flows;
- advanced workflow orchestration;
- complex agent routing;
- opaque background automation.

Start by making the system governable.

### 2.5 Markdown and local DB have distinct roles
The repository specs already separate those roles and implementation should preserve that separation:

- Markdown stores living content and human-readable artifacts.
- The local DB stores structured operational state, relations, indexes, and audit history.

Early implementation should reinforce this distinction instead of blurring it for convenience.

---

## 3. Build sequence overview

Recommended build order:

1. Phase 0: repository and spec hardening
2. Phase 1: local core substrate
3. Phase 2: minimal control plane
4. Phase 3: initial CLI operations
5. Phase 4: API exposure
6. Phase 5: runtime adapters and tracing basics
7. Phase 6: cockpit and basic UI
8. Phase 7: expansion layers

This order is intentional:

- substrate before interfaces;
- governance before automation;
- CLI before richer surfaces;
- API before cockpit;
- tracing before complex agent behavior.

---

## 4. Phase 0: repository and spec hardening

### Objective
Make the repository implementation-ready and reduce ambiguity before application code starts.

### Scope

- validate that the core planning docs are internally aligned;
- define missing execution-oriented planning artifacts;
- establish repository contract for sessions and commits;
- confirm expected folder conventions for later slices.

### Deliverables

- `AGENTS.md`
- `Plan/NEXUS_IMPLEMENTATION_SEQUENCE.md`
- stable `logs/sessions/` path
- clear agreement on first executable slice

### Dependencies

- existing `Plan/` specs
- repository initialized in git

### Non-goals

- application runtime code
- API handlers
- CLI commands
- UI scaffolding

### Acceptance criteria

- the repository has an explicit operational contract for implementation sessions;
- there is a practical sequence document that can guide subsequent prompts;
- later sessions can identify what to build first without re-inventing the roadmap.

---

## 5. Phase 1: local core substrate

### Objective
Create the minimal local substrate that can persist state, store documents, and record mutations reliably.

### Scope

- workspace initialization flow
- local DuckDB bootstrap using the MVP schema as baseline
- deterministic filesystem layout for document storage and local config
- minimal migration/bootstrap runner
- minimal audit write path for state mutations
- hash-aware document persistence primitives

### Deliverables

- an app/package skeleton for the local Nexus core
- a bootstrap command or script equivalent to `nexus init`
- creation of:
  - `nexus.duckdb`
  - `.nexus/config.*`
  - document root folders
  - backup folder placeholder if required
- DB bootstrap from `Plan/NEXUS_MVP_SCHEMA.sql`
- repository-safe document I/O utilities
- a basic audit logging utility for create/update operations

### Dependencies

- Phase 0 completed
- schema source available in `Plan/NEXUS_MVP_SCHEMA.sql`

### Non-goals

- full business CRUD
- HTTP server
- React UI
- autonomous agent workflows
- advanced reconciliation logic

### Acceptance criteria

- a fresh local workspace can be initialized deterministically;
- the DuckDB file is created and populated with baseline schema/system state;
- document folders are created in a predictable structure;
- at least one mutation path can write to `audit_log`;
- Markdown persistence and DB persistence are implemented as separate concerns.

---

## 6. Phase 2: minimal control plane

### Objective
Introduce the smallest governable control-plane concepts required to supervise execution and state transitions.

### Scope

- session identity
- execution identity
- system status surface
- event and audit registration for major operations
- basic health and environment reporting

### Deliverables

- a minimal session registry model
- a minimal execution registry model
- system status service backing `nexus status` and later `/system/status`
- stable metadata for:
  - active workspace
  - active session
  - last sync
  - schema version
- explicit event recording for important operations

### Dependencies

- Phase 1 substrate

### Non-goals

- sophisticated orchestration engine
- multi-agent routing
- scheduling or background workers
- rich UI dashboards

### Acceptance criteria

- the system can identify an active session or create one when needed;
- important operations can be associated with a session or execution context;
- there is a single place to ask for current system status;
- control metadata exists before advanced automation begins.

---

## 7. Phase 3: initial CLI operations

### Objective
Expose the first stable operational surface through CLI commands that operate on the local substrate and control plane.

### Scope

- bootstrap and status commands first
- minimal CRUD for the most foundational entities
- document creation and validation primitives
- audit inspection

Recommended command order:

1. `nexus init`
2. `nexus status`
3. `nexus entity add/list/show`
4. `nexus relation add/list/show`
5. `nexus document create/show`
6. `nexus audit`

### Deliverables

- a Typer-based CLI entrypoint
- consistent output conventions
- minimal JSON mode where it materially helps future API and tooling reuse
- first safe write flows for:
  - entities
  - relations
  - documents
- first read flows for:
  - system status
  - audit log

### Dependencies

- Phase 1 substrate
- Phase 2 control metadata

### Non-goals

- full CLI coverage from the spec
- interactive graph visualizations
- batch ingestion
- approval workflows with git automation

### Acceptance criteria

- a user can initialize a workspace and inspect status from the CLI;
- a user can create and list entities and relations;
- a user can create a draft document with Markdown persisted to disk and metadata persisted to DB;
- writes leave an auditable trail;
- command behavior is narrow, explicit, and locally testable.

---

## 8. Phase 4: API exposure

### Objective
Expose the same stable core capabilities over a local API without changing the source-of-truth model.

### Scope

- FastAPI application shell
- health/system endpoints first
- entity, relation, and document endpoints backed by shared services
- response shape alignment with `Plan/NEXUS_MVP_API_SPEC.md`

### Deliverables

- application bootstrap for FastAPI
- `/system/status`
- initial endpoints:
  - `GET/POST /entities`
  - `GET /entities/{id}`
  - `GET/POST /relations`
  - `GET /relations/{id}`
  - `GET/POST /documents`
  - `GET /documents/{id}`
- service layer reused by CLI and API
- error normalization aligned to the API spec

### Dependencies

- Phase 3 CLI-safe core services

### Non-goals

- WebSocket behavior
- document approval auto-commit
- full query language
- inbox ingestion breadth
- UI-facing auto-save polish

### Acceptance criteria

- API handlers delegate to shared domain/services instead of duplicating logic;
- the API reflects the local DB and Markdown substrate already established;
- endpoint behavior is coherent with existing CLI semantics;
- errors are explicit and predictable.

---

## 9. Phase 5: runtime adapters and tracing basics

### Objective
Introduce the first runtime execution boundaries and traces without overbuilding full automation.

### Scope

- executor adapter abstraction
- task runner boundary
- basic trace capture
- minimal tool invocation recording
- safe draft-only automation hooks

### Deliverables

- a runtime adapter contract
- one initial local adapter, likely for the current executor environment
- trace records tied to execution/session identity
- basic output records for generated artifacts
- draft-safe runtime actions for low-risk operations

### Dependencies

- Phase 2 control plane
- Phase 4 services/API surface

### Non-goals

- complex workflow graphs
- autonomous inbox triage
- unrestricted write automation
- multi-adapter production matrix

### Acceptance criteria

- runtime actions can be traced back to a session/execution;
- adapter behavior is explicit and replaceable;
- generated outputs can be registered without pretending the runtime is fully mature;
- no sensitive action bypasses auditability.

---

## 10. Phase 6: cockpit and basic UI

### Objective
Provide a basic human supervision surface after the substrate, control plane, and initial operations already exist.

### Scope

- status inspection
- document inspection
- audit inspection
- session/execution visibility
- limited editing only where backend semantics already exist

### Deliverables

- a basic web UI shell
- views for:
  - system status
  - entities
  - documents
  - audit history
  - sessions/executions
- minimal editing support for already-supported backend operations

### Dependencies

- Phase 4 API exposure
- Phase 5 runtime traces if trace inspection is included

### Non-goals

- design polish as primary work
- complete tab coverage from the product vision
- rich graph exploration
- advanced editor ergonomics
- heavy frontend state complexity before core flows are stable

### Acceptance criteria

- the UI is a supervision surface, not a speculative product shell;
- key state can be inspected without direct DB access;
- UI operations do not invent new backend semantics;
- cockpit functionality increases visibility instead of hiding complexity.

---

## 11. Phase 7: expansion layers

### Objective
Expand the Nexus carefully after the core substrate, governance, and inspection loops are already stable.

### Scope

- inbox ingestion breadth
- query language growth
- document approval and git-linked flows
- conflict detection and reconciliation
- richer workflows
- additional adapters and connectors
- backup and restore maturity

### Deliverables

- inbox ingest and triage flows
- simple query engine beyond narrow CRUD
- document validation and approval lifecycle
- filesystem-versus-DB reconciliation tools
- stronger backup/restore handling
- richer cockpit views

### Dependencies

- Phases 1 through 6

### Non-goals

- rewriting early architecture
- replacing the storage model
- collapsing all behavior into one generalized automation layer

### Acceptance criteria

- each expansion feature reuses existing substrate, control, and audit layers;
- the system remains explainable after adding automation;
- later complexity is additive, not corrective to a weak foundation.

---

## 12. First executable slice

The first executable slice should be the smallest coherent implementation that proves the Nexus substrate is real.

### Recommended first slice

Build:

1. repository-local Python package/app skeleton;
2. workspace bootstrap flow equivalent to `nexus init`;
3. DB bootstrap from the existing schema file;
4. local config creation under `.nexus/`;
5. document root creation;
6. a basic `nexus status`;
7. one auditable write path, preferably `nexus entity add`.

### Why this should come first

This slice creates:

- a real local system boundary;
- a repeatable way to initialize state;
- a known place for config and documents;
- the first proof that DB writes and audit writes work;
- a base that every later CLI/API/UI path can reuse.

It also avoids a common failure mode: building command surfaces or HTTP routes before there is a stable substrate behind them.

### What this first slice should explicitly avoid

- React frontend setup
- broad CRUD coverage
- inbox ingestion
- document approval with git automation
- advanced runtime adapters
- speculative control-plane complexity beyond minimal session/status scaffolding

### Acceptance criteria for the first slice

- `nexus init` (or equivalent bootstrap command) creates the local workspace substrate;
- `nexus status` can report schema version and workspace metadata;
- `nexus entity add` persists one entity record successfully;
- the entity creation also creates an `audit_log` entry;
- the repository gains a small but real executable core.

---

## 13. Prompting guidance for implementation sessions

Future implementation prompts should be scoped as execution slices, not as broad product aspirations.

### Good prompt pattern

Each implementation prompt should state:

1. the target phase;
2. the exact slice to implement;
3. the relevant spec files;
4. explicit non-goals;
5. expected validation.

Example shape:

> Implement Phase 1, Slice A: workspace bootstrap and schema initialization.  
> Read `AGENTS.md`, `Plan/NEXUS_MVP_SPEC.md`, `Plan/NEXUS_MVP_SCHEMA.sql`, and `Plan/NEXUS_IMPLEMENTATION_SEQUENCE.md`.  
> Do not add API routes or frontend code.  
> Deliver a local bootstrap command, config creation, DB initialization, and a basic status check.  
> Add tests if the repository structure already supports them.

### Prompt rules for later sessions

- ask for one coherent slice at a time;
- name the phase explicitly;
- say what not to build in that session;
- anchor the request to the relevant spec files;
- request local validation where possible;
- require a session summary and commit unless intentionally paused.

### Prompting anti-patterns

Avoid prompts like:

- "build the Nexus MVP"
- "create the whole backend"
- "set up the full architecture"
- "add the UI and API and runtime"
- "make it production ready"

Those prompts are too broad for a repository that is still in bootstrap mode.

---

## 14. What should NOT be built too early

The following items are directionally correct for the Nexus, but should not be built before the substrate and control-plane basics are stable:

- full React cockpit with polished UX
- advanced query language/parser
- autonomous ingestion pipelines
- aggressive background automation
- multi-agent orchestration
- heavy workflow engines
- approval flows that trigger git commits automatically
- reconciliation engines before basic document I/O is stable
- complex sync across multiple external systems
- broad plugin or adapter ecosystems
- generalized abstraction layers for future providers not yet needed

The repository should first become:

- bootable;
- inspectable;
- auditable;
- locally coherent.

Only then should it become expansive.

---

## 15. Practical sequencing rule

When in doubt, prefer the next slice that improves one of these in order:

1. local substrate integrity
2. control and auditability
3. operator-facing CLI usefulness
4. API reuse of the same core
5. runtime traceability
6. cockpit visibility
7. expansion and automation

If a proposed change skips upward in that stack without satisfying the lower level first, it is probably out of sequence.
