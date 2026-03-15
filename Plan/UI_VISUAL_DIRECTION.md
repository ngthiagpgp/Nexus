# UI Visual Direction - Obsidian-like Analytical Cockpit

## 1. Intent

"Obsidian-like" in Nexus does not mean copying Obsidian's interface literally.

It means inheriting the qualities that make an environment suitable for thought, inspection, and structured reading:

- dark by default;
- sober rather than decorative;
- modular rather than flat;
- dense enough for analysis, but still readable;
- supportive of long inspection sessions.

The target is an analytical cockpit, not a note-taking app clone.

## 2. Desired Feel

The cockpit should feel:

- calm;
- dark;
- modular;
- analytical;
- trustworthy;
- low-noise;
- operational rather than decorative.

The interface should suggest that the user is entering a serious supervision surface, not a marketing shell or a settings console.

## 3. Visual Principles

### Dark mode by default

The visual baseline should assume a dark environment suitable for prolonged inspection and reading.

### Restrained accent color use

Accent color should signal selection, state, or urgency. It should not become a branding layer spread across every component.

### Layered surfaces with subtle separation

Panels should feel distinct through tonal contrast, spacing, and border logic rather than loud ornament.

### Typography optimized for scan and reading

The UI must support both quick scanning and slower inspection of operational content.

### Metadata visually secondary

Ids, schema markers, file paths, timestamps, and integrity internals should remain quiet unless they are the reason the user is looking.

### Content area comfortable for reading

Document previews and detail areas must feel like reading surfaces, not just cards full of fields.

### Emphasis on current focus

The currently relevant operational object should be visually easier to detect than the surrounding context.

### Cards as functional blocks, not ornamental widgets

Blocks should exist to separate meaning and action. They should not exist merely to produce a dashboard aesthetic.

## 4. Semantic Use of Color

Color should primarily indicate:

- status;
- warning;
- selection;
- emphasis.

It should not be used as a decorative blanket.

Suggested semantic pattern:

- neutral tones for structure and inactive context;
- restrained emphasis color for selected or active focus;
- warning color for risky, inconsistent, or blocked states;
- success or resolved color only when it conveys operational meaning.

If color disappears, the hierarchy should still remain understandable through structure and typography.

## 5. Typography and Density

Titles should orient, not decorate. They should tell the user what the panel is for.

Technical ids should appear only when they add trust or disambiguation. They should rarely be the primary label.

To avoid the generic admin-panel look:

- do not put equal typographic weight on every label;
- do not present all fields as uniform key-value rows;
- do not let raw status chips replace explanatory structure.

Density should be deliberate:

- enough information to support supervision;
- not so much repetition that the screen becomes visually heavy;
- not so little context that the user must click constantly to understand the current object.

## 6. Panel Logic

### Navigation column

This area should orient the operator toward the current work frame, especially the active cycle and its immediate workflow.

### Operational center

This is the main reading and navigation surface. It should contain the work path and the supporting material that belong to the active cycle.

### Selected detail panel

This area should deepen understanding of the selected object, clarify safe actions, and provide readable inspection context.

### Secondary governance areas

Audit and related governance surfaces should remain accessible but visually subordinate to the work path.

## 7. Reading Surfaces

Documents, previews, and inspections should feel closer to reading panes than to database rows.

This means:

- enough width and spacing to read text;
- clear section headers;
- lifecycle and integrity controls near the document, not isolated as detached metadata;
- preview content treated as content, not as another field.

The operator should feel invited to inspect, not forced to decode.

## 8. Do / Don't

### Do

- highlight the active operational object;
- keep metadata quiet;
- separate context from action;
- make support material readable;
- use panel contrast to communicate hierarchy;
- make the cycle-first model obvious in layout and language.

### Don't

- flatten all panels into one visual layer;
- give equal visual weight to everything;
- expose raw ids as the main labels;
- overload the home with repeated explanatory blocks;
- let audit compete with the main work path.

## 9. Implications for UI Passes

Phase 2 and later UI passes should use this direction to decide:

- which panels deserve stronger visual emphasis;
- which metadata should be quieter or collapsible;
- where repetition is still helping and where it has become noise;
- how far dark analytical styling should go before it turns theatrical;
- how to make future surfaces more inspectable without becoming tool-like clutter.

Future mockups or UI passes should be reviewed against this document before micro-polish work continues.
