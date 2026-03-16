# Nexus UI Contract System — v2

## Premissa
O Nexus não deve mais ser especificado como um conjunto de telas. Deve ser especificado como um sistema de presença operacional: um ambiente relacional onde espaço, estado, evidência, risco e julgamento se tornam legíveis sem colapsar em dashboard.

Este sistema substitui mockups como autoridade primária. Sua função é permitir que um humano e outro agente entendam, critiquem e implementem o produto sem improvisar sua lógica profunda.

A unidade central não é a página. A unidade central é o regime cognitivo.

---

# 0. Arquitetura do sistema

```text
nexus-ui-system/
  00_constitution/
    00_product_thesis.md
    01_world_model.md
    02_spatial_doctrine.md
    03_visual_grammar.md
    04_attention_regimes.md
    05_persistence_policy.md
    06_map_doctrine.md

  01_views/
    overview.md
    map_immersion.md
    map_focus.md
    flow.md
    inspect_activity.md
    inspect_document.md
    inspect_governance.md
    audit_narrative.md
    crisis_mode.md

  02_entities/
    cycle.md
    activity.md
    document.md
    evidence.md
    risk.md
    governance.md
    relation.md
    trace.md

  03_states/
    calm.md
    tension.md
    crisis.md
    investigation.md
    blocked.md
    unresolved.md
    empty.md
    loading.md

  04_components/
    node.md
    edge.md
    overlay.md
    context_rail.md
    inspect_surface.md
    minimal_card.md
    audit_cluster.md
    event_chain.md
    filter_surface.md
    command_bar.md

  05_interactions/
    hover_probe.md
    click_focus.md
    expand_neighborhood.md
    isolate_subgraph.md
    inspect_evidence.md
    switch_regime.md
    apply_filter.md
    open_trace.md

  06_blueprints/
    overview_scan.yaml
    map_immersion.yaml
    map_focus.yaml
    inspect_document.yaml
    audit_narrative.yaml
    crisis_mode.yaml

  07_review/
    critique_protocol.md
    anti_patterns.md
    freeze_criteria.md
    builder_notes.md
```

---

# 1. Constituição

## `00_product_thesis.md`

```md
# Product Thesis

## Core claim
Nexus is a relational command surface for operational interpretation.

## Product promise
It makes structure visible before action, consequence legible before escalation, and judgment possible before intervention.

## What makes it different
Nexus does not treat work as isolated items moving across panels. It treats institutional reality as a field of entities, relations, evidence, risks, decisions, and traces.

## What the interface must feel like
- Serious without bureaucracy
- Premium without decoration
- Dense without compression
- Relational without chaos
- Quiet without emptiness

## Non-negotiables
- MAP is the dominant cognitive field.
- Detail appears by intention, not by default.
- Support UI cannot compete with the center.
- Space is semantic.
- Relations are native, not supplemental.
```

## `01_world_model.md`

```md
# World Model

## What exists in the Nexus world
- Cycles
- Activities
- Documents
- Evidence
- Risks
- Governance states
- Decisions
- Traces
- Relations between all of the above

## Core ontological law
Nothing important in Nexus is fully meaningful in isolation.
Meaning emerges through relation, state, sequence, and consequence.

## What changes over time
- State
- Priority
- Legitimacy
- Risk pressure
- Evidence context
- Dependency structure
- Audit trace

## What the UI must reveal
- What is central now
- What is connected
- What is changing
- What is at risk
- What has evidence
- What leaves a trace

## Rule of representation
The interface should not merely list world objects. It should reveal the world structure they inhabit.
```

## `02_spatial_doctrine.md`

```md
# Spatial Doctrine

## Primary law
The center belongs to reasoning.
In Nexus, the center belongs to MAP whenever the task involves relation, evidence, dependency, risk, or judgment.

## Secondary law
Periphery exists to orient, filter, inspect, and support. It must never rival the center.

## Spatial hierarchy
1. Center field
2. Active overlay or inspect surface
3. Context rail
4. Global command/navigation
5. Utility controls

## Fixed elements
- Top band
- Center field
- Minimal rail anchors

## Collapsible elements
- Left rail
- Right rail
- Support surfaces

## Floating elements
- Hover probes
- Quick overlays
- Filter surfaces
- Physics / density controls

## Rule of failure
If the eye reads the layout as blocks before it reads the center as field, the product has collapsed into dashboard logic.
```

## `03_visual_grammar.md`

```md
# Visual Grammar

## Tone
Institutional. Restrained. Precise. Contemporary.

## Character sources
- Consequence from Palantir-like operational seriousness
- Discipline from Linear-like visual restraint
- Relational depth from Obsidian-like connectedness
- Gravity from situation-room atmosphere

## What premium means
- Silence over flourish
- Precision over decoration
- Contrast over noise
- Depth over gloss
- Material restraint over spectacle

## Color law
Color is semantic before branded.
Color must indicate state, pressure, legitimacy, evidence, and escalation.

## Typography law
Typography clarifies order and weight. It must not perform personality.

## Surface law
Surfaces should feel dry, controlled, and layered. Not glossy. Not playful. Not ornamental.

## Rule of failure
If the interface reads like polished SaaS, the grammar is wrong.
```

## `04_attention_regimes.md`

```md
# Attention Regimes

## Overview / Scan
Purpose: orient fast.
Center: summary structure.
Detail policy: suppressed.
Space behavior: stable, sparse, legible.

## MAP / Immersion
Purpose: think through relation.
Center: graph field.
Detail policy: layered by focus and intent.
Space behavior: center sovereign, rails reduced.

## Inspect
Purpose: judge a selected object in context.
Center: semantic analysis surface.
Detail policy: active object privileged, surrounding context quiet.
Space behavior: continuous field, not modular panels.

## Audit
Purpose: reconstruct meaningful institutional sequence.
Center: event chain / grouped narrative.
Detail policy: causal and evidentiary links foregrounded.
Space behavior: narrative continuity over row repetition.

## Crisis
Purpose: elevate urgency without losing control.
Center: critical structure under pressure.
Detail policy: suppress non-essential context.
Space behavior: sharpened contrast, reduced ambiguity.
```

## `05_persistence_policy.md`

```md
# Persistence Policy

## Always visible
- Current regime
- Current scope
- Dominant state
- Center structure
- Minimal command anchors

## Visible on focus
- Node identity
- Active relations
- Selected object state
- Immediate dependencies

## Visible on intention
- Evidence detail
- Document excerpt
- Relation explanation
- Metadata depth
- Advanced controls

## Normally hidden
- Dense support metadata
- Secondary traces
- Rarely used utilities
- Explanatory helper text

## Rule of sophistication
Premium products do not expose everything. They preserve depth as potential.

## Rule of failure
If detail feels present before it feels needed, persistence is too high.
```

## `06_map_doctrine.md`

```md
# MAP Doctrine

## What MAP is
MAP is not a widget, tab, or visualization module.
It is the primary cognitive environment of Nexus.

## What MAP must do
- Reveal structure
- Support navigation by relation
- Expose consequence
- Organize focus
- Carry evidence into context
- Make risk and governance pressure perceptible

## What MAP must feel like
- Expansive
- Traversable
- Consequential
- Layered
- Alive but controlled

## What MAP must not become
- Decorative graph field
- Data wallpaper
- Feature demo
- Static topology poster

## Rule of dominance
When MAP is active, every other interface element becomes support.

## Rule of failure
If the user feels they are looking at the graph instead of thinking inside it, MAP is underdesigned.
```

---

# 2. Contratos de vista

## Universal template

```md
# View Contract — <name>

## Purpose

## User mental mode

## Primary question answered fast

## Regime
Overview / MAP / Inspect / Audit / Crisis

## Center of gravity

## Fixed zones
- 

## Collapsible zones
- 

## Floating zones
- 

## Primary actions
- 

## Secondary actions
- 

## Required components
- 

## Required entities visible
- 

## States supported
- 

## Always visible
- 

## Visible on focus
- 

## Visible on intention
- 

## Anti-patterns
- 

## Failure condition

## Success condition

```

## `map_immersion.md`

```md
# View Contract — MAP Immersion

## Purpose
Let the user perceive the living relational structure of the current operational world.

## User mental mode
Exploring, orienting, tracing, interpreting.

## Primary question answered fast
What matters here, what is connected, and where is structural pressure accumulating?

## Regime
MAP

## Center of gravity
A sovereign graph field.

## Fixed zones
- Top command band
- Center graph field
- Minimal rail anchors

## Collapsible zones
- Scope rail
- Inspect rail
- Filter support

## Floating zones
- Hover probe
- Quick overlay
- Filter surface
- Physics / density controls

## Primary actions
- Focus node
- Expand neighborhood
- Isolate subgraph
- Filter by relation or type
- Inspect evidence

## Secondary actions
- Freeze layout
- Highlight path
- Change density
- Switch regime

## Required components
- Node
- Edge
- Overlay
- Context rail
- Filter surface
- Command bar

## Required entities visible
- Relations
- Selected scope
- Dominant state
- Active nodes of current field

## States supported
- Calm
- Tension
- Investigation
- Crisis

## Always visible
- Current regime
- Scope
- Graph field
- Dominant state

## Visible on focus
- Immediate neighborhood
- Active relation types
- Node identity

## Visible on intention
- Evidence detail
- Full relation explanation
- Metadata depth
- Advanced controls

## Anti-patterns
- Cards inside center field
- Exposed metadata walls
- Rail dominance
- Decorative motion
- Overframed graph area

## Failure condition
The graph feels contained, observed, or auxiliary.

## Success condition
The graph feels like the world itself, and everything else reads as support.
```

## `inspect_document.md`

```md
# View Contract — Inspect Document

## Purpose
Allow the user to judge a document as epistemic object in operational context.

## User mental mode
Reading, weighing, comparing, verifying.

## Primary question answered fast
What is this document, why does it matter, what does it support, and how trustworthy is it here?

## Regime
Inspect

## Center of gravity
A semantic analysis surface anchored on the active document.

## Fixed zones
- Top band
- Document analysis field

## Collapsible zones
- Left scope rail
- Right support rail

## Floating zones
- Evidence overlay
- Relation overlay
- Metadata reveal surface

## Primary actions
- Read excerpt
- Inspect linked entities
- Compare evidence
- Trace document relation

## Secondary actions
- Collapse support
- Open source trail
- Shift to MAP focus

## Required components
- Inspect surface
- Overlay
- Context rail
- Event trace link

## Required entities visible
- Document
- Related evidence
- Linked cycle/activity
- State markers

## States supported
- Calm
- Investigation
- Unresolved

## Always visible
- Document identity
- Current status
- Core excerpt / summary
- Immediate relation context

## Visible on focus
- Evidence links
- Governance relevance
- Dependency position

## Visible on intention
- Full metadata
- Document history
- Deep trace

## Anti-patterns
- Modular card pile
- Reading area too small
- Metadata louder than content
- Support rails stealing center

## Failure condition
The user feels they opened a panel collection instead of entering a state of analysis.

## Success condition
The interface feels like a judgment surface, not a dashboard arrangement.
```

## `audit_narrative.md`

```md
# View Contract — Audit Narrative

## Purpose
Reconstruct institutional memory as meaningful sequence, not raw log.

## User mental mode
Rebuilding causality, tracing change, understanding consequence.

## Primary question answered fast
What happened, why did it matter, and what changed as a result?

## Regime
Audit

## Center of gravity
Narrative event chain grouped by meaning.

## Fixed zones
- Top band
- Narrative field

## Collapsible zones
- Filter rail
- Linked entity rail

## Floating zones
- Event detail overlay
- Evidence reveal
- Relation trace

## Primary actions
- Expand event chain
- Group by semantic transition
- Open evidence
- Trace consequence

## Secondary actions
- Narrow scope
- Change grouping
- Switch to MAP or Inspect

## Required components
- Audit cluster
- Event chain
- Overlay
- Context rail

## Required entities visible
- Event groups
- Transitions
- Key actors / objects
- Evidence anchors

## States supported
- Calm
- Tension
- Crisis

## Always visible
- Scope
- Time range
- Main chain
- Key transition markers

## Visible on focus
- Selected event detail
- Immediate linked objects
- Local causal chain

## Visible on intention
- Full evidence references
- Full trace depth
- Secondary event groups

## Anti-patterns
- Raw log feel
- Uniform event repetition
- Spreadsheet chronology
- Narrative without causality

## Failure condition
The user receives information but not interpretation.

## Success condition
The user can reconstruct meaningful institutional memory with low effort.
```

---

# 3. Contratos de entidade

## Universal template

```md
# Entity Contract — <name>

## What it is in the world

## Why it matters

## Required visible identity
- 

## Required relations
- 

## Required state signals
- 

## Optional depth
- 

## Risk of misrepresentation

## Rule of display

```

## `document.md`

```md
# Entity Contract — Document

## What it is in the world
A document is not merely a file. It is an evidentiary or operational object embedded in process and consequence.

## Why it matters
Documents support, justify, trigger, record, or constrain action.

## Required visible identity
- Title
- Type
- Current status
- Relevance marker

## Required relations
- Linked activities
- Linked cycle
- Evidence role
- Governance relevance

## Required state signals
- Active / outdated / unresolved / verified

## Optional depth
- Excerpt
- Source detail
- Metadata
- Change history

## Risk of misrepresentation
If displayed as isolated content container, the document loses operational meaning.

## Rule of display
Show the document as situated evidence, not as detached object.
```

## `relation.md`

```md
# Entity Contract — Relation

## What it is in the world
A relation is not line decoration. It is meaningful structure connecting entities.

## Why it matters
Relations carry dependency, support, contradiction, sequence, risk propagation, evidence relevance, or governance implication.

## Required visible identity
- Relation type
- Direction when relevant
- Strength or salience when relevant

## Required relations
- Source entity
- Target entity
- Context of meaning

## Required state signals
- Active / weak / blocked / contested / risk-bearing

## Optional depth
- Explanation
- Evidence anchor
- Historical shift

## Risk of misrepresentation
If treated as generic edge, the graph loses epistemic power.

## Rule of display
Relations must communicate meaning, not merely connectivity.
```

---

# 4. State sheets

## Universal template

```md
# State Sheet — <name>

## Operational meaning

## Atmosphere

## Visual behavior
- contrast:
- color pressure:
- motion:
- density:

## MAP behavior

## Rail behavior

## Overlay behavior

## Action bias

## Failure condition

```

## `calm.md`

```md
# State Sheet — Calm

## Operational meaning
The system is stable and intelligible. No acute pressure dominates interpretation.

## Atmosphere
Open, controlled, breathable.

## Visual behavior
- contrast: moderate
- color pressure: low
- motion: minimal
- density: low to medium

## MAP behavior
Topology remains legible and unforced. Focus can emerge without urgency.

## Rail behavior
Rails stay quiet and low-emphasis.

## Overlay behavior
Overlays are light, sparse, and optional.

## Action bias
Orient, review, compare.

## Failure condition
Calm turns into flatness or generic product blandness.
```

## `crisis.md`

```md
# State Sheet — Crisis

## Operational meaning
The system is under meaningful pressure. Consequence and escalation are active.

## Atmosphere
Sharpened, tense, controlled, high-stakes.

## Visual behavior
- contrast: elevated around critical structures
- color pressure: selective but strong
- motion: minimal and decisive
- density: compressed around urgency, suppressed elsewhere

## MAP behavior
Critical nodes, risky relations, and pressure paths gain priority.

## Rail behavior
Only essential support remains loud enough to matter.

## Overlay behavior
Urgent detail becomes easier to reveal; non-essential detail stays buried.

## Action bias
Isolate, assess, intervene.

## Failure condition
Crisis becomes theatrical instead of precise.
```

---

# 5. Contratos de componente

## Universal template

```md
# Component Contract — <name>

## Function

## Why it exists

## Minimum structure
- 

## Allowed content
- 

## Forbidden content
- 

## States
- default
- hover
- active
- muted
- disabled

## Visual priority
Primary / Secondary / Tertiary

## Usage rules
- 

## Common failure
- 

```

## `node.md`

```md
# Component Contract — Node

## Function
Represent an operational entity inside the relational field.

## Why it exists
The graph needs meaningful anchors of world structure.

## Minimum structure
- Title or short label
- Type signal
- State signal

## Allowed content
- Identity
- One state cue
- One type cue

## Forbidden content
- Dense metadata
- Long descriptions
- Multi-section mini panels
- Heavy action menus by default

## States
- default
- hover
- focused
- selected
- muted
- risk-elevated
- evidence-linked

## Visual priority
Primary inside MAP.

## Usage rules
- Identity must be readable fast.
- Detail should move to overlay.
- State should be perceptible without visual overload.

## Common failure
Node becomes a card and destroys graph legibility.
```

## `inspect_surface.md`

```md
# Component Contract — Inspect Surface

## Function
Create a continuous semantic field for analysis of an active object.

## Why it exists
Inspect mode should feel like entering a state of judgment, not opening modular panels.

## Minimum structure
- Active object identity
- Central reading or analysis area
- Immediate relation context
- Quiet support zone

## Allowed content
- Core excerpt
- Semantic highlights
- Relation anchors
- Evidence cues

## Forbidden content
- Dashboard KPI clusters
- Repeated cards
- Dense chrome
- Excessive rail competition

## States
- default
- focused
- unresolved
- evidence-open

## Visual priority
Primary in Inspect regime.

## Usage rules
- Must read as surface, not layout assembly.
- Must preserve continuity across sections.
- Must privilege thought over container logic.

## Common failure
Inspect looks like three aligned panels with better styling.
```

## `overlay.md`

```md
# Component Contract — Overlay

## Function
Reveal detail without breaking the sovereignty of the active field.

## Why it exists
Nexus needs depth without persistent clutter.

## Minimum structure
- Anchor context
- Title
- Core detail block
- Dismiss action

## Allowed content
- Relation explanation
- Evidence preview
- Node detail
- Quick metadata

## Forbidden content
- Full workflows
- Large editing surfaces
- Permanent navigation
- Dense dashboards

## States
- preview
- active
- pinned
- dismissed

## Visual priority
Secondary by default, elevated only in direct service of center reasoning.

## Usage rules
- Triggered by intention
- Fast to dismiss
- Lightweight in structure
- Never becomes layout backbone

## Common failure
Overlay becomes pseudo-panel and starts occupying permanent mental space.
```

---

# 6. Scripts de interação

## Universal template

```md
# Interaction Script — <name>

## Trigger

## Immediate response

## Visual response

## Cognitive effect

## Persistence

## Exit condition

## Error to avoid

```

## `click_focus.md`

```md
# Interaction Script — Click Focus

## Trigger
User clicks a node or meaningful entity anchor.

## Immediate response
The object becomes the active center and the surrounding relational field reorganizes around it.

## Visual response
- Focus emphasis appears
- Relevant edges strengthen
- Peripheral field dims but remains legible
- Optional overlay or inspect path becomes available

## Cognitive effect
The user understands what is central, what is adjacent, and where consequence propagates.

## Persistence
Focus remains until replaced, cleared, or converted into Inspect.

## Exit condition
User clears focus, shifts focus, or changes regime.

## Error to avoid
Chaotic reflow, overexposed detail, or loss of global orientation.
```

## `isolate_subgraph.md`

```md
# Interaction Script — Isolate Subgraph

## Trigger
User activates isolate on a focused node, relation, or filter set.

## Immediate response
The relevant subgraph gains sovereignty while non-relevant topology recedes.

## Visual response
- Subgraph remains high legibility
- Surrounding field dims strongly or disappears
- Context label clarifies isolation scope

## Cognitive effect
The user can think locally without losing trust in the larger world model.

## Persistence
Isolation remains until reset or scope change.

## Exit condition
User exits isolation, changes filter, or returns to full field.

## Error to avoid
Isolation feeling like navigation away from the world instead of local concentration within it.
```

---

# 7. Blueprints estruturais

## Convenção
Os YAMLs abaixo não são código. São contratos de estrutura, prioridade e presença para handoff.

## `map_immersion.yaml`

```yaml
view: map_immersion
regime: map
purpose: think inside relational structure
center_of_gravity: sovereign_graph_field
layout:
  top_band:
    role: fixed
    priority: secondary
    contents:
      - regime_identity
      - scope
      - dominant_state
      - primary_commands
  left_rail:
    role: collapsible
    priority: tertiary
    contents:
      - navigation_anchor
      - filter_summary
      - scope_selector
  center_field:
    role: primary
    priority: absolute
    contents:
      - active_graph
      - topology
      - active_focus
      - neighborhood
      - pressure_paths
  right_rail:
    role: contextual
    priority: secondary
    contents:
      - active_inspect_anchor
      - evidence_links
      - governance_pressure
  floating_surfaces:
    role: transient
    priority: secondary
    contents:
      - hover_probe
      - detail_overlay
      - filter_surface
      - density_controls
persistence:
  always_visible:
    - regime_identity
    - scope
    - dominant_state
    - graph_field
  on_focus:
    - node_identity
    - immediate_relations
    - local_state
  on_intention:
    - evidence_detail
    - relation_explanation
    - metadata_depth
    - advanced_controls
anti_patterns:
  - framed_graph_container
  - cards_in_center
  - dense_persistent_metadata
  - loud_rails
  - ornamental_motion
success_condition: user feels they are thinking inside the graph
```

## `inspect_document.yaml`

```yaml
view: inspect_document
regime: inspect
purpose: judge a document in operational context
center_of_gravity: semantic_analysis_surface
layout:
  top_band:
    role: fixed
    contents:
      - regime_identity
      - object_identity
      - status
  left_rail:
    role: collapsible
    contents:
      - scope
      - linked_entities
  center_field:
    role: primary
    contents:
      - document_surface
      - core_excerpt
      - semantic_markers
      - relation_context
  right_rail:
    role: quiet_support
    contents:
      - evidence_links
      - governance_relevance
      - trace_anchor
  floating_surfaces:
    role: transient
    contents:
      - metadata_reveal
      - relation_overlay
      - evidence_preview
persistence:
  always_visible:
    - object_identity
    - status
    - core_content
    - immediate_context
  on_focus:
    - linked_evidence
    - dependency_position
  on_intention:
    - metadata_depth
    - source_history
    - full_trace
anti_patterns:
  - modular_panel_composition
  - small_reading_area
  - metadata_louder_than_content
  - dashboard_kpi_logic
success_condition: the user feels inside a state of judgment
```

## `audit_narrative.yaml`

```yaml
view: audit_narrative
regime: audit
purpose: reconstruct institutional sequence with meaning
center_of_gravity: grouped_event_chain
layout:
  top_band:
    role: fixed
    contents:
      - regime_identity
      - scope
      - time_range
  left_rail:
    role: collapsible
    contents:
      - filters
      - entity_scope
  center_field:
    role: primary
    contents:
      - narrative_groups
      - transition_markers
      - event_chain
      - causal_links
  right_rail:
    role: contextual
    contents:
      - selected_event_detail
      - evidence_refs
      - linked_objects
  floating_surfaces:
    role: transient
    contents:
      - event_overlay
      - trace_reveal
persistence:
  always_visible:
    - scope
    - main_chain
    - transition_markers
  on_focus:
    - local_event_detail
    - nearby_causes
    - nearby_effects
  on_intention:
    - secondary_trace_depth
    - full_evidence_refs
anti_patterns:
  - raw_log_feel
  - repetitive_rows
  - spreadsheet_timeline
  - ungrouped_event_mass
success_condition: user understands what happened and why it mattered
```

---

# 8. Protocolo de crítica

## `critique_protocol.md`

```md
# Critique Protocol

## 1. Ontology
- Does the interface reveal a world or merely objects?
- Are relations meaningful or merely visible?
- Is consequence perceptible?

## 2. Presence
- Does the product feel like a cognitive environment?
- Does the center impose itself naturally?
- Does the interface feel inevitable rather than assembled?

## 3. Spatial order
- Is the center readable in under 3 seconds?
- Are rails subordinate?
- Does whitespace protect thought?

## 4. Persistence
- Is essential state visible?
- Is depth preserved as potential?
- Does detail appear only when needed?

## 5. Regime integrity
- Is it obvious whether the user is scanning, immersing, inspecting, auditing, or managing crisis?
- Does each regime alter space and emphasis meaningfully?

## 6. MAP quality
- Does the graph feel traversable?
- Does it feel alive but controlled?
- Does it carry analytical power, not just topology?

## 7. Product character
- Does it avoid admin-panel energy?
- Does it avoid note-workspace energy?
- Does it avoid ornamental graph energy?
```

## `anti_patterns.md`

```md
# Anti-patterns

## Dashboard fragmentation
Thinking is broken into competing blocks.

## Graph containment
The MAP feels framed, boxed, or auxiliary.

## Metadata inflation
Detail persists before it becomes necessary.

## Rail inflation
Peripheral support becomes spatial rival.

## Module addiction
Inspect and Audit feel like panel compositions instead of cognitive states.

## Ontological thinness
The interface shows objects but not the world they inhabit.

## Premium mimicry
The interface borrows aesthetics of sophistication without real control of density, hierarchy, and consequence.
```

## `freeze_criteria.md`

```md
# Freeze Criteria

A direction can be frozen only when:

- the world model is perceptible,
- MAP dominance survives across regimes,
- persistence is under control,
- Inspect reads as judgment surface,
- Audit reads as meaningful sequence,
- the UI feels serious without becoming bureaucratic,
- another builder could implement it without inventing hidden logic.
```

## `builder_notes.md`

```md
# Builder Notes

## Implementation priorities
1. Center-first spatial hierarchy
2. Regime clarity
3. Persistence control
4. MAP interaction quality
5. Component restraint
6. Visual polish

## Instructions
- Build world structure before chrome.
- Protect center sovereignty at every breakpoint.
- Prefer overlays to permanent support detail.
- Keep nodes informationally lean.
- Make relations meaningful.
- Make Audit interpretive, not chronological.
- Make Inspect continuous, not modular.

## Decision question
Does this make Nexus feel more like a relational cognitive environment and less like a dashboard?
```

---

# 9. Protocolo operacional

## Workflow
1. Constitution is written.
2. Regimes are defined.
3. View contracts are filled.
4. Entity and component contracts are bound.
5. Blueprints are generated.
6. Human or agent materializes UI.
7. Screenshots return for critique.
8. Critique is made against ontology, regime, persistence, and MAP quality — not against taste.

## Final rule
Nexus should not merely look sophisticated.
It should make sophistication feel structurally necessary.
