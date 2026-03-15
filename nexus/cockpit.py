from __future__ import annotations


def render_cockpit_page() -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Nexus Cockpit</title>
    <style>{_style()}</style>
  </head>
  <body>
    {_body()}
    <script>{_script()}</script>
  </body>
</html>
"""


def _style() -> str:
    return """
:root {
  color-scheme: dark;
  --page: #091119;
  --page-alt: #0e1721;
  --panel: rgba(15, 24, 35, 0.92);
  --panel-alt: rgba(18, 30, 44, 0.92);
  --panel-soft: rgba(12, 20, 30, 0.72);
  --panel-strong: rgba(20, 33, 49, 0.98);
  --line: rgba(114, 141, 173, 0.24);
  --line-strong: rgba(124, 165, 223, 0.34);
  --text: #edf3f8;
  --text-soft: #ccd6e1;
  --text-muted: #8fa0b3;
  --accent: #8db6ff;
  --accent-soft: rgba(141, 182, 255, 0.18);
  --accent-strong: #dce9ff;
  --success: #90d2a7;
  --success-soft: rgba(62, 142, 94, 0.18);
  --warning: #f0c37a;
  --warning-soft: rgba(187, 133, 35, 0.18);
  --danger: #ff9a93;
  --danger-soft: rgba(176, 66, 60, 0.18);
  --shadow: 0 24px 60px rgba(0, 0, 0, 0.34);
  --radius-lg: 22px;
  --radius-md: 16px;
  --radius-sm: 12px;
}

* { box-sizing: border-box; }
html, body { margin: 0; min-height: 100%; }
body {
  font-family: "Aptos", "Segoe UI", system-ui, sans-serif;
  color: var(--text);
  background:
    radial-gradient(circle at 8% 4%, rgba(141, 182, 255, 0.18), transparent 20%),
    radial-gradient(circle at 90% 0%, rgba(113, 157, 214, 0.10), transparent 20%),
    linear-gradient(180deg, #091019 0%, #0d1620 30%, #0f1823 100%);
}
a { color: inherit; }
button, input, select { font: inherit; }

.app-shell {
  max-width: 1600px;
  margin: 0 auto;
  padding: 22px 24px 30px;
}

.top-shell {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 14px;
}

.brand-kicker {
  color: var(--accent);
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  margin-bottom: 8px;
}

.top-shell h1 {
  margin: 0;
  font-size: clamp(2rem, 4vw, 3.4rem);
  line-height: 0.95;
  letter-spacing: -0.04em;
}

.top-shell p {
  margin: 10px 0 0;
  max-width: 760px;
  color: var(--text-muted);
  line-height: 1.55;
}

.workspace-pill {
  padding: 14px 16px;
  min-width: 240px;
  background: linear-gradient(180deg, rgba(141, 182, 255, 0.14), rgba(12, 20, 30, 0.92));
  border: 1px solid rgba(141, 182, 255, 0.26);
  border-radius: var(--radius-md);
  color: var(--accent-strong);
  box-shadow: var(--shadow);
}

.surface {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
  backdrop-filter: blur(10px);
}

.readiness-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  padding: 14px 18px;
  margin-bottom: 14px;
}

.readiness-bar.loading { border-color: rgba(141, 182, 255, 0.24); }
.readiness-bar.ready { border-color: rgba(92, 170, 121, 0.28); }
.readiness-bar.warning { border-color: rgba(187, 133, 35, 0.32); }
.readiness-bar.error { border-color: rgba(176, 66, 60, 0.32); }

.readiness-title {
  font-size: 0.86rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--text-muted);
  margin-bottom: 6px;
}

.readiness-detail {
  color: var(--text-soft);
  line-height: 1.45;
}

.cycle-context-bar {
  display: grid;
  grid-template-columns: 2.2fr repeat(6, 1fr);
  gap: 12px;
  padding: 14px;
  margin-bottom: 14px;
  background: linear-gradient(180deg, rgba(141, 182, 255, 0.10), rgba(18, 30, 44, 0.96));
}

.context-cell {
  padding: 12px 14px;
  background: rgba(9, 16, 24, 0.42);
  border: 1px solid rgba(141, 182, 255, 0.12);
  border-radius: var(--radius-md);
}

.context-label {
  font-size: 0.76rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-muted);
}

.context-value {
  margin-top: 8px;
  color: var(--text);
  font-size: 1rem;
  line-height: 1.35;
}

.context-value strong {
  display: block;
  font-size: 1.1rem;
  color: var(--accent-strong);
}

.main-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  padding: 12px;
  margin-bottom: 16px;
}

.nav-button,
.tab-button,
.inline-button {
  appearance: none;
  border: 1px solid var(--line);
  background: rgba(13, 22, 31, 0.72);
  color: var(--text-muted);
  border-radius: 999px;
  padding: 9px 14px;
  cursor: pointer;
  transition: 120ms ease;
}

.nav-button:hover,
.tab-button:hover,
.inline-button:hover {
  border-color: var(--line-strong);
  color: var(--text);
}

.nav-button.active,
.tab-button.active,
.inline-button.primary {
  background: var(--accent-soft);
  color: var(--accent-strong);
  border-color: rgba(141, 182, 255, 0.34);
}

.workspace-grid {
  display: grid;
  grid-template-columns: 300px minmax(0, 1.55fr) 380px;
  gap: 16px;
  align-items: start;
}

.rail,
.view-surface,
.decision-surface {
  padding: 18px;
}

.section-title {
  margin: 0;
  font-size: 1.02rem;
  letter-spacing: -0.01em;
}

.section-copy,
.quiet-copy {
  color: var(--text-muted);
  line-height: 1.5;
}

.quiet-copy { font-size: 0.92rem; }

.stack {
  display: grid;
  gap: 14px;
}

.list-reset {
  list-style: none;
  padding: 0;
  margin: 0;
}

.cycle-card,
.entity-card,
.activity-card,
.document-card,
.audit-card,
.mini-card,
.inspect-card {
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background: rgba(10, 17, 25, 0.58);
}

.cycle-card button,
.entity-card button,
.activity-card button,
.document-card button {
  width: 100%;
  border: 0;
  background: transparent;
  color: inherit;
  text-align: left;
  padding: 14px;
  cursor: pointer;
}

.cycle-card.active,
.activity-card.active,
.document-card.active {
  border-color: rgba(141, 182, 255, 0.34);
  background: linear-gradient(180deg, rgba(141, 182, 255, 0.16), rgba(18, 30, 44, 0.92));
}

.card-title {
  font-weight: 600;
  color: var(--text);
  line-height: 1.35;
}

.card-kicker {
  color: var(--accent);
  font-size: 0.76rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 6px;
}

.card-meta,
.card-secondary {
  margin-top: 6px;
  color: var(--text-muted);
  line-height: 1.45;
  font-size: 0.92rem;
}

.badge-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 10px;
}

.badge {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  padding: 5px 9px;
  font-size: 0.83rem;
  background: rgba(141, 182, 255, 0.13);
  color: var(--accent-strong);
}

.badge.success { background: var(--success-soft); color: var(--success); }
.badge.warning { background: var(--warning-soft); color: var(--warning); }
.badge.danger { background: var(--danger-soft); color: var(--danger); }

.view-panel[hidden] { display: none !important; }

.view-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 14px;
  margin-bottom: 14px;
}

.view-head-copy {
  max-width: 720px;
}

.view-body {
  display: grid;
  gap: 16px;
}

.map-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.4fr) 300px;
  gap: 16px;
}

.graph-stage {
  position: relative;
  min-height: 620px;
  overflow: hidden;
  background:
    radial-gradient(circle at top, rgba(141, 182, 255, 0.08), transparent 34%),
    linear-gradient(180deg, rgba(11, 18, 26, 0.96), rgba(9, 15, 23, 0.96));
}

.graph-svg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.graph-link {
  stroke: rgba(141, 182, 255, 0.24);
  stroke-width: 1.6;
}

.graph-link.risk { stroke: rgba(255, 154, 147, 0.4); stroke-dasharray: 6 6; }
.graph-link.support { stroke: rgba(240, 195, 122, 0.34); }

.graph-node {
  position: absolute;
  transform: translate(-50%, -50%);
  min-width: 146px;
  max-width: 190px;
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 12px;
  background: linear-gradient(180deg, rgba(18, 30, 44, 0.96), rgba(8, 14, 21, 0.94));
  color: var(--text);
  box-shadow: 0 16px 32px rgba(0, 0, 0, 0.25);
  cursor: pointer;
  text-align: left;
}

.graph-node.primary {
  width: 230px;
  min-width: 230px;
  border-color: rgba(141, 182, 255, 0.36);
  background: linear-gradient(180deg, rgba(141, 182, 255, 0.18), rgba(18, 30, 44, 0.98));
}

.graph-node.activity { border-color: rgba(124, 165, 223, 0.2); }
.graph-node.document { border-color: rgba(240, 195, 122, 0.22); }
.graph-node.entity { border-color: rgba(143, 176, 159, 0.2); }
.graph-node.risk { border-color: rgba(255, 154, 147, 0.26); }
.graph-node.selected { outline: 2px solid rgba(141, 182, 255, 0.34); }

.graph-node-title {
  font-weight: 600;
  line-height: 1.3;
}

.graph-node-meta {
  margin-top: 6px;
  color: var(--text-muted);
  font-size: 0.84rem;
  line-height: 1.35;
}

.map-aside,
.flow-grid,
.inspect-grid {
  display: grid;
  gap: 16px;
}

.flow-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.lane {
  padding: 16px;
}

.lane-header {
  margin-bottom: 12px;
}

.lane-header h3,
.inspect-card h3,
.map-aside h3 {
  margin: 0;
  font-size: 1rem;
}

.lane-items {
  display: grid;
  gap: 10px;
}

.support-strip {
  display: grid;
  gap: 12px;
}

.inspect-grid {
  grid-template-columns: 1.15fr 0.85fr;
}

.inspect-focus {
  padding: 18px;
}

.inspect-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 14px;
}

.inspect-panel[hidden] { display: none !important; }

.inspect-header {
  padding-bottom: 14px;
  border-bottom: 1px solid var(--line);
}

.inspect-label {
  color: var(--accent);
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  margin-bottom: 6px;
}

.inspect-title {
  font-size: 1.48rem;
  line-height: 1.1;
  letter-spacing: -0.03em;
}

.inspect-summary {
  margin-top: 10px;
  color: var(--text-soft);
  line-height: 1.6;
}

.inspect-section {
  margin-top: 16px;
}

.meta-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.meta-cell {
  padding: 12px;
  border: 1px solid var(--line);
  border-radius: var(--radius-sm);
  background: rgba(9, 16, 24, 0.5);
}

.meta-cell strong {
  display: block;
  margin-top: 6px;
  color: var(--text);
}

.evidence-block {
  padding: 14px;
  border: 1px solid var(--line);
  border-radius: var(--radius-sm);
  background: rgba(9, 16, 24, 0.58);
  line-height: 1.6;
}

.preview {
  padding: 16px;
  min-height: 300px;
  white-space: pre-wrap;
  font-family: "Cascadia Code", Consolas, monospace;
  font-size: 0.9rem;
  line-height: 1.6;
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background: rgba(5, 11, 17, 0.9);
  color: #dbe5ef;
}

.preview.error {
  background: rgba(50, 17, 17, 0.72);
  color: var(--danger);
  font-family: "Aptos", "Segoe UI", system-ui, sans-serif;
}

.action-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}

.detail-callout {
  padding: 14px;
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background: rgba(9, 16, 24, 0.52);
}

.decision-surface {
  display: grid;
  gap: 16px;
}

.secondary-focus {
  opacity: 0.9;
}

.audit-group {
  padding: 14px;
}

.audit-group + .audit-group { margin-top: 12px; }

.audit-date {
  color: var(--accent);
  font-size: 0.82rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  margin-bottom: 12px;
}

.audit-entry {
  padding: 12px 0;
  border-top: 1px solid rgba(114, 141, 173, 0.18);
}

.audit-entry:first-child { border-top: 0; padding-top: 0; }

.audit-head {
  display: flex;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 6px;
}

.audit-title {
  font-weight: 600;
  line-height: 1.35;
}

.audit-time {
  color: var(--text-muted);
  font-size: 0.84rem;
  white-space: nowrap;
}

.audit-body {
  color: var(--text-soft);
  line-height: 1.55;
}

.quiet-details {
  border: 1px solid var(--line);
  border-radius: var(--radius-sm);
  background: rgba(9, 16, 24, 0.4);
}

.quiet-details summary {
  cursor: pointer;
  list-style: none;
  padding: 10px 12px;
  color: var(--text-muted);
}

.quiet-details summary::-webkit-details-marker { display: none; }

.technical-list {
  display: grid;
  gap: 10px;
  padding: 0 12px 12px;
}

.technical-row {
  display: grid;
  gap: 4px;
}

.technical-label {
  color: var(--text-muted);
  font-size: 0.76rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.technical-value {
  color: var(--text-soft);
  font-size: 0.88rem;
  word-break: break-word;
}

.toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.toolbar select {
  min-width: 150px;
}

.toolbar input,
.toolbar select {
  appearance: none;
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 10px 12px;
  background: rgba(9, 16, 24, 0.62);
  color: var(--text);
}

.empty-state {
  padding: 14px;
  border: 1px dashed rgba(114, 141, 173, 0.24);
  border-radius: var(--radius-md);
  color: var(--text-muted);
  background: rgba(9, 16, 24, 0.34);
}

.muted { color: var(--text-muted); }

@media (max-width: 1320px) {
  .workspace-grid {
    grid-template-columns: 1fr;
  }
  .inspect-grid,
  .map-layout,
  .flow-grid,
  .cycle-context-bar {
    grid-template-columns: 1fr;
  }
  .graph-stage { min-height: 560px; }
}
"""


def _body() -> str:
    return """
<main class="app-shell">
  <header class="top-shell">
    <div>
      <div class="brand-kicker">Institutional supervision surface</div>
      <h1>Nexus Cockpit</h1>
      <p>
        A shared operational substrate for human and agent work. Read the system through cycles,
        follow the pressure moving inside them, and judge evidence before acting.
      </p>
    </div>
    <div id="workspace-badge" class="workspace-pill" aria-live="polite">Checking workspace...</div>
  </header>

  <section id="readiness-bar" class="surface readiness-bar loading" aria-live="polite">
    <div>
      <div class="readiness-title" id="readiness-title">Preparing cockpit</div>
      <div class="readiness-detail" id="readiness-detail">
        Loading local supervision surfaces and validating workspace readiness.
      </div>
    </div>
    <div class="badge-row" id="readiness-badges"></div>
  </section>

  <section id="cycle-context-bar" class="surface cycle-context-bar">
    <div class="context-cell">
      <div class="context-label">Cycle in focus</div>
      <div class="context-value"><strong id="context-cycle-title">Waiting for cycle context</strong><span id="context-cycle-summary">Select a cycle to anchor the supervision surface.</span></div>
    </div>
    <div class="context-cell">
      <div class="context-label">State</div>
      <div class="context-value" id="context-cycle-state">-</div>
    </div>
    <div class="context-cell">
      <div class="context-label">Temporal pressure</div>
      <div class="context-value" id="context-cycle-pressure">-</div>
    </div>
    <div class="context-cell">
      <div class="context-label">Relevant work</div>
      <div class="context-value" id="context-cycle-work">-</div>
    </div>
    <div class="context-cell">
      <div class="context-label">Blockages</div>
      <div class="context-value" id="context-cycle-blockers">-</div>
    </div>
    <div class="context-cell">
      <div class="context-label">Risk</div>
      <div class="context-value" id="context-cycle-risk">-</div>
    </div>
    <div class="context-cell">
      <div class="context-label">Evidence health</div>
      <div class="context-value" id="context-cycle-evidence">-</div>
    </div>
  </section>

  <nav id="main-nav" class="surface main-nav" aria-label="Primary cockpit views">
    <button class="nav-button active" type="button" data-view="map">MAP</button>
    <button class="nav-button" type="button" data-view="flow">FLOW</button>
    <button class="nav-button" type="button" data-view="inspect">INSPECT</button>
    <button class="nav-button" type="button" data-view="audit">AUDIT</button>
  </nav>

  <section class="workspace-grid">
    <aside class="surface rail stack">
      <section>
        <h2 class="section-title">Cycle Index</h2>
        <p class="section-copy">Cycles remain the gravitational center of the workspace.</p>
        <ul id="cycle-index" class="list-reset stack"></ul>
      </section>

      <section>
        <h2 class="section-title">Structural Context</h2>
        <p class="quiet-copy">Entities and documents stay visible as supporting institutional structure.</p>
        <div id="ontology-list" class="stack"></div>
      </section>

      <section>
        <h2 class="section-title">Workspace Pulse</h2>
        <div id="workspace-pulse" class="stack"></div>
      </section>
    </aside>

    <section class="surface view-surface">
      <section id="map-view" class="view-panel">
        <div class="view-head">
          <div class="view-head-copy">
            <h2 class="section-title">MAP</h2>
            <p class="section-copy">
              Read the workspace as a living institutional map. The focused cycle anchors the scene,
              activities reveal operational pressure, and documents show the supporting evidence layer.
            </p>
          </div>
        </div>
        <div class="view-body map-layout">
          <section id="graph-stage" class="surface graph-stage"></section>
          <aside class="map-aside">
            <article class="surface inspect-card">
              <h3>Map reading guide</h3>
              <p class="quiet-copy" id="map-guide-copy">
                Select a node to move directly into operational inspection.
              </p>
              <div class="badge-row" id="map-legend"></div>
            </article>
            <article class="surface inspect-card">
              <h3>Focused cycle narrative</h3>
              <div id="map-cycle-narrative" class="evidence-block">
                Cycle context will appear here once the workspace is ready.
              </div>
            </article>
          </aside>
        </div>
      </section>

      <section id="flow-view" class="view-panel" hidden>
        <div class="view-head">
          <div class="view-head-copy">
            <h2 class="section-title">FLOW</h2>
            <p class="section-copy">
              Move from focused cycle to immediate action. This surface answers what requires action now,
              what is actively moving, and which documents are carrying operational legitimacy.
            </p>
          </div>
        </div>
        <div class="toolbar">
          <select id="flow-status-filter">
            <option value="">All flow states</option>
            <option value="attention">Requires action now</option>
            <option value="moving">Moving now</option>
            <option value="stable">Stabilized</option>
          </select>
        </div>
        <div class="view-body flow-grid">
          <section class="surface lane">
            <div class="lane-header">
              <h3>Requires action now</h3>
              <p class="quiet-copy">Blocked and pending work that should shape the next intervention.</p>
            </div>
            <div id="flow-attention" class="lane-items"></div>
          </section>
          <section class="surface lane">
            <div class="lane-header">
              <h3>Moving now</h3>
              <p class="quiet-copy">Work already in motion inside the selected cycle.</p>
            </div>
            <div id="flow-moving" class="lane-items"></div>
          </section>
          <section class="surface lane">
            <div class="lane-header">
              <h3>Stabilized and support</h3>
              <p class="quiet-copy">Completed work and the documents currently supporting the cycle.</p>
            </div>
            <div id="flow-stable" class="lane-items"></div>
            <div class="support-strip" id="flow-documents"></div>
          </section>
        </div>
      </section>

      <section id="inspect-view" class="view-panel" hidden>
        <div class="view-head">
          <div class="view-head-copy">
            <h2 class="section-title">INSPECT</h2>
            <p class="section-copy">
              Judge the selected object through context, evidence, and governance. Technical details remain
              accessible, but secondary.
            </p>
          </div>
        </div>
        <div class="view-body inspect-grid">
          <section class="surface inspect-focus">
            <div class="inspect-header">
              <div class="inspect-label" id="inspect-object-label">Focus</div>
              <div class="inspect-title" id="inspect-object-title">Select an activity, document, or cycle</div>
              <div class="inspect-summary" id="inspect-object-summary">
                The selected detail surface will organize context, evidence, and governance.
              </div>
              <div class="badge-row" id="inspect-object-badges"></div>
            </div>
            <div class="inspect-tabs">
              <button class="tab-button active" type="button" data-inspect-tab="context">Context</button>
              <button class="tab-button" type="button" data-inspect-tab="evidence">Evidence</button>
              <button class="tab-button" type="button" data-inspect-tab="governance">Governance</button>
            </div>
            <section id="inspect-context" class="inspect-panel"></section>
            <section id="inspect-evidence" class="inspect-panel" hidden></section>
            <section id="inspect-governance" class="inspect-panel" hidden></section>
          </section>

          <aside class="decision-surface">
            <article class="surface inspect-card">
              <h3>Selected Detail</h3>
              <p class="quiet-copy">Primary focus comes first; supporting material stays visible but quieter.</p>
              <div id="selected-primary" class="stack"></div>
              <div id="selected-secondary" class="stack secondary-focus"></div>
            </article>
            <article class="surface inspect-card">
              <h3>Decision signal</h3>
              <div id="decision-signal" class="evidence-block">
                The cockpit will synthesize what matters once a cycle is in focus.
              </div>
            </article>
            <details class="quiet-details">
              <summary>Technical details</summary>
              <div id="technical-drawer" class="technical-list"></div>
            </details>
          </aside>
        </div>
      </section>

      <section id="audit-view" class="view-panel" hidden>
        <div class="view-head">
          <div class="view-head-copy">
            <h2 class="section-title">AUDIT</h2>
            <p class="section-copy">
              Reconstruct the institutional memory of the workspace. Events are grouped as narrative
              consequences rather than exposed as a flat technical log.
            </p>
          </div>
        </div>
        <div id="audit-timeline" class="view-body"></div>
      </section>
    </section>

    <aside class="surface decision-surface">
      <article class="inspect-card">
        <h3>What matters now</h3>
        <div id="operator-guidance" class="evidence-block">
          Cycle pressure and evidence health will guide action once the workspace loads.
        </div>
      </article>
      <article class="inspect-card">
        <h3>Supporting documents</h3>
        <p class="quiet-copy">Documents remain visible as operational support, not as the primary reading path.</p>
        <div id="document-strip" class="stack"></div>
      </article>
      <article class="inspect-card">
        <h3>Institutional memory</h3>
        <p class="quiet-copy">A small live sample stays here; the full narrative remains in the AUDIT view.</p>
        <div id="audit-snapshot" class="stack"></div>
      </article>
    </aside>
  </section>
</main>
"""


def _script() -> str:
    return """
const api = {
  status: "/api/system/status",
  entities: "/api/entities",
  relations: "/api/relations",
  documents: "/api/documents",
  documentIntegrity: "/api/document-integrity",
  cycles: "/api/cycles",
  activities: "/api/activities",
  audit: "/api/audit-log?limit=40"
};

const state = {
  view: "map",
  inspectTab: "context",
  status: null,
  entities: [],
  relations: [],
  documents: [],
  documentIntegrity: [],
  cycles: [],
  activities: [],
  audit: [],
  focusedCycleId: null,
  selected: { type: "cycle", id: null },
  documentDetails: {},
  pendingMutation: null
};

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function setHtml(id, html) {
  const element = document.getElementById(id);
  if (element) {
    element.innerHTML = html;
  }
}

function setText(id, value) {
  const element = document.getElementById(id);
  if (element) {
    element.textContent = value;
  }
}

async function fetchJson(url, options) {
  const response = await fetch(url, options);
  const payload = await response.json();
  if (!response.ok || payload.status !== "ok") {
    throw new Error(payload.message || `Request failed for ${url}`);
  }
  return payload.data;
}

function titleCase(value) {
  return String(value || "")
    .replaceAll("_", " ")
    .split(" ")
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

function statusLabel(value) {
  return titleCase(value || "unknown");
}

function cycleLabel(cycle) {
  if (!cycle) {
    return "No cycle selected";
  }
  return `${titleCase(cycle.type)} cycle | ${formatDate(cycle.start_date)}`;
}

function documentTypeLabel(value) {
  return titleCase(value || "document");
}

function formatDate(value) {
  if (!value) {
    return "-";
  }
  const parsed = new Date(String(value).replace(" ", "T"));
  if (Number.isNaN(parsed.getTime())) {
    return String(value);
  }
  return parsed.toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" });
}

function formatDateTime(value) {
  if (!value) {
    return "-";
  }
  const parsed = new Date(String(value).replace(" ", "T"));
  if (Number.isNaN(parsed.getTime())) {
    return String(value);
  }
  return parsed.toLocaleString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit"
  });
}

function statusBadgeClass(value) {
  if (["completed", "approved", "ok", "active"].includes(value)) {
    return "success";
  }
  if (["pending", "warning", "draft"].includes(value)) {
    return "warning";
  }
  if (["blocked", "error", "archived"].includes(value)) {
    return "danger";
  }
  return "";
}

function integrityFor(documentId) {
  return state.documentIntegrity.find((item) => item.document_id === documentId) || null;
}

function cycleById(cycleId) {
  return state.cycles.find((item) => item.id === cycleId) || null;
}

function activityById(activityId) {
  return state.activities.find((item) => item.id === activityId) || null;
}

function documentById(documentId) {
  return state.documents.find((item) => item.id === documentId) || null;
}

function relatedActivities(cycleId) {
  return state.activities.filter((item) => item.cycle_id === cycleId);
}

function relatedDocuments(cycleId) {
  return state.documents.filter((item) => item.cycle_id === cycleId);
}

function currentSelection() {
  if (state.selected.type === "activity") {
    return activityById(state.selected.id);
  }
  if (state.selected.type === "document") {
    return documentById(state.selected.id);
  }
  return cycleById(state.selected.id || state.focusedCycleId);
}

function summarizeCycle(cycle) {
  const documents = relatedDocuments(cycle.id);
  const integrityIssues = documents.filter((doc) => {
    const integrity = integrityFor(doc.id);
    return integrity && integrity.integrity_state !== "ok";
  }).length;
  let pressure = "Calm";
  if (cycle.blocked_count > 0) {
    pressure = "Critical";
  } else if (cycle.pending_count > 1 || cycle.in_progress_count > 2) {
    pressure = "Elevated";
  } else if (cycle.activity_count > 0) {
    pressure = "Active";
  }
  let risk = "Managed";
  if (cycle.blocked_count > 0 || integrityIssues > 0) {
    risk = "Elevated";
  }
  if (cycle.blocked_count > 1 || integrityIssues > 1) {
    risk = "High";
  }
  let evidence = "Steady";
  if (integrityIssues > 0) {
    evidence = integrityIssues > 1 ? "Degraded" : "Fragile";
  }
  return { documents, integrityIssues, pressure, risk, evidence };
}

function pickFocusedCycle() {
  if (state.focusedCycleId && cycleById(state.focusedCycleId)) {
    return cycleById(state.focusedCycleId);
  }
  state.focusedCycleId = state.cycles[0]?.id || null;
  return cycleById(state.focusedCycleId);
}

function selectObject(type, id) {
  state.selected = { type, id };
  if (type === "cycle") {
    state.focusedCycleId = id;
  }
  void renderEverything();
}

function activateView(view) {
  state.view = view;
  document.querySelectorAll("[data-view]").forEach((button) => {
    button.classList.toggle("active", button.dataset.view === view);
  });
  ["map", "flow", "inspect", "audit"].forEach((name) => {
    const panel = document.getElementById(`${name}-view`);
    if (panel) {
      panel.hidden = name !== view;
    }
  });
}

function activateInspectTab(tab) {
  state.inspectTab = tab;
  document.querySelectorAll("[data-inspect-tab]").forEach((button) => {
    button.classList.toggle("active", button.dataset.inspectTab === tab);
  });
  ["context", "evidence", "governance"].forEach((name) => {
    const panel = document.getElementById(`inspect-${name}`);
    if (panel) {
      panel.hidden = name !== tab;
    }
  });
}

function setReadiness(title, detail, tone, ready = false) {
  const bar = document.getElementById("readiness-bar");
  bar.className = `surface readiness-bar ${tone}`;
  setText("readiness-title", title);
  setText("readiness-detail", detail);
  setHtml(
    "readiness-badges",
    ready
      ? '<span class="badge success">workspace ready</span><span class="badge">views online</span>'
      : tone === "warning"
      ? '<span class="badge warning">workspace missing</span>'
      : tone === "error"
      ? '<span class="badge danger">load failed</span>'
      : '<span class="badge">loading</span>'
  );
}

function renderWorkspaceBadge() {
  const status = state.status;
  if (!status) {
    setText("workspace-badge", "Checking workspace...");
    return;
  }
  if (!status.is_workspace) {
    setHtml("workspace-badge", "<strong>Workspace not initialized</strong><div class='card-secondary'>Run init and seed before opening the cockpit.</div>");
    return;
  }
  setHtml(
    "workspace-badge",
    `<strong>${escapeHtml(status.workspace_name || "Nexus workspace")}</strong><div class="card-secondary">Schema ${escapeHtml(status.schema_version || "-")} | DB ${status.db_present ? "present" : "missing"}</div>`
  );
}

function renderMetaGrid(items) {
  return `<div class="meta-grid">${items
    .map(
      ([label, value]) => `
        <div class="meta-cell">
          <div class="context-label">${escapeHtml(label)}</div>
          <strong>${escapeHtml(value)}</strong>
        </div>
      `
    )
    .join("")}</div>`;
}

function renderTechnicalDetails(items) {
  if (!items.length) {
    return "";
  }
  return items
    .map(
      ([label, value]) => `
        <div class="technical-row">
          <div class="technical-label">${escapeHtml(label)}</div>
          <div class="technical-value">${escapeHtml(value)}</div>
        </div>
      `
    )
    .join("");
}

function documentNarrative(document) {
  const cycle = document.cycle_id ? cycleById(document.cycle_id) : null;
  const integrity = integrityFor(document.id);
  const health =
    integrity?.integrity_state === "ok"
      ? "is aligned with the current backing file"
      : integrity?.integrity_state === "warning"
      ? "has metadata drift that deserves operator review"
      : "is materially out of sync with its backing file";
  if (cycle) {
    return `${document.title} supports ${cycleLabel(cycle)} and ${health}.`;
  }
  return `${document.title} is general support material and ${health}.`;
}

function activityNarrative(activity) {
  const cycle = cycleById(activity.cycle_id);
  if (!cycle) {
    return `${activity.title} is active in the workspace.`;
  }
  if (activity.status === "blocked") {
    return `${activity.title} is blocked inside ${cycleLabel(cycle)} and needs intervention before work can move.`;
  }
  if (activity.status === "in_progress") {
    return `${activity.title} is currently moving inside ${cycleLabel(cycle)}.`;
  }
  if (activity.status === "completed") {
    return `${activity.title} is already completed inside ${cycleLabel(cycle)}.`;
  }
  return `${activity.title} is waiting to move inside ${cycleLabel(cycle)}.`;
}

function cycleNarrative(cycle) {
  const summary = summarizeCycle(cycle);
  return `${cycleLabel(cycle)} holds ${cycle.activity_count} activities and ${summary.documents.length} supporting documents. Pressure is ${summary.pressure.toLowerCase()}, risk is ${summary.risk.toLowerCase()}, and evidence health is ${summary.evidence.toLowerCase()}.`;
}

function describeAuditEntry(entry) {
  const entity = titleCase(entry.entity_type);
  const action =
    entry.action === "create"
      ? "entered the workspace"
      : entry.action === "update"
      ? "changed state"
      : entry.action === "reconcile"
      ? "was reconciled"
      : entry.action;
  return `${entity} ${action}. ${entry.reason || "No reason recorded."}`;
}

function auditObjectLabel(entry) {
  if (entry.entity_type === "activity") {
    return activityById(entry.entity_id)?.title || "Activity";
  }
  if (entry.entity_type === "document") {
    return documentById(entry.entity_id)?.title || "Document";
  }
  if (entry.entity_type === "cycle") {
    const cycle = cycleById(entry.entity_id);
    return cycle ? cycleLabel(cycle) : "Cycle";
  }
  if (entry.entity_type === "entity") {
    return state.entities.find((item) => item.id === entry.entity_id)?.name || "Entity";
  }
  return entry.entity_id || titleCase(entry.entity_type);
}

function groupAuditEntries(entries) {
  const groups = new Map();
  entries.forEach((entry) => {
    const key = formatDate(entry.timestamp);
    if (!groups.has(key)) {
      groups.set(key, []);
    }
    groups.get(key).push(entry);
  });
  return Array.from(groups.entries());
}

function supportingDocumentForActivity(activity) {
  return state.documents.find((item) => item.cycle_id === activity.cycle_id) || null;
}

function supportingActivityForDocument(document) {
  return state.activities.find((item) => item.cycle_id === document.cycle_id) || null;
}

function operatorGuidance(cycle) {
  if (!cycle) {
    return "The workspace needs an active cycle before the cockpit can orient action.";
  }
  const summary = summarizeCycle(cycle);
  if (cycle.blocked_count > 0) {
    return `${cycleLabel(cycle)} is carrying blocked work. Clear blocked activities first, then review supporting documents for legitimacy drift.`;
  }
  if (summary.integrityIssues > 0) {
    return `${cycleLabel(cycle)} has fragile evidence. Review supporting documents before moving more operational work.`;
  }
  if (cycle.pending_count > 0) {
    return `${cycleLabel(cycle)} is ready to move. Start with pending activities and keep evidence close at hand.`;
  }
  return `${cycleLabel(cycle)} is stable. Use inspection and audit to reconstruct how the cycle evolved.`;
}

function renderOntology() {
  const entityTypes = {};
  state.entities.forEach((item) => {
    entityTypes[item.type] = (entityTypes[item.type] || 0) + 1;
  });
  const integrityIssues = state.documentIntegrity.filter((item) => item.integrity_state !== "ok").length;
  setHtml(
    "ontology-list",
    `
      <div class="entity-card"><button type="button" disabled>
        <div class="card-kicker">Entities</div>
        <div class="card-title">${state.entities.length} structural actors and objects</div>
        <div class="card-secondary">${Object.entries(entityTypes).map(([key, count]) => `${titleCase(key)} ${count}`).join(" | ") || "No entities yet"}</div>
      </button></div>
      <div class="entity-card"><button type="button" disabled>
        <div class="card-kicker">Relations</div>
        <div class="card-title">${state.relations.length} explicit structural links</div>
        <div class="card-secondary">The map uses these links as institutional context.</div>
      </button></div>
      <div class="entity-card"><button type="button" disabled>
        <div class="card-kicker">Evidence</div>
        <div class="card-title">${state.documents.length} supporting documents</div>
        <div class="card-secondary">${integrityIssues ? `${integrityIssues} documents need integrity attention` : "Evidence layer currently aligned"}</div>
      </button></div>
    `
  );
}

function renderWorkspacePulse() {
  const counts = state.status?.counts;
  const activitySummary = state.status?.activity_summary;
  if (!counts || !activitySummary) {
    setHtml("workspace-pulse", '<div class="empty-state">Workspace counts will appear after initialization.</div>');
    return;
  }
  setHtml(
    "workspace-pulse",
    `
      <div class="mini-card"><div class="card-title">${counts.cycles} cycles in memory</div><div class="card-secondary">${counts.active_cycles} active | ${counts.completed_cycles} completed | ${counts.archived_cycles} archived</div></div>
      <div class="mini-card"><div class="card-title">${counts.activities} activities</div><div class="card-secondary">${activitySummary.pending} pending | ${activitySummary.in_progress} in progress | ${activitySummary.completed} completed | ${activitySummary.blocked} blocked</div></div>
      <div class="mini-card"><div class="card-title">${counts.documents} documents</div><div class="card-secondary">${counts.approved_documents} approved | ${counts.draft_documents} draft | ${counts.archived_documents} archived</div></div>
    `
  );
}

function renderCycleIndex() {
  if (!state.cycles.length) {
    setHtml("cycle-index", '<li class="empty-state">No cycles are available yet.</li>');
    return;
  }
  setHtml(
    "cycle-index",
    state.cycles
      .map((cycle) => {
        const summary = summarizeCycle(cycle);
        return `
          <li class="cycle-card ${cycle.id === state.focusedCycleId ? "active" : ""}">
            <button type="button" data-select-cycle="${escapeHtml(cycle.id)}">
              <div class="card-kicker">${escapeHtml(titleCase(cycle.type))}</div>
              <div class="card-title">${escapeHtml(formatDate(cycle.start_date))}</div>
              <div class="card-secondary">${escapeHtml(statusLabel(cycle.status))} | ${cycle.activity_count} activities | ${summary.documents.length} documents</div>
              <div class="badge-row">
                <span class="badge ${statusBadgeClass(cycle.status)}">${escapeHtml(statusLabel(cycle.status))}</span>
                <span class="badge ${statusBadgeClass(summary.pressure === "Critical" ? "blocked" : summary.pressure === "Elevated" ? "pending" : "completed")}">${escapeHtml(summary.pressure)}</span>
              </div>
            </button>
          </li>
        `;
      })
      .join("")
  );
}

function renderContextBar() {
  const cycle = pickFocusedCycle();
  if (!cycle) {
    setText("context-cycle-title", "No cycle in focus");
    setText("context-cycle-summary", "Seed the workspace to unlock the institutional reading path.");
    ["context-cycle-state", "context-cycle-pressure", "context-cycle-work", "context-cycle-blockers", "context-cycle-risk", "context-cycle-evidence"].forEach((id) => setText(id, "-"));
    return;
  }
  const summary = summarizeCycle(cycle);
  const blocked = cycle.blocked_count ? `${cycle.blocked_count} blocked activities` : "No active blockages";
  const work = cycle.in_progress_count
    ? `${cycle.in_progress_count} activities moving now`
    : cycle.pending_count
    ? `${cycle.pending_count} activities ready to move`
    : "Operational work is mostly stabilized";
  setText("context-cycle-title", cycleLabel(cycle));
  setText("context-cycle-summary", cycleNarrative(cycle));
  setText("context-cycle-state", statusLabel(cycle.status));
  setText("context-cycle-pressure", summary.pressure);
  setText("context-cycle-work", work);
  setText("context-cycle-blockers", blocked);
  setText("context-cycle-risk", summary.risk);
  setText("context-cycle-evidence", summary.evidence);
  setText("operator-guidance", operatorGuidance(cycle));
}

function graphNodeMarkup(node) {
  return `
    <button
      class="graph-node ${escapeHtml(node.kind)} ${node.primary ? "primary" : ""} ${node.selected ? "selected" : ""}"
      style="left:${node.x}%; top:${node.y}%"
      type="button"
      data-select="${escapeHtml(node.kind)}:${escapeHtml(node.id)}"
    >
      <div class="card-kicker">${escapeHtml(node.kicker)}</div>
      <div class="graph-node-title">${escapeHtml(node.title)}</div>
      <div class="graph-node-meta">${escapeHtml(node.meta)}</div>
    </button>
  `;
}

function buildMapModel(cycle) {
  const activities = relatedActivities(cycle.id);
  const documents = relatedDocuments(cycle.id);
  const otherCycles = state.cycles.filter((item) => item.id !== cycle.id).slice(0, 3);
  const entities = state.entities.slice(0, 4);
  const riskNodes = [];
  if (cycle.blocked_count > 0) {
    riskNodes.push({
      kind: "risk",
      id: `${cycle.id}-blocked`,
      kicker: "Risk",
      title: "Blocked work pressure",
      meta: `${cycle.blocked_count} blocked activities`,
      x: 20,
      y: 18,
      selected: false
    });
  }
  if (summarizeCycle(cycle).integrityIssues > 0) {
    riskNodes.push({
      kind: "risk",
      id: `${cycle.id}-evidence`,
      kicker: "Risk",
      title: "Evidence drift",
      meta: "Supporting documents need attention",
      x: 80,
      y: 18,
      selected: false
    });
  }

  const nodes = [
    {
      kind: "cycle",
      id: cycle.id,
      kicker: "Cycle",
      title: cycleLabel(cycle),
      meta: `${statusLabel(cycle.status)} | ${cycle.activity_count} activities`,
      x: 50,
      y: 48,
      primary: true,
      selected: state.selected.type === "cycle" && state.selected.id === cycle.id
    },
    ...otherCycles.map((item, index) => ({
      kind: "cycle",
      id: item.id,
      kicker: "Adjacent cycle",
      title: cycleLabel(item),
      meta: `${statusLabel(item.status)} | ${item.activity_count} activities`,
      x: 24 + index * 26,
      y: 12,
      selected: state.selected.type === "cycle" && state.selected.id === item.id
    })),
    ...activities.map((item, index) => ({
      kind: "activity",
      id: item.id,
      kicker: "Activity",
      title: item.title,
      meta: `${statusLabel(item.status)} | ${titleCase(item.priority === 1 ? "urgent" : item.priority === 2 ? "high" : item.priority === 4 ? "low" : "normal")}`,
      x: 22,
      y: 30 + index * (activities.length > 1 ? 16 : 0),
      selected: state.selected.type === "activity" && state.selected.id === item.id
    })),
    ...documents.map((item, index) => ({
      kind: "document",
      id: item.id,
      kicker: "Document",
      title: item.title,
      meta: `${documentTypeLabel(item.type)} | ${statusLabel(item.status)}`,
      x: 78,
      y: 30 + index * (documents.length > 1 ? 16 : 0),
      selected: state.selected.type === "document" && state.selected.id === item.id
    })),
    ...entities.map((item, index) => ({
      kind: "entity",
      id: item.id,
      kicker: "Entity",
      title: item.name,
      meta: titleCase(item.type),
      x: 20 + index * 20,
      y: 84,
      selected: false
    })),
    ...riskNodes
  ];

  const links = [];
  nodes.filter((node) => node.kind === "activity").forEach((node) => {
    links.push({ from: cycle.id, to: node.id, tone: node.meta.includes("Blocked") ? "risk" : "default" });
  });
  nodes.filter((node) => node.kind === "document").forEach((node) => {
    links.push({ from: cycle.id, to: node.id, tone: "support" });
  });
  nodes.filter((node) => node.kind === "entity").forEach((node) => {
    links.push({ from: cycle.id, to: node.id, tone: "default" });
  });
  riskNodes.forEach((node) => {
    links.push({ from: cycle.id, to: node.id, tone: "risk" });
  });
  return { nodes, links };
}

function renderMapView() {
  const cycle = pickFocusedCycle();
  if (!cycle) {
    setHtml("graph-stage", '<div class="empty-state" style="margin:18px">No cycle is available yet.</div>');
    setText("map-guide-copy", "Initialize and seed the workspace to populate the map.");
    setText("map-cycle-narrative", "Cycle context will appear here once the workspace contains operational data.");
    return;
  }
  const model = buildMapModel(cycle);
  const positions = Object.fromEntries(model.nodes.map((node) => [node.id, node]));
  const links = model.links
    .map((link) => {
      const from = positions[link.from];
      const to = positions[link.to];
      if (!from || !to) return "";
      return `<line class="graph-link ${link.tone === "risk" ? "risk" : link.tone === "support" ? "support" : ""}" x1="${from.x}%" y1="${from.y}%" x2="${to.x}%" y2="${to.y}%"></line>`;
    })
    .join("");
  setHtml(
    "graph-stage",
    `
      <svg class="graph-svg" viewBox="0 0 100 100" preserveAspectRatio="none">${links}</svg>
      ${model.nodes.map(graphNodeMarkup).join("")}
    `
  );
  setHtml(
    "map-legend",
    `
      <span class="badge">cycle</span>
      <span class="badge">activity</span>
      <span class="badge warning">document</span>
      <span class="badge success">entity</span>
      <span class="badge danger">risk</span>
    `
  );
  setText("map-guide-copy", "The cycle stays at the center. Activities carry operational pressure, documents carry support and evidence, and risk nodes signal where supervision should tighten.");
  setText("map-cycle-narrative", cycleNarrative(cycle));
}

function activityCardMarkup(activity, emphasize = false) {
  return `
    <div class="activity-card ${state.selected.type === "activity" && state.selected.id === activity.id ? "active" : ""}">
      <button type="button" data-select-activity="${escapeHtml(activity.id)}">
        <div class="card-kicker">Activity</div>
        <div class="card-title">${escapeHtml(activity.title)}</div>
        <div class="card-secondary">${escapeHtml(activityNarrative(activity))}</div>
        <div class="badge-row">
          <span class="badge ${statusBadgeClass(activity.status)}">${escapeHtml(statusLabel(activity.status))}</span>
          ${emphasize ? '<span class="badge warning">needs attention</span>' : ""}
        </div>
      </button>
    </div>
  `;
}

function documentCardMarkup(document) {
  const integrity = integrityFor(document.id);
  return `
    <div class="document-card ${state.selected.type === "document" && state.selected.id === document.id ? "active" : ""}">
      <button type="button" data-select-document="${escapeHtml(document.id)}">
        <div class="card-kicker">${escapeHtml(documentTypeLabel(document.type))}</div>
        <div class="card-title">${escapeHtml(document.title)}</div>
        <div class="card-secondary">${escapeHtml(documentNarrative(document))}</div>
        <div class="badge-row">
          <span class="badge ${statusBadgeClass(document.status)}">${escapeHtml(statusLabel(document.status))}</span>
          ${
            integrity
              ? `<span class="badge ${statusBadgeClass(integrity.integrity_state)}">${escapeHtml(statusLabel(integrity.integrity_state))}</span>`
              : ""
          }
        </div>
      </button>
    </div>
  `;
}

function renderFlowView() {
  const cycle = pickFocusedCycle();
  if (!cycle) {
    ["flow-attention", "flow-moving", "flow-stable", "flow-documents"].forEach((id) => setHtml(id, '<div class="empty-state">No focused cycle is available.</div>'));
    return;
  }
  const activities = relatedActivities(cycle.id);
  const filter = document.getElementById("flow-status-filter")?.value || "";
  const attention = activities.filter((item) => ["pending", "blocked"].includes(item.status));
  const moving = activities.filter((item) => item.status === "in_progress");
  const stable = activities.filter((item) => item.status === "completed");
  const groups = { attention, moving, stable };
  Object.entries(groups).forEach(([name, items]) => {
    const target = filter && filter !== name ? [] : items;
    setHtml(
      `flow-${name}`,
      target.length ? target.map((item) => activityCardMarkup(item, name === "attention")).join("") : '<div class="empty-state">No items in this lane.</div>'
    );
  });
  const documents = relatedDocuments(cycle.id);
  setHtml(
    "flow-documents",
    documents.length ? documents.map(documentCardMarkup).join("") : '<div class="empty-state">No supporting documents are linked to this cycle.</div>'
  );
  setHtml(
    "document-strip",
    documents.slice(0, 4).length ? documents.slice(0, 4).map(documentCardMarkup).join("") : '<div class="empty-state">No supporting documents in focus.</div>'
  );
}

function renderSelectedCards() {
  const selection = currentSelection();
  const focusedCycle = pickFocusedCycle();
  let primaryHtml = '<div class="empty-state">Select a cycle, activity, or document to anchor judgment.</div>';
  let secondaryHtml = "";

  if (!selection) {
    setHtml("selected-primary", primaryHtml);
    setHtml("selected-secondary", secondaryHtml);
    return;
  }

  if (state.selected.type === "activity") {
    const document = supportingDocumentForActivity(selection);
    primaryHtml = activityCardMarkup(selection, selection.status === "blocked" || selection.status === "pending");
    secondaryHtml = document
      ? `<div class="inspect-card detail-callout"><div class="card-kicker">Supporting document</div><div class="card-title">${escapeHtml(document.title)}</div><div class="card-secondary">${escapeHtml(documentNarrative(document))}</div></div>`
      : '<div class="empty-state">No supporting document is linked to this activity yet.</div>';
  } else if (state.selected.type === "document") {
    const activity = supportingActivityForDocument(selection);
    primaryHtml = documentCardMarkup(selection);
    secondaryHtml = activity
      ? `<div class="inspect-card detail-callout"><div class="card-kicker">Operational anchor</div><div class="card-title">${escapeHtml(activity.title)}</div><div class="card-secondary">${escapeHtml(activityNarrative(activity))}</div></div>`
      : '<div class="empty-state">No single activity is currently anchored by this document.</div>';
  } else {
    primaryHtml = `<div class="inspect-card detail-callout"><div class="card-kicker">Focused cycle</div><div class="card-title">${escapeHtml(cycleLabel(selection))}</div><div class="card-secondary">${escapeHtml(cycleNarrative(selection))}</div></div>`;
    const firstActivity = relatedActivities(selection.id)[0];
    secondaryHtml = firstActivity
      ? `<div class="inspect-card detail-callout"><div class="card-kicker">Next activity</div><div class="card-title">${escapeHtml(firstActivity.title)}</div><div class="card-secondary">${escapeHtml(activityNarrative(firstActivity))}</div></div>`
      : '<div class="empty-state">No activity is attached to the focused cycle yet.</div>';
  }

  if (!secondaryHtml && focusedCycle) {
    secondaryHtml = `<div class="inspect-card detail-callout"><div class="card-kicker">Cycle context</div><div class="card-title">${escapeHtml(cycleLabel(focusedCycle))}</div><div class="card-secondary">${escapeHtml(cycleNarrative(focusedCycle))}</div></div>`;
  }
  setHtml("selected-primary", primaryHtml);
  setHtml("selected-secondary", secondaryHtml);
}

async function ensureDocumentDetails(documentId) {
  if (!documentId) return null;
  if (state.documentDetails[documentId]) {
    return state.documentDetails[documentId];
  }
  try {
    const details = await fetchJson(`/api/documents/${encodeURIComponent(documentId)}`);
    state.documentDetails[documentId] = details;
    return details;
  } catch (error) {
    state.documentDetails[documentId] = { error: error.message };
    return state.documentDetails[documentId];
  }
}

function renderInspectContext(selection) {
  if (!selection) {
    setHtml("inspect-context", '<div class="empty-state">Nothing is selected yet.</div>');
    return;
  }
  if (state.selected.type === "activity") {
    setHtml(
      "inspect-context",
      renderMetaGrid([
        ["Activity", selection.title],
        ["Cycle", cycleLabel(cycleById(selection.cycle_id))],
        ["State", statusLabel(selection.status)],
        ["Priority", selection.priority <= 2 ? "High" : selection.priority >= 4 ? "Low" : "Normal"],
        ["Reading", activityNarrative(selection)],
        ["Created", formatDateTime(selection.created_at)]
      ])
    );
    return;
  }
  if (state.selected.type === "document") {
    const integrity = integrityFor(selection.id);
    setHtml(
      "inspect-context",
      renderMetaGrid([
        ["Document", selection.title],
        ["Type", documentTypeLabel(selection.type)],
        ["Lifecycle", statusLabel(selection.status)],
        ["Cycle", selection.cycle_id ? cycleLabel(cycleById(selection.cycle_id)) : "General support material"],
        ["Integrity", integrity ? statusLabel(integrity.integrity_state) : "Unknown"],
        ["Reading", documentNarrative(selection)]
      ])
    );
    return;
  }
  const summary = summarizeCycle(selection);
  setHtml(
    "inspect-context",
    renderMetaGrid([
      ["Cycle", cycleLabel(selection)],
      ["State", statusLabel(selection.status)],
      ["Activities", String(selection.activity_count)],
      ["Supporting documents", String(summary.documents.length)],
      ["Pressure", summary.pressure],
      ["Risk", summary.risk]
    ])
  );
}

async function renderInspectEvidence(selection) {
  if (!selection) {
    setHtml("inspect-evidence", '<div class="empty-state">Nothing is selected yet.</div>');
    return;
  }
  if (state.selected.type === "document") {
    const details = await ensureDocumentDetails(selection.id);
    const integrity = integrityFor(selection.id);
    const previewClass = details?.error ? "preview error" : "preview";
    setHtml(
      "inspect-evidence",
      `
        <div class="detail-callout">
          <div class="card-kicker">Document evidence</div>
          <div class="card-title">${escapeHtml(selection.title)}</div>
          <div class="card-secondary">${escapeHtml(documentNarrative(selection))}</div>
          <div class="badge-row">
            <span class="badge ${statusBadgeClass(selection.status)}">${escapeHtml(statusLabel(selection.status))}</span>
            ${
              integrity
                ? `<span class="badge ${statusBadgeClass(integrity.integrity_state)}">${escapeHtml(statusLabel(integrity.integrity_state))}</span>`
                : ""
            }
          </div>
        </div>
        <div class="${previewClass}">${escapeHtml(details?.content_preview || details?.error || "(empty document)")}</div>
      `
    );
    return;
  }
  if (state.selected.type === "activity") {
    const document = supportingDocumentForActivity(selection);
    if (!document) {
      setHtml("inspect-evidence", '<div class="empty-state">No supporting document is linked to this activity.</div>');
      return;
    }
    const details = await ensureDocumentDetails(document.id);
    setHtml(
      "inspect-evidence",
      `
        <div class="detail-callout">
          <div class="card-kicker">Supporting evidence</div>
          <div class="card-title">${escapeHtml(document.title)}</div>
          <div class="card-secondary">${escapeHtml(documentNarrative(document))}</div>
        </div>
        <div class="${details?.error ? "preview error" : "preview"}">${escapeHtml(details?.content_preview || details?.error || "(empty document)")}</div>
      `
    );
    return;
  }
  const documents = relatedDocuments(selection.id);
  setHtml(
    "inspect-evidence",
    documents.length ? documents.map(documentCardMarkup).join("") : '<div class="empty-state">No supporting documents are currently attached to this cycle.</div>'
  );
}

function activityStatusControls(activity) {
  const options = ["pending", "in_progress", "completed", "blocked"];
  return options
    .filter((value) => value !== activity.status)
    .map(
      (value) => `<button class="inline-button ${value === "blocked" ? "" : "primary"}" type="button" data-set-activity-status="${escapeHtml(activity.id)}:${escapeHtml(value)}" ${state.pendingMutation ? "disabled" : ""}>Mark ${escapeHtml(statusLabel(value))}</button>`
    )
    .join("");
}

function documentStatusControls(document) {
  const allowed = document.status === "draft" ? ["approved"] : document.status === "approved" ? ["archived"] : [];
  return allowed
    .map(
      (value) => `<button class="inline-button primary" type="button" data-set-document-status="${escapeHtml(document.id)}:${escapeHtml(value)}" ${state.pendingMutation ? "disabled" : ""}>Set ${escapeHtml(statusLabel(value))}</button>`
    )
    .join("");
}

function canReconcile(integrity) {
  return Boolean(
    integrity &&
      integrity.backing_file_exists &&
      (integrity.current_content_hash && integrity.current_content_hash !== integrity.recorded_content_hash ||
        (!integrity.path_matches_expected && integrity.expected_path_exists))
  );
}

function renderInspectGovernance(selection) {
  if (!selection) {
    setHtml("inspect-governance", '<div class="empty-state">Nothing is selected yet.</div>');
    setHtml("technical-drawer", "");
    return;
  }
  const relatedAudit = state.audit.filter((entry) => entry.entity_id === selection.id).slice(0, 5);
  if (state.selected.type === "activity") {
    setHtml(
      "inspect-governance",
      `
        <div class="detail-callout">
          <div class="card-kicker">Controlled status transition</div>
          <div class="card-secondary">Activity status updates stay explicit and auditable across CLI, API, and cockpit.</div>
          <div class="action-row">${activityStatusControls(selection)}</div>
        </div>
        ${relatedAudit.map(renderAuditSnippet).join("") || '<div class="empty-state">No audit memory yet for this activity.</div>'}
      `
    );
    setHtml(
      "technical-drawer",
      renderTechnicalDetails([
        ["Activity id", selection.id],
        ["Cycle id", selection.cycle_id],
        ["Created at", selection.created_at],
        ["Raw status", selection.status]
      ])
    );
    return;
  }
  if (state.selected.type === "document") {
    const integrity = integrityFor(selection.id);
    setHtml(
      "inspect-governance",
      `
        <div class="detail-callout">
          <div class="card-kicker">Lifecycle and reconciliation</div>
          <div class="card-secondary">Document legitimacy remains explicit. Lifecycle and reconcile actions are available only when the current state allows them.</div>
          <div class="action-row">${documentStatusControls(selection)}
            <button class="inline-button ${canReconcile(integrity) ? "primary" : ""}" type="button" data-reconcile-document="${escapeHtml(selection.id)}" ${canReconcile(integrity) && !state.pendingMutation ? "" : "disabled"}>Reconcile metadata</button>
          </div>
        </div>
        ${relatedAudit.map(renderAuditSnippet).join("") || '<div class="empty-state">No audit memory yet for this document.</div>'}
      `
    );
    setHtml(
      "technical-drawer",
      renderTechnicalDetails([
        ["Document id", selection.id],
        ["Stored path", selection.path],
        ["Version", selection.version],
        ["Created at", selection.created_at],
        ["Modified at", selection.modified_at],
        ["Approved at", selection.approved_at || "-"]
      ])
    );
    return;
  }
  setHtml(
    "inspect-governance",
    `
      <div class="detail-callout">
        <div class="card-kicker">Cycle governance</div>
        <div class="card-secondary">Cycles anchor the shared operational context. Use audit and supporting evidence to judge whether the cycle remains institutionally sound.</div>
      </div>
      ${relatedAudit.map(renderAuditSnippet).join("") || '<div class="empty-state">No audit memory yet for this cycle.</div>'}
    `
  );
  setHtml(
    "technical-drawer",
    renderTechnicalDetails([
      ["Cycle id", selection.id],
      ["Type", selection.type],
      ["Start", selection.start_date],
      ["End", selection.end_date || "-"],
      ["Created at", selection.created_at]
    ])
  );
}

function renderAuditSnippet(entry) {
  return `
    <div class="detail-callout">
      <div class="audit-head">
        <div class="audit-title">${escapeHtml(auditObjectLabel(entry))}</div>
        <div class="audit-time">${escapeHtml(formatDateTime(entry.timestamp))}</div>
      </div>
      <div class="audit-body">${escapeHtml(describeAuditEntry(entry))}</div>
    </div>
  `;
}

async function renderInspectView() {
  const selection = currentSelection();
  if (!selection) {
    setText("inspect-object-label", "Focus");
    setText("inspect-object-title", "Select an activity, document, or cycle");
    setText("inspect-object-summary", "The selected detail surface will organize context, evidence, and governance.");
    setHtml("inspect-object-badges", "");
    setHtml("inspect-context", '<div class="empty-state">Nothing selected.</div>');
    setHtml("inspect-evidence", '<div class="empty-state">Nothing selected.</div>');
    setHtml("inspect-governance", '<div class="empty-state">Nothing selected.</div>');
    setHtml("technical-drawer", "");
    return;
  }
  const label = state.selected.type === "document" ? "Supporting document" : state.selected.type === "activity" ? "Operational activity" : "Focused cycle";
  const title = state.selected.type === "cycle" ? cycleLabel(selection) : selection.title;
  const summary = state.selected.type === "document" ? documentNarrative(selection) : state.selected.type === "activity" ? activityNarrative(selection) : cycleNarrative(selection);
  const badges =
    state.selected.type === "cycle"
      ? `<span class="badge ${statusBadgeClass(selection.status)}">${escapeHtml(statusLabel(selection.status))}</span>`
      : state.selected.type === "activity"
      ? `<span class="badge ${statusBadgeClass(selection.status)}">${escapeHtml(statusLabel(selection.status))}</span><span class="badge">${escapeHtml(cycleLabel(cycleById(selection.cycle_id)))}</span>`
      : `<span class="badge ${statusBadgeClass(selection.status)}">${escapeHtml(statusLabel(selection.status))}</span><span class="badge ${statusBadgeClass(integrityFor(selection.id)?.integrity_state || "")}">${escapeHtml(statusLabel(integrityFor(selection.id)?.integrity_state || "unknown"))}</span>`;
  setText("inspect-object-label", label);
  setText("inspect-object-title", title);
  setText("inspect-object-summary", summary);
  setHtml("inspect-object-badges", badges);
  renderInspectContext(selection);
  await renderInspectEvidence(selection);
  renderInspectGovernance(selection);
  renderSelectedCards();
}

function renderAuditView() {
  if (!state.audit.length) {
    setHtml("audit-timeline", '<div class="empty-state">Audit memory will appear here once the workspace records events.</div>');
    setHtml("audit-snapshot", '<div class="empty-state">No recent audit activity.</div>');
    return;
  }
  const groups = groupAuditEntries(state.audit);
  setHtml(
    "audit-timeline",
    groups
      .map(
        ([dateLabel, entries]) => `
          <section class="surface audit-group">
            <div class="audit-date">${escapeHtml(dateLabel)}</div>
            ${entries
              .map(
                (entry) => `
                  <article class="audit-entry">
                    <div class="audit-head">
                      <div class="audit-title">${escapeHtml(auditObjectLabel(entry))}</div>
                      <div class="audit-time">${escapeHtml(formatDateTime(entry.timestamp))}</div>
                    </div>
                    <div class="audit-body">${escapeHtml(describeAuditEntry(entry))}</div>
                  </article>
                `
              )
              .join("")}
          </section>
        `
      )
      .join("")
  );
  setHtml(
    "audit-snapshot",
    state.audit.slice(0, 4).map(renderAuditSnippet).join("")
  );
}

async function refreshWorkspace(preserveSelection = true) {
  const previousSelection = { ...state.selected };
  const previousFocus = state.focusedCycleId;
  const status = await fetchJson(api.status);
  state.status = status;
  renderWorkspaceBadge();
  if (!status.is_workspace) {
    setReadiness(
      "Workspace not initialized",
      "Run `python -m nexus init` and then seed the workspace before opening the cockpit.",
      "warning"
    );
    renderEmptyWorkspace();
    return;
  }

  const [entities, relations, documents, documentIntegrity, cycles, activities, audit] = await Promise.all([
    fetchJson(api.entities),
    fetchJson(api.relations),
    fetchJson(api.documents),
    fetchJson(api.documentIntegrity),
    fetchJson(api.cycles),
    fetchJson(api.activities),
    fetchJson(api.audit)
  ]);
  state.entities = entities;
  state.relations = relations;
  state.documents = documents;
  state.documentIntegrity = documentIntegrity;
  state.cycles = cycles;
  state.activities = activities;
  state.audit = audit;

  if (preserveSelection && previousFocus && cycleById(previousFocus)) {
    state.focusedCycleId = previousFocus;
  } else {
    state.focusedCycleId = state.cycles[0]?.id || null;
  }
  if (preserveSelection && previousSelection.id) {
    const stillExists =
      previousSelection.type === "activity"
        ? activityById(previousSelection.id)
        : previousSelection.type === "document"
        ? documentById(previousSelection.id)
        : cycleById(previousSelection.id);
    state.selected = stillExists ? previousSelection : { type: "cycle", id: state.focusedCycleId };
  } else {
    state.selected = { type: "cycle", id: state.focusedCycleId };
  }
  if (!state.selected.id && state.focusedCycleId) {
    state.selected = { type: "cycle", id: state.focusedCycleId };
  }
  await renderEverything();
  setReadiness(
    "Workspace ready",
    "The institutional map, operational flow, judgment surface, and audit memory are fully loaded.",
    "ready",
    true
  );
}

function renderEmptyWorkspace() {
  setHtml("cycle-index", '<li class="empty-state">No cycles are available.</li>');
  setHtml("ontology-list", '<div class="empty-state">No local structural context yet.</div>');
  setHtml("workspace-pulse", '<div class="empty-state">Workspace pulse will appear after initialization.</div>');
  setHtml("graph-stage", '<div class="empty-state" style="margin:18px">Workspace not initialized.</div>');
  setHtml("flow-attention", '<div class="empty-state">Workspace not initialized.</div>');
  setHtml("flow-moving", '<div class="empty-state">Workspace not initialized.</div>');
  setHtml("flow-stable", '<div class="empty-state">Workspace not initialized.</div>');
  setHtml("flow-documents", '<div class="empty-state">Workspace not initialized.</div>');
  setHtml("document-strip", '<div class="empty-state">Workspace not initialized.</div>');
  setHtml("audit-timeline", '<div class="empty-state">Workspace not initialized.</div>');
  setHtml("audit-snapshot", '<div class="empty-state">Workspace not initialized.</div>');
  setHtml("selected-primary", '<div class="empty-state">Workspace not initialized.</div>');
  setHtml("selected-secondary", "");
  setText("operator-guidance", "Initialize the workspace before using the cockpit.");
}

async function renderEverything() {
  renderOntology();
  renderWorkspacePulse();
  renderCycleIndex();
  renderContextBar();
  renderMapView();
  renderFlowView();
  await renderInspectView();
  renderAuditView();
}

async function updateActivityStatus(activityId, status) {
  if (state.pendingMutation) return;
  state.pendingMutation = `activity:${activityId}`;
  try {
    await fetchJson(`/api/activities/${encodeURIComponent(activityId)}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status })
    });
    await refreshWorkspace(true);
  } finally {
    state.pendingMutation = null;
    await renderEverything();
  }
}

async function updateDocumentStatus(documentId, status) {
  if (state.pendingMutation) return;
  state.pendingMutation = `document:${documentId}`;
  try {
    await fetchJson(`/api/documents/${encodeURIComponent(documentId)}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status })
    });
    delete state.documentDetails[documentId];
    await refreshWorkspace(true);
  } finally {
    state.pendingMutation = null;
    await renderEverything();
  }
}

async function reconcileDocument(documentId) {
  if (state.pendingMutation) return;
  state.pendingMutation = `reconcile:${documentId}`;
  try {
    await fetchJson(`/api/documents/${encodeURIComponent(documentId)}/reconcile`, {
      method: "POST"
    });
    delete state.documentDetails[documentId];
    await refreshWorkspace(true);
  } finally {
    state.pendingMutation = null;
    await renderEverything();
  }
}

function bindEvents() {
  document.getElementById("main-nav")?.addEventListener("click", (event) => {
    const button = event.target.closest("[data-view]");
    if (!button) return;
    activateView(button.dataset.view);
  });

  document.addEventListener("click", async (event) => {
    const cycleButton = event.target.closest("[data-select-cycle]");
    if (cycleButton) {
      selectObject("cycle", cycleButton.dataset.selectCycle);
      return;
    }
    const activityButton = event.target.closest("[data-select-activity]");
    if (activityButton) {
      selectObject("activity", activityButton.dataset.selectActivity);
      activateView("inspect");
      return;
    }
    const documentButton = event.target.closest("[data-select-document]");
    if (documentButton) {
      selectObject("document", documentButton.dataset.selectDocument);
      activateView("inspect");
      return;
    }
    const graphButton = event.target.closest("[data-select]");
    if (graphButton) {
      const [type, id] = graphButton.dataset.select.split(":");
      if (type === "entity" || type === "risk") return;
      selectObject(type === "cycle" ? "cycle" : type, id);
      if (type !== "cycle") activateView("inspect");
      return;
    }
    const tabButton = event.target.closest("[data-inspect-tab]");
    if (tabButton) {
      activateInspectTab(tabButton.dataset.inspectTab);
      return;
    }
    const activityMutation = event.target.closest("[data-set-activity-status]");
    if (activityMutation) {
      const [id, status] = activityMutation.dataset.setActivityStatus.split(":");
      await updateActivityStatus(id, status);
      return;
    }
    const documentMutation = event.target.closest("[data-set-document-status]");
    if (documentMutation) {
      const [id, status] = documentMutation.dataset.setDocumentStatus.split(":");
      await updateDocumentStatus(id, status);
      return;
    }
    const reconcileButton = event.target.closest("[data-reconcile-document]");
    if (reconcileButton) {
      await reconcileDocument(reconcileButton.dataset.reconcileDocument);
      return;
    }
  });

  document.getElementById("flow-status-filter")?.addEventListener("change", () => renderFlowView());
}

async function boot() {
  activateView("map");
  activateInspectTab("context");
  bindEvents();
  setReadiness(
    "Preparing cockpit",
    "Loading workspace surfaces and resolving the current institutional picture.",
    "loading"
  );
  try {
    await refreshWorkspace(false);
  } catch (error) {
    renderWorkspaceBadge();
    renderEmptyWorkspace();
    setReadiness("Cockpit load failed", error.message, "error");
  }
}

boot();
"""
