	# 🔧 BUILDER SPEC — Nexus Graph Control System v1

**Inspiration reference (mandatory reading):**  
[https://help.obsidian.md/plugins/graph](https://help.obsidian.md/plugins/graph?utm_source=chatgpt.com)

Do NOT copy UI.  
Replicate interaction philosophy + control mechanics adapted to Nexus ontology.

---

## 🎯 Goal

Upgrade current MAP from:

> visual relational diagram  
> to  
> operator-controlled relational field

User must **govern what exists in the graph**, not only what is highlighted.

Current Nexus graph:

- semantic modes OK
    
- visual control weak
    
- investigation depth missing
    
- relation filtering insufficient
    
- physics control underexposed
    

This spec fixes that.

---

## 🧠 Core UX Model (Hybrid)

Nexus MAP must operate with TWO layers:

### Layer 1 — Cognitive Modes (existing)

Presets:

- SIGNAL
    
- STRUCTURE
    
- PRESSURE
    
- TRACE
    

These remain semantic interpretation modes.

### Layer 2 — Field Control System (NEW)

User directly controls:

- graph depth
    
- entity visibility
    
- relation visibility
    
- physics behavior
    
- visual density
    
- layout compactness
    

This is NOT aesthetic.  
This is **epistemic control**.

---

## 🌍 Field Regimes

Introduce two graph regimes:

### 1️⃣ GLOBAL FIELD

Full workspace topology.

Used for:

- orientation
    
- system reading
    
- macro pressure perception
    

### 2️⃣ FOCUSED FIELD

Triggered when node clicked.

Behavior:

- clicked node becomes gravitational center
    
- graph recenters smoothly
    
- neighborhood rendered by depth
    

Depth selector:

- ALL
    
- 1 HOP
    
- 2 HOPS
    
- 3 HOPS
    

Implementation rule:  
Depth filtering must REMOVE nodes from field, not only fade.

---

## 🧭 Focus Mechanics (Critical)

On node click:

System must:

1. Recenter graph
    
2. Recompute layout
    
3. Apply depth filter
    
4. Maintain visual continuity
    
5. Reduce global noise
    

No modal switch.  
No new page.  
Same field transforms.

User must feel:

> "I entered the local world of this object."

---

## 🔎 Entity Filtering (NEW)

Panel section:

### ENTITIES

Toggle visibility:

- cycles
    
- activities
    
- documents
    
- evidence
    
- risks
    
- governance states
    
- decisions
    
- traces
    
- agents
    
- external entities
    

Behavior:

Toggle = remove from graph topology.  
Not opacity.

Graph must recompute layout after change.

---

## 🔗 Relation Filtering (Nexus advantage)

Panel section:

### RELATIONS

Toggle:

- blocks
    
- supports
    
- requires
    
- impacts
    
- references
    
- owns
    
- governs
    
- validates
    
- contradicts
    
- escalates
    

Filtering rule:

When relation disabled:

- edge removed
    
- dependent nodes optionally removed if isolated
    

Must be configurable:  
✔ remove isolated nodes  
✔ keep isolated nodes

---

## 🎛️ Field Controls (Obsidian-like but structured)

Panel section:

### VIEW

Controls:

- label density
    
- node size
    
- link thickness
    
- relation label visibility
    
- hover reveal intensity
    

---

### LAYOUT

Controls:

- compact
    
- balanced
    
- spread
    

These are presets mapping to physics params.

---

### FORCES (advanced — collapsible)

Sliders:

- center force
    
- repulsion force
    
- link force
    
- link distance
    

Implementation:  
Client side physics engine only.

No backend changes.

---

## 🔁 Dynamic Focus Continuity

When depth changes:

Graph must:

- animate topology change
    
- maintain spatial memory
    
- avoid hard redraw
    

Important:  
No jarring recomposition.

This is essential for:

> cognitive continuity

---

## 🎨 Visual Semantics Upgrade

Nodes:

Color by ontology type.

Edges:

Styled by relation type:

Example mapping:

blocks → thick + red tint  
supports → soft + green  
requires → dashed  
impacts → glow  
references → thin  
owns → stable neutral

Do NOT rely on color only.  
Use stroke + opacity + texture.

---

## 🧠 Graph Interpretation Philosophy

Builder must understand:

This is NOT a knowledge graph explorer.

This is:

> operational reasoning surface

Therefore:

- visual calm > feature density
    
- transformation > navigation
    
- field continuity > screen switching
    
- investigation > browsing
    

---

## 🚫 Anti-Goals

Do NOT:

- add graph legends panel
    
- add mini dashboards inside graph
    
- add force-directed gimmicks
    
- add 3D
    
- add node animation noise
    
- add color explosion
    
- add graph background grid
    

Graph must feel:

> institutional, quiet, sovereign

---

## 🧪 Validation Criteria

Builder must validate manually:

Operator must be able to:

1️⃣ See full system topology  
2️⃣ Click object → enter local reasoning field  
3️⃣ Adjust depth → see causal layers  
4️⃣ Remove relation types → reveal structural truth  
5️⃣ Compress/expand field → reveal pressure dynamics  
6️⃣ Identify blockers without Inspect regime  
7️⃣ Understand system drift visually

If this fails → graph not operational yet.

---

## 📦 Technical Constraint

Must remain:

- server-rendered architecture
    
- same ontology
    
- same endpoints
    
- same cockpit file
    
- no graph backend engine
    
- no new build tooling
    

Everything:  
client side enhancement.

---

## 🔥 Final Design Intent

After this change:

MAP must stop feeling like:

> premium graph widget

and start feeling like:

> operational reasoning instrument