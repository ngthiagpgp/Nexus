# UI North Star - Nexus Cockpit v1

## 1. Purpose

The Nexus UI is not a generic dashboard, not an IDE in disguise, and not a styled database browser.

Its purpose is to provide a shared supervision surface where a human operator and an agent can inspect the same operational reality, reason over the same objects, and intervene on the same workflow without translation through long textual explanations.

## 2. Core Thesis

The Nexus cockpit must allow a human to supervise the same operational reality as the agent, with enough clarity to understand, decide, and intervene without depending on a textual description of the system.

This means the UI must make work legible before it makes structure exhaustive.

## 3. Primary User

The primary user is the human operator-supervisor.

This user is not trying to configure a platform or explore a schema. The user is trying to:

- understand what is currently in focus;
- identify what work is active, blocked, or complete;
- inspect the documents that support or constrain that work;
- verify whether the system state is trustworthy;
- intervene safely when a status, document, or linkage must change.

## 4. Main Job To Be Done

The main job of the Nexus UI is to help the operator:

- understand the current operational focus;
- follow cycles as the organizing frame of work;
- open activities inside the active cycle;
- inspect supporting documents attached to that cycle and its work;
- validate status and integrity states;
- intervene with confidence and traceability.

The UI succeeds when the operator can answer "what is happening, what matters now, and what can I safely change?" without reading implementation details.

## 5. Operational Unit

The current operating hypothesis for Nexus is:

- `cycle` is the primary operational unit;
- `activity` is the work unit that lives inside a cycle;
- `document` is evidence, instruction, or support material connected to the work of a cycle.

This hierarchy matters. The cockpit should not flatten cycles, activities, and documents into equivalent lists. It should show them as different layers of the same operational frame.

## 6. Design Principles

### First work, then structure

The UI should show what work is underway before it shows the full structural inventory of the workspace.

### First focus, then context

The active cycle and its immediate operational state should be visible before secondary context such as entities, counts, or audit details.

### First active object, then inventory

A selected cycle, activity, or document should be more prominent than the raw inventory around it.

### First action and evidence, then metadata

The operator should see what the object is for, what state it is in, and what evidence supports it before seeing technical metadata, ids, or internal fields.

### Human-legible without betraying technical truth

The UI must simplify presentation, not falsify reality. Technical truth must remain available, but it should not dominate the first reading.

### Governance visible but not dominant

Auditability, integrity, and lifecycle controls are essential, but they must remain subordinate to the main work path rather than overwhelming it.

## 7. Canonical Views

### Operational Focus View

This view answers: what cycle is active, what is the current operational focus, and what matters now.

It should contain:

- current or focused cycle;
- high-signal operational status;
- immediate counts that help orientation;
- the next actionable focus.

It should not become a dense inventory or an audit log wall.

### Work Flow View

This view answers: what work exists inside the selected cycle and how it is moving.

It should contain:

- activities grouped or ordered in a human-comprehensible way;
- supporting documents linked to the same cycle;
- status contrast across work objects.

It should not collapse work and support material into one undifferentiated list.

### Inspection View

This view answers: what exactly is selected, what does it mean, and what can I do with confidence.

It should contain:

- selected activity details;
- selected document details and readable preview;
- status and integrity controls where appropriate;
- enough context to support a decision.

It should not read like a schema dump.

### Structural Context View

This view answers: what wider context exists around the active operational work.

It should contain:

- entities and relations relevant to orientation;
- secondary reference material;
- governance traces that support trust.

It should not compete with the main operational flow.

## 8. Information Hierarchy

### Primary elements

- current cycle;
- active or blocked activities;
- relevant supporting document;
- next actionable focus.

### Secondary elements

- workspace summary;
- reference entities;
- aggregate counts;
- recent but non-critical context.

### Tertiary elements

- raw ids;
- schema version;
- integrity internals;
- audit detail;
- technical metadata.

Primary information should shape the page. Secondary information should support interpretation. Tertiary information should stay available without dominating the screen.

## 9. What Good Looks Like

A good Nexus UI makes the operator immediately understand where work is happening, what object is active, what document supports that work, and where intervention is safe.

It does not require the user to reverse-engineer the data model from the screen. It does not rely on raw labels to communicate hierarchy. It does not confuse supervision with passive reporting.

If the cockpit is working well, a human can enter, orient in seconds, follow the cycle-to-work chain, inspect evidence, and act without feeling that they are navigating a developer tool.

## 10. Quality Tests

### Orientation test

Within a few seconds, the user should be able to identify the active cycle, the current state of work, and where to start.

### Focus test

The screen should make it obvious what object currently deserves attention and why.

### Flow test

A user should be able to move from cycle to activity to supporting document without losing context.

### Inspection test

Once an object is selected, the detail area should reduce ambiguity rather than adding density.

### Governance test

Audit and integrity information should be available when needed, but should not dominate first-read cognition.

### Spatial memory test

The user should learn where key information lives and find it again consistently across sessions and iterations.

## 11. Anti-Goals

The Nexus UI must not become:

- a generic admin panel;
- a BI clone;
- an IDE-like surface;
- a raw database viewer with cosmetic polish;
- a governance-heavy screen that hides the work itself.

These patterns may expose information, but they do not solve the supervision problem Nexus exists to solve.

## 12. Consequences for Future Iterations

Future UI iterations should:

- strengthen cycle-first orientation rather than weakening it;
- reduce repeated explanation once hierarchy becomes visually self-evident;
- quiet tertiary metadata without hiding it;
- make selected-object inspection more readable than list browsing;
- preserve governance as a trusted secondary layer;
- evaluate every new component by whether it improves supervision of shared operational reality.

Possible future views such as graph, timeline, or board surfaces should only be introduced if they clarify the same operational model rather than replacing it with a different one.
