by chatgpt in 15-03-2025 1:14:00
# Requirements Assessment — UI, Human Test, and Core Expansibility
**Project:** Nexus  
**Status:** Working assessment  
**Scope:** Consolidation of findings and requirements gathered after the latest UI cycles, pre-human-test passes, human test, and speculative expansibility analysis  
**Purpose:** Capture the current product diagnosis, the main user-facing requirements, and the architectural requirements needed before broader expansion or operation

---

## 1. Executive Summary

The latest cycles materially changed the state of Nexus.

Nexus is no longer only a technical prototype. It now has:

- local-first workspace bootstrap;
- operational CLI;
- local API;
- read-only and write-controlled cockpit;
- document lifecycle and reconciliation;
- audit trail;
- demo seed and serve flow.

However, the first human test showed a critical distinction:

> Nexus is already viable as an agent-first operational system, but it is not yet mature as a human-first workspace.

The core problem is no longer missing backend capability.  
The main gap is now the mismatch between:

- what the system can do;
- what a human can immediately perceive, understand, and trust.

This assessment therefore consolidates two parallel requirement sets:

1. **UI / human comprehension requirements**
2. **core expansibility requirements**

The strategic conclusion is:

> Nexus should currently be treated as a shared operational base between human and agent, where the agent is the primary procedural operator and the human is the supervisory cognitive operator.

This has strong implications for both product design and core architecture.

---

## 2. Source of this assessment

This document consolidates requirements inferred from the following recent workstreams:

- cockpit implementation and refinement;
- audit and release hardening;
- pre-human-test UX pass;
- first human test of the MVP;
- product thesis exploration around shared surface between agent and human;
- speculative expansibility tests for:
  - project management
  - CRM
  - embedding / semantic layer
  - BI / cognitive observability;
- evaluation of whether the current backend should be reconfigured before broader operation.

This is therefore not a greenfield PRD.  
It is a structured reading of what the product has already revealed about itself.

---

## 3. Current product diagnosis

### 3.1. What Nexus already is

At the current stage, Nexus is best described as:

- a local-first operational system;
- based on structured state plus file-backed documents;
- shared between human and agent;
- supervised through CLI, API, and cockpit;
- governed by explicit lifecycle, integrity, reconciliation, and audit patterns.

### 3.2. What Nexus is not yet

At the current stage, Nexus is not yet:

- a human-first workspace;
- a visually intuitive cognitive environment;
- a graph-native or timeline-native work surface;
- a complete project manager, CRM, or BI suite;
- a broadly operable product for users with no mediation.

### 3.3. Key product tension

The human test revealed the central tension:

- the backend and operational flows are increasingly coherent;
- the human-facing comprehension layer is still weak.

This means the main bottleneck has moved from capability to legibility.

---

## 4. Core product thesis

The product thesis that emerged from the recent exploration can be stated as follows:

> Nexus is a shared operational substrate between humans and agents.
> The agent interacts procedurally.
> The human interacts cognitively.
> Both must see the same underlying reality, but not necessarily through the same interface.

This leads to two related principles.

### 4.1. Primary principle
**What the agent sees, the human must also be able to see.**

This implies:

- common data substrate;
- common ontology;
- shared state model;
- shared audit and lifecycle visibility.

### 4.2. Secondary principle
**What the agent does, the human should be able to understand, supervise, and, where useful, also perform.**

This principle is weaker and should not be interpreted as strict symmetry of interaction.
The human and the agent do not need identical workflows; they need coherent access to the same reality.

---

## 5. Requirements from the human test

### 5.1. Summary of human-test findings

The first human test showed that:

- installation and setup are now viable;
- core operational flows do work;
- status updates and document lifecycle are usable;
- cockpit navigation is still not intuitive enough;
- the main work model is not yet obvious to a human;
- reconciliation/integrity remains poorly understood from the UI;
- the product currently feels more useful for an agent than for a human operator.

### 5.2. Key interpreted finding

The most important finding is this:

> The MVP did not fail as an operational system.
> It failed as a sufficiently self-explanatory human product.

This distinction matters because it changes what should happen next:
the priority is no longer “add more capability,” but rather “improve the human comprehension layer.”

---

## 6. UI and human-comprehension requirements

### 6.1. Requirement group A — Explicit operational model

The cockpit must make the main work model explicit.

The human should be able to understand, within seconds:

- what the central object of navigation is;
- what a cycle is;
- how activities relate to cycles;
- how documents relate to activities and cycles;
- what actions are currently expected.

#### Implication
The UI cannot remain organized primarily by backend object categories.
It must expose a more understandable work logic.

---

### 6.2. Requirement group B — Clear hierarchy of attention

The interface must make it visually obvious:

- what matters now;
- what is selected;
- what changed;
- what requires action;
- what is secondary.

The human test showed friction around:
- where to click;
- where a document is shown;
- where the status control lives;
- what the audit area means;
- what reconcile means.

#### Implication
The cockpit needs stronger information hierarchy and clearer focus states.

---

### 6.3. Requirement group C — Better human readability

The current UI still feels too vertical, too dense, and too procedural.

The cockpit must improve:

- content placement;
- panel priority;
- readability of document content;
- visibility of the active context;
- stability during mutation.

#### Specific issues identified
- document view is hard to read in the lower-right region;
- screen “blinks” and reflows when state changes;
- navigation depends too much on implicit panel logic.

---

### 6.4. Requirement group D — Reduced technical language burden

The human test showed friction with:
- many names in English;
- insufficient conceptual explanation;
- unclear meaning of cycle / integrity / reconcile.

#### Implication
The human-facing surface needs:
- clearer labels;
- less backend language;
- more operational wording;
- small contextual explanations.

---

### 6.5. Requirement group E — Stronger readiness and continuity cues

The first impression must feel stable and legible.

The cockpit should always communicate:
- loading state;
- ready state;
- active selection;
- result of the last action;
- continuity after mutation.

The latest UX pass improved this, but this requirement remains foundational.

---

## 7. Requirements for a human-cognitive layer

A major conclusion of the exploration is that the cockpit should not be only a control surface.
It should evolve into a cognitive surface.

The human uses the system not only to mutate state, but to understand:

- structure;
- time;
- proportion;
- state;
- change.

This suggests that the future human-facing Nexus should support five reading modes.

### 7.1. Now
Immediate operational situation:
- current cycle
- pending work
- alerts
- recent changes
- items requiring attention

### 7.2. Map
Structural relations:
- entities
- clusters
- dependencies
- related documents
- graph-like context

### 7.3. Time
Temporal understanding:
- cycle history
- deadlines
- state changes over time
- cadence

### 7.4. Flow
Operational movement:
- kanban
- blocked items
- throughput
- transitions

### 7.5. Memory
Continuity:
- recent sessions
- key documents
- context recovery
- decision memory

These do not all need to exist immediately, but they should now be treated as a serious requirement direction.

---

## 8. Requirements derived from expansibility analysis

The recent speculative tests showed that the backend is not trapped in a single vertical.
It is already behaving like a platform.

This implies a new architectural requirement:

> The Nexus core must be clarified as a platform core, not just as an accumulation of current features.

### 8.1. Requirement group F — Explicit core vs derived-module boundary

The system should formally distinguish between:

#### Core platform
- workspace
- storage
- ids
- audit
- lifecycle
- integrity
- reconciliation
- API shell
- cockpit shell

#### Domain primitives
- entity
- relation
- document
- cycle
- activity

#### Derived modules
- project manager
- CRM
- embedding layer
- BI / observability
- case management
- second-brain layer

This boundary is currently implicit and should be made explicit before the system expands further.

---

### 8.2. Requirement group G — Type and capability clarity

The backend is fertile because it is generic.
However, further expansion will require a better distinction between:

- free types;
- supported types;
- capability-bearing types;
- lifecycle-bearing types;
- view-bearing types.

This does not yet require a heavy metamodel,
but it does require an explicit type/capability policy.

---

### 8.3. Requirement group H — Read-model layer

This is the most important architectural requirement identified in the expansibility analysis.

The next stage of Nexus will depend less on CRUD and more on:
- summaries
- projections
- aggregations
- graph views
- timeline views
- dashboard views
- audit and integrity surfaces

Therefore, Nexus needs a clearer read-model layer.

Without it:
- UI logic will spread;
- API duplication will increase;
- derived modules will become harder to add.

---

### 8.4. Requirement group I — Mutation contract standardization

The system now has several controlled mutation flows:
- activity status
- document lifecycle
- document reconciliation

This pattern should now be treated as a platform-level contract:
- validate
- apply
- audit
- refresh

The more derived modules Nexus gains, the more important this becomes.

---

## 9. Expansibility findings by module type

### 9.1. Project manager
The backend already supports an operational PM-like layer relatively well.
This is a good proof of schema flexibility, but not the most revealing future direction.

### 9.2. CRM
A light relational CRM is feasible, especially in an agent-first model.
However, a commercial CRM would require stronger stage, ownership, and timeline semantics.

### 9.3. Embedding layer
This is one of the most promising expansion tests.
Embeddings fit the current backend well as an auxiliary semantic-retrieval layer.

### 9.4. BI / cognitive observability
This is likely the most strategically aligned next expansion.
It directly addresses the human test and makes visible what already exists structurally.

### 9.5. Second-brain visual layer
This is highly aligned with the product thesis, but depends more on UI/read-model work than on schema expansion.

---

## 10. Strategic interpretation

The expansibility analysis suggests that the most promising near-future direction is not a vertical application module such as CRM or PM.

The most promising direction is:

- **BI / cognitive observability**
- **embedding-based semantic retrieval**
- **human-cognitive read surfaces**

This is because these directions:
- reinforce the actual thesis of Nexus;
- reuse the current backend well;
- improve the shared surface between human and agent;
- avoid prematurely locking Nexus into a narrow vertical identity.

---

## 11. What should not be prioritized next

Based on the combined analysis, the following should not be prioritized next:

- broad new domain modules before core clarification;
- React/Vite/frontend stack replacement;
- multi-user or auth-heavy operation;
- heavy ontology refactoring;
- large workflow expansion unrelated to current comprehension issues;
- vertical productization (CRM/PM full modules) before read-model and human-cognitive improvements.

---

## 12. Recommended next moves

### 12.1. Product-level recommendation
The next product move should be a **human comprehension pass**, not a feature expansion pass.

Focus:
- clarify the work model;
- improve layout and information hierarchy;
- make cycle/activity/document logic legible;
- improve the human reading surface.

### 12.2. Core-level recommendation
The next core move should be an **expansibility pass**, focused on:
- core vs derived boundaries;
- read-model layer;
- mutation contract;
- type/capability clarity.

### 12.3. Strategic recommendation
Treat Nexus, for now, as:
- **agent-first**
- **human-supervised**
- evolving toward a richer human-cognitive layer.

This is more honest and more aligned with observed behavior than treating it as already human-first.

---

## 13. Consolidated requirement priorities

### Priority 1
Improve human comprehension of the existing product:
- hierarchy
- labels
- layout
- cycle-centered model
- reduce confusion

### Priority 2
Clarify the platform core:
- core vs derived
- read-model layer
- mutation pattern
- type/capability policy

### Priority 3
Advance the human-cognitive layer:
- dashboard
- kanban
- timeline
- graph-like relation view

### Priority 4
Explore semantic enrichment:
- embeddings
- related context
- semantic retrieval

### Priority 5
Only then explore broader derived modules:
- PM
- CRM
- case management

---

## 14. Final conclusion

The recent sprint sequence produced a technically credible local-first system.

However, the human test showed that the limiting factor has shifted:

> the bottleneck is no longer missing backend capability;
> the bottleneck is whether the human can read, trust, and think through the same surface that the agent already uses operationally.

This changes the product agenda.

Nexus should now be treated as a shared operational substrate whose next phase must emphasize:
- human comprehension,
- cognitive observability,
- and explicit platform boundaries.

That is the condition for expanding safely without losing the product’s identity.