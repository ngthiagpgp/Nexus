from __future__ import annotations


def render_cockpit_page() -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Nexus Cockpit</title>
    <link
      rel="icon"
      href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' stop-color='%238db6ff'/%3E%3Cstop offset='100%25' stop-color='%239786ff'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='64' height='64' rx='18' fill='%23091119'/%3E%3Cpath d='M17 45V19h6l18 18V19h6v26h-6L23 27v18z' fill='url(%23g)'/%3E%3C/svg%3E"
    />
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
  --page-glow: rgba(115, 155, 228, 0.14);
  --panel: rgba(15, 24, 35, 0.92);
  --panel-alt: rgba(18, 30, 44, 0.92);
  --panel-soft: rgba(12, 20, 30, 0.72);
  --panel-strong: rgba(20, 33, 49, 0.98);
  --panel-glass: rgba(18, 28, 42, 0.78);
  --line: rgba(114, 141, 173, 0.24);
  --line-strong: rgba(124, 165, 223, 0.34);
  --text: #edf3f8;
  --text-soft: #ccd6e1;
  --text-muted: #8fa0b3;
  --text-faint: #728396;
  --accent: #8db6ff;
  --accent-soft: rgba(141, 182, 255, 0.18);
  --accent-strong: #dce9ff;
  --accent-glow: rgba(151, 134, 255, 0.26);
  --success: #90d2a7;
  --success-soft: rgba(62, 142, 94, 0.18);
  --warning: #f0c37a;
  --warning-soft: rgba(187, 133, 35, 0.18);
  --danger: #ff9a93;
  --danger-soft: rgba(176, 66, 60, 0.18);
  --shadow-soft: 0 18px 40px rgba(0, 0, 0, 0.24);
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
    radial-gradient(circle at 8% 4%, rgba(141, 182, 255, 0.16), transparent 20%),
    radial-gradient(circle at 90% 0%, rgba(113, 157, 214, 0.08), transparent 20%),
    radial-gradient(circle at 50% 0%, rgba(164, 133, 255, 0.08), transparent 32%),
    linear-gradient(180deg, #091019 0%, #0d1620 30%, #0f1823 100%);
}
a { color: inherit; }
button, input, select { font: inherit; }

.app-shell {
  max-width: 1760px;
  margin: 0 auto;
  padding: 18px 20px 30px;
}

.top-shell {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 8px;
}

.brand-kicker {
  color: var(--accent);
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  margin-bottom: 10px;
  opacity: 0.9;
}

.top-shell h1 {
  margin: 0;
  font-size: clamp(2.1rem, 4vw, 3.5rem);
  line-height: 0.92;
  letter-spacing: -0.05em;
}

.top-shell p {
  margin: 9px 0 0;
  max-width: 800px;
  color: var(--text-muted);
  line-height: 1.52;
}

.workspace-pill {
  padding: 12px 16px;
  min-width: 250px;
  background: linear-gradient(180deg, rgba(18, 30, 44, 0.86), rgba(11, 17, 24, 0.92));
  border: 1px solid rgba(141, 182, 255, 0.2);
  border-radius: var(--radius-md);
  color: var(--text-soft);
  box-shadow: var(--shadow-soft);
  backdrop-filter: blur(12px);
  align-self: flex-start;
}

.surface {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-soft);
  backdrop-filter: blur(10px);
}

.readiness-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  padding: 12px 16px;
  margin-bottom: 10px;
  background: linear-gradient(180deg, rgba(14, 23, 33, 0.96), rgba(11, 18, 26, 0.92));
}

.readiness-bar.loading { border-color: rgba(141, 182, 255, 0.24); }
.readiness-bar.ready { border-color: rgba(92, 170, 121, 0.28); }
.readiness-bar.warning { border-color: rgba(187, 133, 35, 0.32); }
.readiness-bar.error { border-color: rgba(176, 66, 60, 0.32); }

.readiness-title {
  font-size: 0.74rem;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  color: var(--text-muted);
  margin-bottom: 4px;
}

.readiness-detail {
  color: var(--text-soft);
  line-height: 1.4;
  font-size: 0.95rem;
}

.cycle-context-bar {
  display: grid;
  grid-template-columns: 2.6fr repeat(6, minmax(120px, 1fr));
  gap: 10px;
  padding: 12px;
  margin-bottom: 10px;
  background: linear-gradient(180deg, rgba(20, 33, 49, 0.92), rgba(13, 21, 31, 0.98));
}

.context-cell {
  padding: 12px 13px;
  background: rgba(9, 16, 24, 0.36);
  border: 1px solid rgba(141, 182, 255, 0.1);
  border-radius: var(--radius-md);
}

.context-cell:first-child {
  background: linear-gradient(180deg, rgba(141, 182, 255, 0.12), rgba(12, 20, 30, 0.42));
  border-color: rgba(141, 182, 255, 0.2);
}

.context-label {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: var(--text-faint);
}

.context-value {
  margin-top: 7px;
  color: var(--text);
  font-size: 0.98rem;
  line-height: 1.35;
}

.context-value strong {
  display: block;
  font-size: 1.14rem;
  color: var(--accent-strong);
}

.main-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  padding: 8px 10px;
  margin-bottom: 16px;
  background: linear-gradient(180deg, rgba(14, 22, 31, 0.82), rgba(11, 18, 26, 0.9));
}

.nav-button,
.tab-button,
.inline-button {
  appearance: none;
  border: 1px solid transparent;
  background: rgba(13, 22, 31, 0.42);
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
  background: linear-gradient(180deg, rgba(141, 182, 255, 0.16), rgba(141, 182, 255, 0.08));
  color: var(--accent-strong);
  border-color: rgba(141, 182, 255, 0.34);
  box-shadow: inset 0 -1px 0 rgba(141, 182, 255, 0.22);
}

.workspace-grid {
  display: grid;
  grid-template-columns: 238px minmax(0, 2.12fr) 322px;
  gap: 18px;
  align-items: start;
}

.rail,
.view-surface,
.decision-surface {
  padding: 16px;
}

.rail {
  background: linear-gradient(180deg, rgba(11, 17, 24, 0.76), rgba(8, 13, 20, 0.68));
  border-color: rgba(114, 141, 173, 0.14);
  box-shadow: none;
}

.rail section + section {
  padding-top: 6px;
  border-top: 1px solid rgba(114, 141, 173, 0.08);
}

.view-surface {
  padding: 18px;
  background:
    radial-gradient(circle at 50% 0%, rgba(151, 134, 255, 0.05), transparent 28%),
    linear-gradient(180deg, rgba(13, 20, 29, 0.96), rgba(9, 15, 23, 0.98));
}

.decision-surface {
  background: linear-gradient(180deg, rgba(12, 18, 27, 0.82), rgba(9, 14, 21, 0.72));
  border-color: rgba(114, 141, 173, 0.14);
  box-shadow: none;
}

.decision-surface > .inspect-card {
  background: linear-gradient(180deg, rgba(12, 19, 28, 0.62), rgba(8, 13, 19, 0.44));
  border-color: rgba(114, 141, 173, 0.12);
}

.section-title {
  margin: 0;
  font-size: 1rem;
  letter-spacing: -0.015em;
}

.section-copy,
.quiet-copy {
  color: var(--text-muted);
  line-height: 1.48;
}

.quiet-copy { font-size: 0.9rem; }

.stack {
  display: grid;
  gap: 12px;
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
  background: rgba(10, 17, 25, 0.54);
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.02);
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
  padding: 13px;
  cursor: pointer;
}

.cycle-card.active,
.activity-card.active,
.document-card.active {
  border-color: rgba(141, 182, 255, 0.34);
  background: linear-gradient(180deg, rgba(141, 182, 255, 0.14), rgba(18, 30, 44, 0.92));
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.2);
}

.card-title {
  font-weight: 600;
  color: var(--text);
  line-height: 1.35;
  letter-spacing: -0.01em;
}

.card-kicker {
  color: var(--accent);
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  margin-bottom: 7px;
}

.card-meta,
.card-secondary {
  margin-top: 6px;
  color: var(--text-muted);
  line-height: 1.42;
  font-size: 0.89rem;
}

.badge-row {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  margin-top: 9px;
}

.badge {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  padding: 5px 10px;
  font-size: 0.79rem;
  background: rgba(141, 182, 255, 0.13);
  color: var(--accent-strong);
  border: 1px solid rgba(141, 182, 255, 0.08);
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
  margin-bottom: 10px;
}

.view-head-copy {
  max-width: 640px;
}

.view-body {
  display: grid;
  gap: 14px;
}

.overview-grid {
  grid-template-columns: minmax(0, 1.45fr) repeat(2, minmax(0, 0.82fr));
  gap: 14px;
}

.overview-hero,
.overview-card {
  padding: 18px;
  border: 1px solid var(--line);
  border-radius: 20px;
  background: linear-gradient(180deg, rgba(12, 19, 28, 0.92), rgba(9, 15, 23, 0.88));
}

.overview-hero {
  background:
    radial-gradient(circle at top right, rgba(151, 134, 255, 0.12), transparent 34%),
    linear-gradient(180deg, rgba(15, 23, 33, 0.96), rgba(9, 15, 23, 0.92));
}

.overview-kicker {
  color: var(--text-faint);
  font-size: 0.72rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

.overview-title {
  margin-top: 10px;
  font-size: 1.54rem;
  line-height: 1.04;
  letter-spacing: -0.04em;
}

.overview-copy {
  margin-top: 10px;
  color: var(--text-soft);
  line-height: 1.58;
}

.overview-card h3 {
  margin: 0;
  font-size: 1rem;
  letter-spacing: -0.01em;
}

.overview-card .card-secondary,
.overview-card .quiet-copy {
  margin-top: 8px;
}

.map-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.92fr) 228px;
  gap: 12px;
}

.graph-stage {
  --graph-node-scale: 1;
  --graph-link-scale: 1;
  position: relative;
  min-height: 720px;
  overflow: hidden;
  background:
    radial-gradient(circle at 50% 42%, rgba(151, 134, 255, 0.12), transparent 20%),
    radial-gradient(circle at top, rgba(141, 182, 255, 0.08), transparent 34%),
    linear-gradient(180deg, rgba(11, 18, 26, 0.96), rgba(9, 15, 23, 0.96));
  border-color: rgba(141, 182, 255, 0.16);
  border-radius: 26px;
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,0.02),
    0 20px 54px rgba(0, 0, 0, 0.28);
}

.graph-toolbar {
  position: absolute;
  left: 18px;
  bottom: 18px;
  z-index: 3;
  display: inline-flex;
  gap: 8px;
  padding: 8px;
  border: 1px solid rgba(141, 182, 255, 0.12);
  border-radius: 16px;
  background: rgba(8, 13, 20, 0.76);
  backdrop-filter: blur(12px);
}

.graph-tool-button {
  min-width: 38px;
  min-height: 38px;
  padding: 0 12px;
  border-radius: 12px;
  border: 1px solid rgba(141, 182, 255, 0.08);
  background: rgba(12, 19, 28, 0.66);
  color: var(--text-soft);
  cursor: pointer;
}

.graph-tool-button:hover {
  color: var(--text);
  border-color: rgba(141, 182, 255, 0.24);
}

.graph-tool-button.active {
  color: var(--accent-strong);
  border-color: rgba(141, 182, 255, 0.3);
  background: rgba(141, 182, 255, 0.12);
}

.graph-viewport {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.graph-world {
  position: absolute;
  inset: 0;
  transform-origin: 50% 50%;
  transition: transform 140ms ease;
  will-change: transform;
}

.graph-stage::before,
.graph-stage::after {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.graph-stage::before {
  background:
    radial-gradient(circle at 50% 48%, rgba(151, 134, 255, 0.18), transparent 18%),
    radial-gradient(circle at 20% 18%, rgba(143, 176, 159, 0.08), transparent 14%),
    radial-gradient(circle at 80% 24%, rgba(240, 195, 122, 0.06), transparent 16%);
  opacity: 0.92;
}

.graph-stage::after {
  background-image:
    linear-gradient(rgba(141, 182, 255, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(141, 182, 255, 0.04) 1px, transparent 1px);
  background-size: 84px 84px;
  mask-image: radial-gradient(circle at 50% 50%, rgba(0, 0, 0, 0.72), transparent 86%);
  opacity: 0.22;
}

.graph-svg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  overflow: visible;
}

.map-stage-overlay {
  position: absolute;
  left: 20px;
  top: 18px;
  z-index: 2;
  max-width: 360px;
  padding: 14px 16px;
  border: 1px solid rgba(141, 182, 255, 0.16);
  border-radius: 18px;
  background: linear-gradient(180deg, rgba(11, 18, 26, 0.74), rgba(8, 13, 20, 0.58));
  box-shadow: 0 18px 36px rgba(0, 0, 0, 0.22);
  backdrop-filter: blur(12px);
}

.map-stage-kicker {
  color: var(--text-faint);
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.18em;
}

.map-stage-title {
  margin-top: 8px;
  font-size: 1.24rem;
  font-weight: 600;
  letter-spacing: -0.03em;
}

.map-stage-copy {
  margin-top: 8px;
  color: var(--text-soft);
  line-height: 1.52;
  font-size: 0.93rem;
}

.map-stage-metrics {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 10px;
}

.hover-probe {
  position: absolute;
  z-index: 4;
  max-width: 250px;
  padding: 12px 13px;
  border: 1px solid rgba(141, 182, 255, 0.16);
  border-radius: 16px;
  background: linear-gradient(180deg, rgba(10, 16, 24, 0.88), rgba(7, 12, 18, 0.84));
  box-shadow: 0 18px 34px rgba(0, 0, 0, 0.26);
  backdrop-filter: blur(12px);
  pointer-events: none;
}

.hover-probe[hidden] { display: none !important; }

.hover-probe-title {
  font-weight: 600;
  line-height: 1.3;
  letter-spacing: -0.01em;
}

.hover-probe-copy {
  margin-top: 7px;
  color: var(--text-soft);
  font-size: 0.88rem;
  line-height: 1.5;
}

.graph-link {
  stroke: rgba(141, 182, 255, 0.24);
  stroke-width: calc(1.12px * var(--graph-link-scale));
  stroke-linecap: round;
  fill: none;
  filter: drop-shadow(0 0 8px rgba(141, 182, 255, 0.12));
  transition: opacity 120ms ease, stroke-width 120ms ease;
}

.graph-link.blocks {
  stroke: rgba(255, 154, 147, 0.54);
  stroke-dasharray: 9 5;
  stroke-linecap: square;
}

.graph-link.supports {
  stroke: rgba(240, 195, 122, 0.34);
  stroke-width: calc(1px * var(--graph-link-scale));
}

.graph-link.requires {
  stroke: rgba(108, 181, 255, 0.34);
  stroke-dasharray: 10 6;
}

.graph-link.impacts {
  stroke: rgba(176, 155, 255, 0.34);
  stroke-dasharray: 14 9;
}

.graph-link.references {
  stroke: rgba(127, 145, 163, 0.24);
  stroke-dasharray: 2 8;
}

.graph-link.owns {
  stroke: rgba(139, 203, 159, 0.32);
  stroke-width: calc(1.46px * var(--graph-link-scale));
}

.graph-link.active { stroke-width: calc(2.2px * var(--graph-link-scale)); opacity: 1; }
.graph-link.muted { opacity: 0.22; }

.graph-link-label {
  fill: var(--text-faint);
  font-size: 2.3px;
  letter-spacing: 0.03em;
  text-transform: uppercase;
  opacity: 0;
}

.graph-link-label.active { opacity: 0.92; }

.graph-node {
  --node-scale: 1;
  position: absolute;
  transform: translate(-50%, -50%) scale(var(--node-scale));
  min-width: 132px;
  max-width: 174px;
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 12px 13px;
  background: linear-gradient(180deg, rgba(19, 30, 43, 0.98), rgba(8, 14, 21, 0.96));
  color: var(--text);
  box-shadow: 0 16px 34px rgba(0, 0, 0, 0.28), inset 0 1px 0 rgba(255,255,255,0.03);
  cursor: pointer;
  text-align: left;
  backdrop-filter: blur(8px);
  transition: transform 120ms ease, border-color 120ms ease, box-shadow 120ms ease;
}

.graph-node:hover {
  transform: translate(-50%, -50%) translateY(-2px) scale(var(--node-scale));
  border-color: rgba(141, 182, 255, 0.28);
}

.graph-node.focused {
  border-color: rgba(141, 182, 255, 0.38);
  box-shadow: 0 0 0 1px rgba(141, 182, 255, 0.16), 0 18px 40px rgba(0, 0, 0, 0.32);
}

.graph-node.muted { opacity: 0.34; }

.graph-node.primary {
  width: 246px;
  min-width: 246px;
  border-color: rgba(176, 155, 255, 0.48);
  background:
    radial-gradient(circle at top, rgba(193, 168, 255, 0.16), transparent 56%),
    linear-gradient(180deg, rgba(74, 52, 112, 0.26), rgba(16, 26, 38, 0.98));
  box-shadow:
    0 0 0 1px rgba(176, 155, 255, 0.12),
    0 0 36px rgba(151, 134, 255, 0.24),
    0 20px 44px rgba(0, 0, 0, 0.34);
  z-index: 3;
}

.graph-node.primary .graph-node-title {
  font-size: 1.16rem;
}

.graph-node.activity { border-color: rgba(124, 165, 223, 0.2); }
.graph-node.document { border-color: rgba(240, 195, 122, 0.22); }
.graph-node.entity { border-color: rgba(143, 176, 159, 0.2); }
.graph-node.risk { border-color: rgba(255, 154, 147, 0.26); }
.graph-node.selected {
  outline: 2px solid rgba(141, 182, 255, 0.3);
  box-shadow: 0 0 0 1px rgba(141, 182, 255, 0.16), 0 18px 40px rgba(0, 0, 0, 0.28);
}

.graph-node-title {
  font-weight: 600;
  line-height: 1.3;
  letter-spacing: -0.015em;
}

.graph-node-meta {
  margin-top: 6px;
  color: var(--text-muted);
  font-size: 0.81rem;
  line-height: 1.42;
}

.graph-node-state {
  margin-top: 10px;
  display: inline-flex;
  align-items: center;
  padding: 4px 9px;
  border-radius: 999px;
  font-size: 0.72rem;
  color: var(--text-soft);
  background: rgba(141, 182, 255, 0.08);
  border: 1px solid rgba(141, 182, 255, 0.08);
}

.map-aside,
.flow-grid,
.inspect-grid {
  display: grid;
  gap: 16px;
}

.map-aside {
  align-content: start;
  gap: 10px;
}

.flow-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.lane {
  padding: 16px;
  background:
    linear-gradient(180deg, rgba(15, 23, 33, 0.96), rgba(10, 16, 24, 0.96));
  position: relative;
  overflow: hidden;
}

.lane::before {
  content: "";
  position: absolute;
  inset: 0 0 auto 0;
  height: 3px;
  border-top-left-radius: inherit;
  border-top-right-radius: inherit;
  opacity: 0.92;
}

.lane-attention::before {
  background: linear-gradient(90deg, rgba(255, 154, 147, 0.92), rgba(240, 195, 122, 0.82));
}

.lane-moving::before {
  background: linear-gradient(90deg, rgba(111, 177, 255, 0.88), rgba(142, 187, 255, 0.4));
}

.lane-stable::before {
  background: linear-gradient(90deg, rgba(110, 206, 144, 0.86), rgba(132, 210, 167, 0.4));
}

.lane-header {
  margin-bottom: 14px;
  padding-right: 24px;
}

.lane-header h3,
.inspect-card h3,
.map-aside h3 {
  margin: 0;
  font-size: 1rem;
  letter-spacing: -0.01em;
}

.lane-items {
  display: grid;
  gap: 11px;
}

.support-strip {
  display: grid;
  gap: 12px;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid rgba(114, 141, 173, 0.12);
}

.support-strip .document-card {
  background: rgba(10, 16, 23, 0.44);
}

.inspect-grid {
  grid-template-columns: 1.34fr 0.66fr;
  align-items: start;
  gap: 12px;
}

.inspect-focus {
  padding: 20px 22px;
  background:
    linear-gradient(180deg, rgba(15, 23, 33, 0.96), rgba(9, 15, 23, 0.98));
}

.inspect-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 16px 0 14px;
}

.inspect-panel[hidden] { display: none !important; }

.inspect-header {
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(114, 141, 173, 0.18);
}

.inspect-label {
  color: var(--text-faint);
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  margin-bottom: 8px;
}

.inspect-title {
  font-size: 1.58rem;
  line-height: 1.04;
  letter-spacing: -0.035em;
}

.inspect-summary {
  margin-top: 12px;
  color: var(--text-soft);
  line-height: 1.62;
  max-width: 66ch;
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
  background: rgba(9, 16, 24, 0.44);
}

.meta-cell strong {
  display: block;
  margin-top: 6px;
  color: var(--text);
  letter-spacing: -0.01em;
}

.evidence-block {
  padding: 14px;
  border: 1px solid var(--line);
  border-radius: var(--radius-sm);
  background: rgba(9, 16, 24, 0.48);
  line-height: 1.6;
}

.inspect-surface {
  display: grid;
  gap: 14px;
}

.inspect-reading-surface {
  padding: 18px;
  border: 1px solid rgba(114, 141, 173, 0.16);
  border-radius: 18px;
  background: linear-gradient(180deg, rgba(8, 14, 21, 0.74), rgba(6, 11, 17, 0.88));
}

.preview {
  padding: 18px 18px 20px;
  min-height: 340px;
  white-space: pre-wrap;
  font-family: "Cascadia Code", Consolas, monospace;
  font-size: 0.92rem;
  line-height: 1.72;
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background: linear-gradient(180deg, rgba(6, 12, 18, 0.96), rgba(7, 13, 19, 0.9));
  color: #dbe5ef;
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.02);
}

.preview.error {
  background: linear-gradient(180deg, rgba(50, 17, 17, 0.78), rgba(28, 10, 10, 0.74));
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
  background: rgba(9, 16, 24, 0.48);
}

.flow-emphasis {
  position: relative;
  padding-left: 12px;
}

.flow-emphasis::before {
  content: "";
  position: absolute;
  left: 0;
  top: 3px;
  bottom: 3px;
  width: 2px;
  border-radius: 999px;
  background: rgba(141, 182, 255, 0.34);
}

.detail-stack-label {
  margin: 2px 0 10px;
  color: var(--text-faint);
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.16em;
}

.decision-surface {
  display: grid;
  gap: 12px;
}

.secondary-focus {
  opacity: 0.82;
}

.audit-group {
  padding: 16px 18px;
  background: linear-gradient(180deg, rgba(14, 21, 31, 0.92), rgba(10, 16, 24, 0.9));
}

.audit-group + .audit-group { margin-top: 12px; }

.audit-date {
  color: var(--text-faint);
  font-size: 0.74rem;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  margin-bottom: 10px;
}

.audit-entry {
  position: relative;
  padding: 14px 0 14px 16px;
  border-top: 1px solid rgba(114, 141, 173, 0.12);
}

.audit-entry:first-child { border-top: 0; padding-top: 0; }

.audit-entry::before {
  content: "";
  position: absolute;
  left: 0;
  top: 18px;
  bottom: 0;
  width: 2px;
  border-radius: 999px;
  background: linear-gradient(180deg, rgba(141, 182, 255, 0.7), rgba(141, 182, 255, 0.08));
}

.audit-entry:first-child::before { top: 4px; }

.audit-head {
  display: flex;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 7px;
}

.audit-title {
  font-weight: 600;
  line-height: 1.35;
  letter-spacing: -0.01em;
}

.audit-subtitle {
  margin-top: 4px;
  color: var(--text-faint);
  font-size: 0.8rem;
  line-height: 1.4;
}

.audit-time {
  color: var(--text-muted);
  font-size: 0.8rem;
  white-space: nowrap;
}

.audit-body {
  color: var(--text-soft);
  line-height: 1.62;
  max-width: 72ch;
}

.audit-group-title {
  font-size: 1rem;
  font-weight: 600;
  letter-spacing: -0.01em;
}

.audit-group-copy {
  margin-top: 6px;
  margin-bottom: 12px;
  color: var(--text-muted);
  line-height: 1.5;
}

.workspace-grid {
  grid-template-columns: 198px minmax(0, 1fr) 266px;
  gap: 14px;
  transition: grid-template-columns 200ms ease, gap 200ms ease;
}

#left-rail,
#right-rail,
.view-surface,
.graph-stage,
.map-aside,
.inspect-focus,
.decision-surface {
  transition: opacity 180ms ease, border-color 180ms ease, background 180ms ease, box-shadow 180ms ease, transform 180ms ease;
}

#left-rail {
  opacity: 0.78;
  padding: 14px;
}

#left-rail .section-copy,
#left-rail .quiet-copy {
  font-size: 0.82rem;
}

#left-rail .cycle-card,
#left-rail .entity-card,
#left-rail .mini-card {
  background: rgba(9, 15, 22, 0.42);
  border-color: rgba(114, 141, 173, 0.1);
  box-shadow: none;
}

#right-rail {
  padding: 14px;
  opacity: 0.9;
}

#right-rail > .inspect-card {
  background: linear-gradient(180deg, rgba(11, 17, 24, 0.54), rgba(8, 13, 19, 0.36));
  border-color: rgba(114, 141, 173, 0.1);
}

.rail-memory {
  padding: 10px 12px 0;
  border: 1px solid rgba(114, 141, 173, 0.12);
  border-radius: var(--radius-md);
  background: rgba(10, 16, 23, 0.42);
}

.map-mode-switcher {
  display: inline-flex;
  gap: 6px;
  align-self: center;
  flex-wrap: wrap;
}

.map-mode-switcher .tab-button {
  padding: 8px 11px;
  font-size: 0.76rem;
  letter-spacing: 0.12em;
}

.mini-map-wrap {
  margin-top: 12px;
}

.mini-map-field {
  position: relative;
  min-height: 176px;
  border: 1px solid rgba(114, 141, 173, 0.12);
  border-radius: 20px;
  overflow: hidden;
  background:
    radial-gradient(circle at 50% 52%, rgba(151, 134, 255, 0.08), transparent 22%),
    linear-gradient(180deg, rgba(10, 16, 23, 0.7), rgba(7, 12, 18, 0.84));
}

.mini-map-field::after {
  content: "";
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(141, 182, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(141, 182, 255, 0.03) 1px, transparent 1px);
  background-size: 56px 56px;
  mask-image: radial-gradient(circle at 50% 50%, rgba(0, 0, 0, 0.7), transparent 90%);
  pointer-events: none;
}

.mini-map-overlay {
  position: absolute;
  inset: auto 14px 14px 14px;
  z-index: 2;
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: end;
}

.mini-map-copy {
  max-width: 420px;
  color: var(--text-soft);
  font-size: 0.88rem;
  line-height: 1.45;
}

.mini-map-jump {
  appearance: none;
  border: 1px solid rgba(141, 182, 255, 0.18);
  background: rgba(11, 18, 27, 0.74);
  color: var(--accent-strong);
  border-radius: 999px;
  padding: 8px 12px;
  cursor: pointer;
}

.mini-map-svg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.mini-map-link {
  fill: none;
  stroke: rgba(141, 182, 255, 0.16);
  stroke-width: 1.2;
}

.mini-map-link.blocks { stroke: rgba(255, 154, 147, 0.26); }
.mini-map-link.supports { stroke: rgba(113, 177, 255, 0.22); }
.mini-map-link.requires { stroke: rgba(141, 182, 255, 0.18); stroke-dasharray: 5 5; }
.mini-map-link.owns { stroke: rgba(172, 183, 196, 0.2); stroke-width: 1.6; }
.mini-map-link.references { stroke: rgba(141, 182, 255, 0.12); stroke-dasharray: 2 5; }
.mini-map-link.impacts { stroke: rgba(240, 195, 122, 0.22); }

.mini-map-node {
  position: absolute;
  transform: translate(-50%, -50%);
  width: 12px;
  height: 12px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  box-shadow: 0 0 0 10px rgba(141, 182, 255, 0.02);
  cursor: pointer;
}

.mini-map-node.cycle {
  width: 18px;
  height: 18px;
  background: rgba(176, 155, 255, 0.74);
  box-shadow: 0 0 0 20px rgba(151, 134, 255, 0.08), 0 0 18px rgba(151, 134, 255, 0.16);
}

.mini-map-node.activity { background: rgba(110, 177, 255, 0.42); }
.mini-map-node.document { background: rgba(240, 195, 122, 0.46); }
.mini-map-node.entity { background: rgba(140, 204, 160, 0.3); }
.mini-map-node.risk { background: rgba(255, 154, 147, 0.5); }
.mini-map-node.dim { opacity: 0.34; }

.mini-map-label {
  position: absolute;
  transform: translate(-50%, calc(-100% - 10px));
  color: rgba(237, 243, 248, 0.7);
  font-size: 0.7rem;
  letter-spacing: 0.04em;
  pointer-events: none;
}

.view-surface {
  padding: 16px 16px 18px;
}

.map-layout {
  grid-template-columns: minmax(0, 1fr) 188px;
  gap: 10px;
}

.map-aside {
  gap: 8px;
}

.map-aside .inspect-card {
  background: linear-gradient(180deg, rgba(10, 16, 23, 0.52), rgba(8, 13, 19, 0.36));
  border-color: rgba(114, 141, 173, 0.1);
}

.graph-stage {
  min-height: 780px;
  border-radius: 30px;
}

.graph-stage::after {
  opacity: 0.12;
}

.map-stage-overlay {
  max-width: 340px;
  padding: 13px 15px;
  background: linear-gradient(180deg, rgba(9, 15, 22, 0.42), rgba(7, 12, 18, 0.18));
  border-color: rgba(141, 182, 255, 0.08);
  box-shadow: 0 10px 26px rgba(0, 0, 0, 0.14);
}

.graph-toolbar {
  left: 18px;
  bottom: 18px;
  display: grid;
  gap: 10px;
  min-width: 292px;
  padding: 12px;
  background: rgba(7, 12, 18, 0.42);
  border-color: rgba(141, 182, 255, 0.08);
  box-shadow: 0 14px 32px rgba(0, 0, 0, 0.18);
}

.graph-toolbar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.graph-toolbar-title {
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: var(--text-faint);
}

.graph-toolbar-copy {
  color: var(--text-muted);
  font-size: 0.84rem;
}

.graph-control-stack {
  display: grid;
  gap: 10px;
}

.graph-control-row {
  display: grid;
  gap: 8px;
}

.graph-control-label {
  color: var(--text-faint);
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.14em;
}

.graph-control-group,
.graph-filter-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
}

.graph-filter-grid {
  gap: 6px;
}

.graph-tool-button,
.graph-chip,
.graph-filter-chip {
  min-height: 32px;
  padding: 0 11px;
  border-radius: 999px;
  border: 1px solid rgba(141, 182, 255, 0.08);
  background: rgba(10, 16, 23, 0.42);
  color: var(--text-muted);
  cursor: pointer;
  transition: 120ms ease;
}

.graph-tool-button:hover,
.graph-chip:hover,
.graph-filter-chip:hover {
  color: var(--text);
  border-color: rgba(141, 182, 255, 0.18);
}

.graph-tool-button.active,
.graph-chip.active,
.graph-filter-chip.active {
  background: rgba(141, 182, 255, 0.12);
  color: var(--accent-strong);
  border-color: rgba(141, 182, 255, 0.28);
}

.graph-tool-button {
  width: auto;
  height: 32px;
}

.graph-chip,
.graph-filter-chip {
  font-size: 0.78rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.graph-toolbar details {
  border-top: 1px solid rgba(114, 141, 173, 0.08);
  padding-top: 10px;
}

.graph-toolbar summary {
  cursor: pointer;
  list-style: none;
  color: var(--text-soft);
  font-size: 0.84rem;
}

.graph-toolbar summary::-webkit-details-marker { display: none; }

.graph-advanced-grid {
  display: grid;
  gap: 10px;
  margin-top: 10px;
}

.graph-range-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.graph-range {
  display: grid;
  gap: 6px;
}

.graph-range.compact {
  padding: 10px;
  border: 1px solid rgba(141, 182, 255, 0.08);
  border-radius: 14px;
  background: rgba(10, 16, 24, 0.44);
}

.graph-range-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  color: var(--text-muted);
  font-size: 0.8rem;
}

.graph-range input[type="range"] {
  width: 100%;
  accent-color: var(--accent);
}

#map-legend {
  display: grid;
  gap: 8px;
}

.map-legend-grid {
  display: grid;
  gap: 6px;
}

.map-legend-row {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  color: var(--text-muted);
  font-size: 0.84rem;
}

.map-legend-row strong {
  color: var(--text-soft);
  font-weight: 600;
}

.graph-link {
  stroke-width: 0.92;
  opacity: 0.2;
  filter: none;
}

.graph-link.active {
  stroke-width: 1.54;
  opacity: 1;
}

.graph-link.blocks {
  stroke: rgba(255, 154, 147, 0.86);
  stroke-width: 1.2;
}

.graph-link.supports {
  stroke: rgba(117, 176, 255, 0.54);
  stroke-linecap: round;
}

.graph-link.requires {
  stroke: rgba(191, 205, 231, 0.42);
  stroke-dasharray: 9 8;
}

.graph-link.impacts {
  stroke: rgba(240, 195, 122, 0.58);
  stroke-dasharray: 12 10;
  animation: lowPulse 4.8s ease-in-out infinite;
}

.graph-link.references {
  stroke: rgba(155, 170, 189, 0.28);
  stroke-dasharray: 2 8;
}

.graph-link.owns,
.graph-link.ownership {
  stroke: rgba(166, 179, 196, 0.44);
  stroke-width: 1.34;
}

.graph-link.muted { opacity: 0.06; }

.graph-link.contextual { opacity: 0.2; }
.graph-link.secondary { opacity: 0.45; }
.graph-link.primary-tone { opacity: 1; }

.graph-link-label {
  opacity: 0;
  font-size: 1.8px;
}

.graph-link-label.visible,
.graph-link-label.active {
  opacity: 0.84;
}

.graph-node {
  min-width: 0;
  max-width: 160px;
  padding: 0;
  background: transparent;
  border: 0;
  box-shadow: none;
  backdrop-filter: none;
}

.graph-node::before {
  content: "";
  position: absolute;
  inset: 8px 12px;
  border-radius: 999px;
  background: rgba(17, 28, 40, 0.12);
  box-shadow: 0 0 0 18px rgba(141, 182, 255, 0.012);
}

.graph-node.primary::before {
  inset: -6px;
  background: radial-gradient(circle, rgba(169, 143, 255, 0.2), rgba(32, 26, 53, 0.1) 58%, transparent 76%);
  box-shadow: 0 0 0 34px rgba(151, 134, 255, 0.08), 0 0 48px rgba(151, 134, 255, 0.16);
}

.graph-node:hover,
.graph-node.focused {
  transform: translate(-50%, -50%);
}

.graph-node.focused::before {
  box-shadow: 0 0 0 26px rgba(141, 182, 255, 0.05), 0 0 28px rgba(141, 182, 255, 0.18);
}

.graph-node-shell {
  position: relative;
  z-index: 1;
  display: grid;
  gap: 4px;
  justify-items: center;
  text-align: center;
}

.graph-node-glyph {
  width: 11px;
  height: 11px;
  border-radius: 999px;
  background: rgba(141, 182, 255, 0.72);
  box-shadow: 0 0 0 6px rgba(141, 182, 255, 0.08);
}

.graph-node.cycle .graph-node-glyph { background: rgba(170, 143, 255, 0.92); }
.graph-node.activity .graph-node-glyph { background: rgba(111, 177, 255, 0.82); }
.graph-node.document .graph-node-glyph { background: rgba(240, 195, 122, 0.82); }
.graph-node.entity .graph-node-glyph { background: rgba(143, 176, 159, 0.78); }
.graph-node.risk .graph-node-glyph { background: rgba(255, 154, 147, 0.88); }

.graph-node-title,
.graph-node-state {
  position: relative;
  z-index: 1;
}

.graph-node-title {
  font-size: 0.84rem;
  line-height: 1.24;
}

.graph-node.primary .graph-node-title {
  font-size: 1.04rem;
}

.graph-node-state {
  margin-top: 2px;
  padding: 3px 8px;
  background: rgba(15, 24, 35, 0.24);
  color: rgba(237, 243, 248, 0.66);
}

.flow-grid {
  grid-template-columns: 1.06fr 0.9fr 0.96fr;
  gap: 10px;
}

.lane {
  padding: 14px;
}

.inspect-grid {
  grid-template-columns: 1.78fr 0.52fr;
  gap: 10px;
}

.inspect-focus {
  padding: 18px 18px 22px;
}

.inspect-focus .mini-map-wrap {
  margin-top: 0;
  margin-bottom: 14px;
}

.decision-surface {
  gap: 10px;
}

.decision-surface > .inspect-card {
  padding: 14px;
}

.audit-group {
  background: linear-gradient(180deg, rgba(11, 17, 24, 0.76), rgba(8, 13, 19, 0.54));
}

.audit-entry {
  padding-top: 10px;
  margin-top: 10px;
  border-top: 1px solid rgba(114, 141, 173, 0.08);
}

.workspace-grid.map-immersive {
  grid-template-columns: 144px minmax(0, 1fr) 226px;
  gap: 10px;
}

.workspace-grid.map-immersive #left-rail,
.workspace-grid.map-immersive #right-rail {
  opacity: 0.48;
}

.workspace-grid.map-immersive #left-rail,
.workspace-grid.map-immersive #right-rail,
.workspace-grid.map-immersive .main-nav,
.workspace-grid.map-immersive + * {
  transition: opacity 180ms ease;
}

.workspace-grid.map-immersive.rails-soft #left-rail,
.workspace-grid.map-immersive.rails-soft #right-rail {
  opacity: 0.16;
}

.workspace-grid.map-immersive .view-surface {
  padding: 8px 10px 14px;
  background:
    radial-gradient(circle at 50% 8%, rgba(151, 134, 255, 0.08), transparent 24%),
    linear-gradient(180deg, rgba(10, 16, 23, 0.98), rgba(8, 13, 19, 1));
}

.workspace-grid.map-immersive .map-layout {
  grid-template-columns: minmax(0, 1fr) 158px;
  gap: 8px;
}

.workspace-grid.map-immersive .graph-stage {
  min-height: calc(100vh - 290px);
}

.workspace-grid.map-immersive.rails-soft .map-aside {
  opacity: 0.28;
}

@keyframes lowPulse {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 0.72; }
}

#audit-snapshot .detail-callout {
  background: rgba(10, 16, 23, 0.4);
}

.quiet-details {
  border: 1px solid var(--line);
  border-radius: var(--radius-sm);
  background: rgba(9, 16, 24, 0.34);
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
  color: var(--text-faint);
  background: rgba(9, 16, 24, 0.34);
}

.muted { color: var(--text-muted); }

@media (max-width: 1320px) {
  .workspace-grid {
    grid-template-columns: 1fr;
  }
  .inspect-grid,
  .overview-grid,
  .map-layout,
  .flow-grid,
  .cycle-context-bar {
    grid-template-columns: 1fr;
  }
  .graph-stage { min-height: 560px; }
  .map-stage-overlay {
    position: relative;
    left: auto;
    top: auto;
    margin: 16px;
    max-width: none;
  }
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
        trace pressure, and judge evidence before acting.
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
    <button class="nav-button" type="button" data-view="overview">OVERVIEW</button>
    <button class="nav-button active" type="button" data-view="map">MAP</button>
    <button class="nav-button" type="button" data-view="flow">FLOW</button>
    <button class="nav-button" type="button" data-view="inspect">INSPECT</button>
    <button class="nav-button" type="button" data-view="audit">AUDIT</button>
  </nav>

  <section id="workspace-grid" class="workspace-grid">
    <aside id="left-rail" class="surface rail stack">
      <section>
        <h2 class="section-title">Cycle Index</h2>
        <p class="section-copy">Cycles anchor the field.</p>
        <ul id="cycle-index" class="list-reset stack"></ul>
      </section>

      <section>
        <h2 class="section-title">Structural Context</h2>
        <p class="quiet-copy">Structural support, kept quiet.</p>
        <div id="ontology-list" class="stack"></div>
      </section>

      <section>
        <h2 class="section-title">Workspace Pulse</h2>
        <div id="workspace-pulse" class="stack"></div>
      </section>
    </aside>

    <section class="surface view-surface">
      <section id="overview-view" class="view-panel" hidden>
        <div class="view-head">
          <div class="view-head-copy">
            <h2 class="section-title">OVERVIEW</h2>
            <p class="section-copy">
              Scan the current operational frame, surface the primary tension, and step directly into the live map.
            </p>
          </div>
        </div>
        <div id="overview-grid" class="view-body overview-grid"></div>
        <div id="overview-field" class="mini-map-wrap"></div>
      </section>

      <section id="map-view" class="view-panel">
        <div class="view-head">
          <div class="view-head-copy">
            <h2 class="section-title">MAP</h2>
            <p class="section-copy">
              Read the workspace as a living institutional map. The focused cycle anchors the scene,
              activities reveal pressure, and documents carry the evidence layer.
            </p>
          </div>
          <div id="map-mode-switcher" class="map-mode-switcher">
            <button class="tab-button active" type="button" data-map-mode="signal">SIGNAL</button>
            <button class="tab-button" type="button" data-map-mode="structure">STRUCTURE</button>
            <button class="tab-button" type="button" data-map-mode="pressure">PRESSURE</button>
            <button class="tab-button" type="button" data-map-mode="trace">TRACE</button>
          </div>
        </div>
        <div class="view-body map-layout">
          <section id="graph-stage" class="surface graph-stage">
            <div class="graph-viewport"><div id="graph-world" class="graph-world"></div></div>
            <div id="hover-probe" class="hover-probe" hidden></div>
            <div id="map-field-controls" class="graph-toolbar"></div>
          </section>
          <aside class="map-aside">
            <article class="surface inspect-card">
              <h3>Read the scene</h3>
              <p class="quiet-copy" id="map-guide-copy">
                Select a node to move directly into operational inspection.
              </p>
              <div class="badge-row" id="map-legend"></div>
            </article>
            <article class="surface inspect-card">
              <h3>Cycle narrative</h3>
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
              what is moving, and which documents are carrying operational legitimacy.
            </p>
          </div>
        </div>
        <div id="flow-field" class="mini-map-wrap"></div>
        <div class="toolbar">
          <select id="flow-status-filter">
            <option value="">All flow states</option>
            <option value="attention">Requires action now</option>
            <option value="moving">Moving now</option>
            <option value="stable">Stabilized</option>
          </select>
        </div>
        <div class="view-body flow-grid">
          <section class="surface lane lane-attention">
            <div class="lane-header">
              <h3>Requires action now</h3>
              <p class="quiet-copy">Blocked and pending work that should shape the next intervention.</p>
              <div class="badge-row" id="flow-attention-meta"></div>
            </div>
            <div id="flow-attention" class="lane-items"></div>
          </section>
          <section class="surface lane lane-moving">
            <div class="lane-header">
              <h3>Moving now</h3>
              <p class="quiet-copy">Work already in motion inside the selected cycle.</p>
              <div class="badge-row" id="flow-moving-meta"></div>
            </div>
            <div id="flow-moving" class="lane-items"></div>
          </section>
          <section class="surface lane lane-stable">
            <div class="lane-header">
              <h3>Stabilized and support</h3>
              <p class="quiet-copy">Completed work and the documents currently supporting the cycle.</p>
              <div class="badge-row" id="flow-stable-meta"></div>
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
              available, but secondary.
            </p>
          </div>
        </div>
        <div class="view-body inspect-grid">
          <section class="surface inspect-focus">
            <div id="inspect-field" class="mini-map-wrap"></div>
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
              <div class="detail-stack-label">Primary focus</div>
              <div id="selected-primary" class="stack"></div>
              <div class="detail-stack-label">Supporting context</div>
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
        <div id="audit-field" class="mini-map-wrap"></div>
        <div id="audit-timeline" class="view-body"></div>
      </section>
    </section>

    <aside id="right-rail" class="surface decision-surface">
      <article class="inspect-card">
        <h3>What matters now</h3>
        <div id="operator-guidance" class="evidence-block">
          Cycle pressure and evidence health will guide action once the workspace loads.
        </div>
      </article>
      <article class="inspect-card">
        <h3>Context support</h3>
        <div id="document-primary" class="stack"></div>
        <details class="quiet-details">
          <summary>More support</summary>
          <div id="document-strip" class="stack"></div>
        </details>
      </article>
      <details class="quiet-details rail-memory">
        <summary>Institutional memory</summary>
        <div id="audit-snapshot" class="stack"></div>
      </details>
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

function defaultMapEntityFilters() {
  return {
    cycles: true,
    activities: true,
    documents: true,
    entities: true,
    risks: true
  };
}

function defaultMapRelationFilters() {
  return {
    blocks: true,
    supports: true,
    requires: true,
    impacts: true,
    references: true,
    owns: true
  };
}

function defaultMapPhysics() {
  return {
    center: 0.58,
    repel: 0.52,
    link: 0.56,
    distance: 0.54,
    focus: 0.66
  };
}

const state = {
  view: "map",
  inspectTab: "context",
  mapMode: "signal",
  mapLabelDensity: "balanced",
  mapSpread: "balanced",
  mapFieldRegime: "global",
  mapDepth: "all",
  mapEntityFilters: defaultMapEntityFilters(),
  mapRelationFilters: defaultMapRelationFilters(),
  mapShowIsolated: false,
  mapControlsAdvanced: false,
  mapPhysics: defaultMapPhysics(),
  mapNodeSize: 1,
  mapLinkThickness: 1,
  mapFrozen: false,
  mapAnimate: true,
  status: null,
  entities: [],
  relations: [],
  documents: [],
  documentIntegrity: [],
  cycles: [],
  activities: [],
  audit: [],
  focusedCycleId: null,
  focusedNodeId: null,
  hoveredNodeId: null,
  isolatedNodeId: null,
  mapScale: 1,
  mapOffset: { x: 0, y: 0 },
  mapPositions: {},
  dragState: null,
  railSoftTimer: null,
  mapModel: null,
  mapSimulation: null,
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

function nodeKey(type, id) {
  return `${type}:${id}`;
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
  state.focusedNodeId = nodeKey(type, id);
  if (type === "cycle") {
    state.focusedCycleId = id;
  }
  void renderEverything();
}

function currentMapAnchorKey() {
  const cycle = pickFocusedCycle();
  if (state.mapFieldRegime === "focused" && state.focusedNodeId) return state.focusedNodeId;
  if (cycle) return nodeKey("cycle", cycle.id);
  return null;
}

function revealRails() {
  const grid = document.getElementById("workspace-grid");
  if (!grid) return;
  grid.classList.remove("rails-soft");
  if (state.railSoftTimer) {
    clearTimeout(state.railSoftTimer);
  }
  if (state.view === "map") {
    state.railSoftTimer = setTimeout(() => {
      const liveGrid = document.getElementById("workspace-grid");
      if (liveGrid && state.view === "map") {
        liveGrid.classList.add("rails-soft");
      }
    }, 2000);
  }
}

function syncFieldRegime() {
  const grid = document.getElementById("workspace-grid");
  if (!grid) return;
  grid.classList.toggle("map-immersive", state.view === "map");
  if (state.view !== "map") {
    grid.classList.remove("rails-soft");
    if (state.railSoftTimer) {
      clearTimeout(state.railSoftTimer);
      state.railSoftTimer = null;
    }
    return;
  }
  revealRails();
}

function activateView(view) {
  state.view = view;
  document.querySelectorAll("[data-view]").forEach((button) => {
    button.classList.toggle("active", button.dataset.view === view);
  });
  ["overview", "map", "flow", "inspect", "audit"].forEach((name) => {
    const panel = document.getElementById(`${name}-view`);
    if (panel) {
      panel.hidden = name !== view;
    }
  });
  syncFieldRegime();
  if (view !== "map") {
    stopMapSimulation();
  } else if (state.mapModel) {
    startMapSimulation(state.mapModel);
  }
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
    `<strong>${escapeHtml(status.workspace_name || "Nexus workspace")}</strong><div class="card-secondary">${status.db_present ? "Local state ready" : "Local state missing"} • schema ${escapeHtml(status.schema_version || "-")}</div>`
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

function activityCardSummary(activity) {
  if (activity.status === "blocked") {
    return "Blocked work requiring intervention before the cycle can move cleanly.";
  }
  if (activity.status === "in_progress") {
    return "Work currently moving inside the focused cycle.";
  }
  if (activity.status === "completed") {
    return "Completed work now stabilizing the cycle.";
  }
  return "Queued work ready to move when the operator advances it.";
}

function documentCardSummary(document) {
  const integrity = integrityFor(document.id);
  const integrityLabel =
    integrity?.integrity_state === "warning"
      ? "Integrity drift needs review."
      : integrity?.integrity_state === "error"
      ? "Integrity is out of sync."
      : "Integrity is aligned.";
  if (document.status === "approved") {
    return `Approved support material for the current operational picture. ${integrityLabel}`;
  }
  if (document.status === "archived") {
    return `Archived reference retained for institutional memory. ${integrityLabel}`;
  }
  return `Working support material still being stabilized. ${integrityLabel}`;
}

function describeAuditEntry(entry) {
  const actor = entry.agent || "system";
  const objectLabel = auditObjectLabel(entry);
  if (entry.entity_type === "document" && entry.action === "reconcile") {
    return `${actor} reconciled ${objectLabel} so the evidence record could be trusted again.`;
  }
  if (entry.entity_type === "document" && entry.action === "update") {
    return `${actor} changed the lifecycle state of ${objectLabel}, shifting what evidence is institutionally valid now.`;
  }
  if (entry.entity_type === "activity" && entry.action === "update") {
    return `${actor} changed ${objectLabel}, altering the pressure pattern inside the focused cycle.`;
  }
  if (entry.action === "create") {
    return `${actor} introduced ${objectLabel} into the workspace, widening the current operational picture.`;
  }
  return `${actor} updated ${objectLabel}. ${entry.reason || "No explicit reason was recorded."}`;
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

function auditContextLabel(entry) {
  const entity = titleCase(entry.entity_type);
  const action =
    entry.action === "create"
      ? "Created"
      : entry.action === "update"
      ? "State changed"
      : entry.action === "reconcile"
      ? "Reconciled"
      : titleCase(entry.action || "Event");
  return `${entity} • ${action}`;
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

function dominantIntegrityIssue(cycle) {
  if (!cycle) return null;
  return relatedDocuments(cycle.id)
    .map((document) => ({ document, integrity: integrityFor(document.id) }))
    .find(({ integrity }) => integrity && integrity.integrity_state !== "ok") || null;
}

function nextOperationalFocus(cycle) {
  if (!cycle) return null;
  return (
    relatedActivities(cycle.id).find((item) => item.status === "blocked") ||
    relatedActivities(cycle.id).find((item) => item.status === "pending") ||
    relatedActivities(cycle.id).find((item) => item.status === "in_progress") ||
    null
  );
}

function renderOverviewView() {
  const cycle = pickFocusedCycle();
  if (!cycle) {
    setHtml("overview-grid", '<div class="empty-state">Seed the workspace to generate an operational frame.</div>');
    renderMiniMapField("overview-field", null);
    return;
  }
  const summary = summarizeCycle(cycle);
  const issue = dominantIntegrityIssue(cycle);
  const focus = nextOperationalFocus(cycle);
  const issueMarkup = issue
    ? `<div class="badge-row"><span class="badge danger">${escapeHtml(statusLabel(issue.integrity.integrity_state))}</span><span class="badge warning">${escapeHtml(issue.document.title)}</span></div><div class="card-secondary">${escapeHtml(documentNarrative(issue.document))}</div>`
    : `<div class="badge-row"><span class="badge success">Evidence steady</span></div><div class="card-secondary">No document is currently drifting away from the operational record.</div>`;
  const focusMarkup = focus
    ? `<div class="badge-row"><span class="badge ${statusBadgeClass(focus.status)}">${escapeHtml(statusLabel(focus.status))}</span></div><div class="card-title">${escapeHtml(focus.title)}</div><div class="card-secondary">${escapeHtml(activityNarrative(focus))}</div>`
    : `<div class="card-secondary">No immediate work item is asking for intervention.</div>`;
  setHtml(
    "overview-grid",
    `
      <article class="overview-hero">
        <div class="overview-kicker">Current operating frame</div>
        <div class="overview-title">${escapeHtml(cycleLabel(cycle))}</div>
        <div class="overview-copy">${escapeHtml(cycleNarrative(cycle))}</div>
        <div class="badge-row">
          <span class="badge ${statusBadgeClass(cycle.status)}">${escapeHtml(statusLabel(cycle.status))}</span>
          <span class="badge ${statusBadgeClass(summary.pressure === "Critical" ? "blocked" : summary.pressure === "Elevated" ? "pending" : "completed")}">${escapeHtml(summary.pressure)}</span>
          <span class="badge ${statusBadgeClass(summary.evidence === "Fragile" ? "warning" : summary.evidence === "Degraded" ? "error" : "completed")}">${escapeHtml(summary.evidence)}</span>
        </div>
        <div class="action-row">
          <button class="inline-button primary" type="button" data-view="map">Enter MAP</button>
          <button class="inline-button" type="button" data-view="inspect">Open judgment surface</button>
        </div>
      </article>
      <article class="overview-card">
        <h3>Primary evidence signal</h3>
        ${issueMarkup}
      </article>
      <article class="overview-card">
        <h3>Immediate operational focus</h3>
        ${focusMarkup}
      </article>
    `
  );
  renderMiniMapField("overview-field", cycle, "The field remains present here in compressed form. Enter MAP when you need full relational depth.");
}

function auditContextLabel(entry) {
  const entity = titleCase(entry.entity_type);
  const action =
    entry.action === "create"
      ? "Created"
      : entry.action === "update"
      ? "State changed"
      : entry.action === "reconcile"
      ? "Reconciled"
      : titleCase(entry.action || "Event");
  return `${entity} • ${action}`;
}

function cycleIdForAuditEntry(entry) {
  if (entry.entity_type === "cycle") return entry.entity_id;
  if (entry.entity_type === "activity") return activityById(entry.entity_id)?.cycle_id || null;
  if (entry.entity_type === "document") return documentById(entry.entity_id)?.cycle_id || null;
  return null;
}

function groupAuditEntries(entries) {
  const groups = new Map();
  entries.forEach((entry) => {
    let spec;
    if (entry.entity_type === "document" && ["update", "reconcile"].includes(entry.action)) {
      spec = {
        key: "evidence",
        title: "Evidence drift or reconcile",
        copy: "Supporting material changed trust state, drifted, or was brought back into alignment."
      };
    } else if (entry.action === "update") {
      spec = {
        key: "state",
        title: "State changed",
        copy: "Operational status shifts changed what the cycle could do next."
      };
    } else {
      spec = {
        key: "work",
        title: "Work created or linked",
        copy: "Objects entered the workspace or became part of the current operational frame."
      };
    }
    if (!groups.has(spec.key)) {
      groups.set(spec.key, { spec, entries: [] });
    }
    groups.get(spec.key).entries.push(entry);
  });
  return Array.from(groups.values());
}

function auditContextLabel(entry) {
  const entity = titleCase(entry.entity_type);
  const action =
    entry.action === "create"
      ? "Created"
      : entry.action === "update"
      ? "State changed"
      : entry.action === "reconcile"
      ? "Reconciled"
      : titleCase(entry.action || "Event");
  return `${entity} • ${action}`;
}

function groupAuditEntries(entries) {
  const groups = new Map();
  entries.forEach((entry) => {
    let spec;
    if (entry.action === "reconcile") {
      spec = {
        key: "reconcile",
        title: "Reconcile",
        copy: "Evidence drift was brought back into alignment so the record could be trusted again."
      };
    } else if (entry.entity_type === "document" && entry.action === "update") {
      spec = {
        key: "decision",
        title: "Decision",
        copy: "Document legitimacy changed, shifting what evidence can currently authorize action."
      };
    } else if (entry.entity_type === "activity" && entry.action === "update") {
      spec = {
        key: "escalation",
        title: "Escalation",
        copy: "Operational pressure changed inside the cycle and altered what needs intervention now."
      };
    } else if (entry.action === "create") {
      spec = {
        key: "trigger",
        title: "Trigger",
        copy: "Objects entered the workspace and widened the current operational frame."
      };
    } else {
      spec = {
        key: "consequence",
        title: "Consequence",
        copy: "Residual state changes now shape how the cycle should be read and acted upon."
      };
    }
    if (!groups.has(spec.key)) {
      groups.set(spec.key, { spec, entries: [] });
    }
    groups.get(spec.key).entries.push(entry);
  });
  return Array.from(groups.values());
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
      data-node-key="${escapeHtml(node.key)}"
      data-node-kind="${escapeHtml(node.kind)}"
      data-node-summary="${escapeHtml(node.summary)}"
      data-node-depth="${escapeHtml(String(node.depth ?? 99))}"
    >
      <div class="graph-node-shell">
        <div class="graph-node-glyph" aria-hidden="true"></div>
        <div class="graph-node-title">${escapeHtml(node.title)}</div>
        <div class="graph-node-state">${escapeHtml(node.stateLabel)}</div>
      </div>
    </button>
  `;
}

function graphLinkPath(from, to, type) {
  const x1 = from.x;
  const y1 = from.y;
  const x2 = to.x;
  const y2 = to.y;
  const dx = x2 - x1;
  const dy = y2 - y1;
  const relation = relationTone(type);
  const curveBias =
    relation === "blocks" ? 1.18 :
    relation === "supports" ? 0.82 :
    relation === "requires" ? 0.92 :
    relation === "impacts" ? 1.06 :
    relation === "owns" ? 0.68 :
    0.74;
  const curvature = Math.max(6, Math.min(22, (Math.abs(dx) * 0.18 + Math.abs(dy) * 0.12) * curveBias));
  const c1x = x1 + dx * 0.28;
  const c2x = x2 - dx * 0.24;
  const c1y = y1 - curvature;
  const c2y = y2 + curvature * 0.76;
  return `M ${x1} ${y1} C ${c1x} ${c1y}, ${c2x} ${c2y}, ${x2} ${y2}`;
}

function relationTone(type) {
  if (type === "blocks") return "blocks";
  if (type === "supports") return "supports";
  if (type === "requires") return "requires";
  if (type === "impacts") return "impacts";
  if (["owns", "owner_of", "ownership"].includes(type)) return "owns";
  return "references";
}

function relationLabel(type) {
  return titleCase(type || "linked");
}

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value));
}

function relationPriority(type) {
  if (["blocks", "impacts"].includes(type)) return "primary";
  if (["supports", "requires", "owns", "owner_of", "ownership"].includes(type)) return "secondary";
  return "contextual";
}

function depthLimitValue() {
  return state.mapDepth === "all" ? Number.POSITIVE_INFINITY : Number(state.mapDepth);
}

function kindFilterKey(kind) {
  if (kind === "risk") return "risks";
  if (kind === "entity") return "entities";
  if (kind === "cycle") return "cycles";
  if (kind === "activity") return "activities";
  return "documents";
}

function relationFilterEnabled(type) {
  return state.mapRelationFilters[relationTone(type)] !== false;
}

function nodeFilterEnabled(kind) {
  return state.mapEntityFilters[kindFilterKey(kind)] !== false;
}

function neighborhoodDepthMap(model, anchorKey) {
  const adjacency = new Map();
  model.nodes.forEach((node) => adjacency.set(node.key, new Set()));
  model.links.forEach((link) => {
    if (!adjacency.has(link.from)) adjacency.set(link.from, new Set());
    if (!adjacency.has(link.to)) adjacency.set(link.to, new Set());
    adjacency.get(link.from).add(link.to);
    adjacency.get(link.to).add(link.from);
  });
  const depth = new Map();
  if (!anchorKey || !adjacency.has(anchorKey)) {
    model.nodes.forEach((node) => depth.set(node.key, Number.POSITIVE_INFINITY));
    return depth;
  }
  const queue = [[anchorKey, 0]];
  depth.set(anchorKey, 0);
  while (queue.length) {
    const [key, level] = queue.shift();
    adjacency.get(key).forEach((next) => {
      if (!depth.has(next)) {
        depth.set(next, level + 1);
        queue.push([next, level + 1]);
      }
    });
  }
  model.nodes.forEach((node) => {
    if (!depth.has(node.key)) depth.set(node.key, Number.POSITIVE_INFINITY);
  });
  return depth;
}

function modeAllowsRelation(type) {
  const normalized = relationTone(type);
  if (state.mapMode === "signal") return ["blocks", "impacts", "supports", "requires"].includes(normalized);
  if (state.mapMode === "structure") return ["owns", "references"].includes(normalized);
  if (state.mapMode === "pressure") return ["blocks", "impacts", "requires"].includes(normalized);
  if (state.mapMode === "trace") return ["supports", "references", "requires", "impacts"].includes(normalized);
  return true;
}

function modeHighlightsNode(node) {
  if (state.mapMode === "signal") return node.kind === "risk" || (node.kind === "document" && /error|drift|fragile|degraded/i.test(node.stateLabel || ""));
  if (state.mapMode === "structure") return node.kind === "entity" || node.kind === "cycle";
  if (state.mapMode === "pressure") return node.kind === "activity" || node.kind === "risk";
  if (state.mapMode === "trace") return node.kind === "document" || node.kind === "activity";
  return true;
}

function buildRiskNodes(cycle) {
  const summary = summarizeCycle(cycle);
  const riskNodes = [];
  if (cycle.blocked_count > 0) {
    riskNodes.push({
      kind: "risk",
      id: `${cycle.id}-blocked`,
      key: nodeKey("risk", `${cycle.id}-blocked`),
      title: "Blocked pressure",
      stateLabel: `${cycle.blocked_count} blocked`,
      summary: "Blocked work is constraining the cycle and should be treated as immediate operational pressure."
    });
  }
  if (summary.integrityIssues > 0) {
    riskNodes.push({
      kind: "risk",
      id: `${cycle.id}-evidence`,
      key: nodeKey("risk", `${cycle.id}-evidence`),
      title: "Evidence drift",
      stateLabel: summary.integrityIssues > 1 ? "degraded" : "fragile",
      summary: "Supporting evidence is drifting away from the stored record and can invalidate action."
    });
  }
  return riskNodes;
}

function resolveMapAnchorKey(rawModel, cycle) {
  const cycleKey = nodeKey("cycle", cycle.id);
  if (state.mapFieldRegime === "focused" && state.focusedNodeId && rawModel.nodes.some((node) => node.key === state.focusedNodeId)) {
    return state.focusedNodeId;
  }
  return cycleKey;
}

function pruneIsolatedNodes(nodes, links, anchorKey) {
  const connected = new Set([anchorKey]);
  links.forEach((link) => {
    connected.add(link.from);
    connected.add(link.to);
  });
  return nodes.filter((node) => connected.has(node.key));
}

function preferredAngleForKind(kind) {
  if (kind === "risk") return -82;
  if (kind === "document") return -18;
  if (kind === "cycle") return -138;
  if (kind === "entity") return 56;
  return 176;
}

function spreadMultiplier() {
  return state.mapSpread === "compact" ? 0.84 : state.mapSpread === "spread" ? 1.18 : 1;
}

function blendNodePosition(key, target) {
  const previous = state.mapPositions[key];
  if (!previous) return target;
  const keep = clamp(0.34 + state.mapPhysics.link * 0.28, 0.24, 0.68);
  return {
    x: Number((previous.x * keep + target.x * (1 - keep)).toFixed(2)),
    y: Number((previous.y * keep + target.y * (1 - keep)).toFixed(2))
  };
}

function graphNodeMass(kind) {
  if (kind === "cycle") return 2.8;
  if (kind === "risk") return 1.9;
  if (kind === "activity") return 1.55;
  if (kind === "document") return 1.34;
  return 1.18;
}

function graphNodeScaleFor(node) {
  const base = node?.primary ? 1.12 : node?.kind === "risk" ? 0.94 : 1;
  return clamp(state.mapNodeSize * base, 0.72, 1.72);
}

function baseLinkDistance(type) {
  const tone = relationTone(type);
  if (tone === "blocks") return 12;
  if (tone === "supports") return 18;
  if (tone === "requires") return 16;
  if (tone === "impacts") return 21;
  if (tone === "owns") return 24;
  return 26;
}

function relationPhysicsProfile(type) {
  const tone = relationTone(type);
  if (tone === "blocks") {
    return { tension: 1.42, fromBias: 1, toBias: 1.08, alignX: 0.026, alignY: 0.012, vector: 0.005 };
  }
  if (tone === "supports") {
    return { tension: 1, fromBias: 1, toBias: 1, cluster: 0.01 };
  }
  if (tone === "requires") {
    return { tension: 0.88, fromBias: 0.72, toBias: 1.18, directional: 0.014 };
  }
  if (tone === "impacts") {
    return { tension: 1.16, fromBias: 0.92, toBias: 1.08, vector: 0.015 };
  }
  if (tone === "owns") {
    return { tension: 1.12, fromBias: 0.85, toBias: 1, radial: 0.034 };
  }
  return { tension: 0.58, fromBias: 1, toBias: 1 };
}

function stableNodeSeed(key) {
  let hash = 0;
  for (let index = 0; index < key.length; index += 1) {
    hash = (hash * 33 + key.charCodeAt(index)) % 1000003;
  }
  return hash / 1000003;
}

function layoutMapNodes(nodes, anchorKey, depthMap) {
  const center = { x: 50, y: 51.5 };
  const positioned = [];
  const anchor = nodes.find((node) => node.key === anchorKey);
  if (anchor) {
    const target = blendNodePosition(anchor.key, center);
    positioned.push({ ...anchor, ...target, targetX: target.x, targetY: target.y, depth: 0, primary: true });
  }
  const density = spreadMultiplier();
  const rings = new Map();
  nodes.forEach((node) => {
    if (node.key === anchorKey) return;
    const depth = depthMap.get(node.key);
    const ringKey = Number.isFinite(depth) ? Math.min(depth, 3) : 3;
    if (!rings.has(ringKey)) rings.set(ringKey, []);
    rings.get(ringKey).push(node);
  });

  Array.from(rings.entries()).sort((a, b) => a[0] - b[0]).forEach(([ring, ringNodes]) => {
    const radiusBase = (ring === 1 ? 23 : ring === 2 ? 35 : 47) * density;
    const radius = radiusBase + state.mapPhysics.distance * 10 - state.mapPhysics.center * 4;
    const groups = new Map();
    ringNodes
      .sort((left, right) => left.kind.localeCompare(right.kind) || left.title.localeCompare(right.title))
      .forEach((node) => {
        if (!groups.has(node.kind)) groups.set(node.kind, []);
        groups.get(node.kind).push(node);
      });
    groups.forEach((items, kind) => {
      const centerAngle = preferredAngleForKind(kind);
      const band = 16 + Math.max(0, items.length - 1) * (8 + state.mapPhysics.repel * 6);
      items.forEach((node, index) => {
        const offset = items.length === 1 ? 0 : -band / 2 + (band / Math.max(items.length - 1, 1)) * index;
        const radians = (centerAngle + offset) * (Math.PI / 180);
        const target = {
          x: clamp(50 + Math.cos(radians) * radius, 8, 92),
          y: clamp(51.5 + Math.sin(radians) * radius * 0.74, 10, 90)
        };
        const blended = blendNodePosition(node.key, target);
        positioned.push({ ...node, ...blended, targetX: blended.x, targetY: blended.y, depth: ring, primary: false });
      });
    });
  });

  return positioned;
}

function stopMapSimulation() {
  if (state.mapSimulation) {
    syncMapPositionsFromSimulation(state.mapSimulation);
  }
  if (state.mapSimulation?.rafId) {
    cancelAnimationFrame(state.mapSimulation.rafId);
  }
  state.mapSimulation = null;
}

function applyMapVisualTuning() {
  const stage = document.getElementById("graph-stage");
  if (stage) {
    stage.style.setProperty("--graph-link-scale", String(state.mapLinkThickness.toFixed(2)));
  }
  const liveNodes = state.mapSimulation?.nodes;
  document.querySelectorAll(".graph-node").forEach((element) => {
    const key = element.dataset.nodeKey;
    const node = (key && liveNodes?.get(key)) || state.mapModel?.nodes.find((item) => item.key === key);
    element.style.setProperty("--node-scale", String(graphNodeScaleFor(node)));
  });
}

function syncMapPositionsFromSimulation(simulation) {
  const nextPositions = {};
  simulation.nodes.forEach((node, key) => {
    nextPositions[key] = { x: Number(node.x.toFixed(2)), y: Number(node.y.toFixed(2)) };
  });
  state.mapPositions = nextPositions;
}

function applySimulationFrame(simulation) {
  const world = document.getElementById("graph-world");
  if (!world) return;
  const positions = new Map();
  simulation.nodes.forEach((node, key) => {
    positions.set(key, node);
    const element = world.querySelector(`[data-node-key="${CSS.escape(key)}"]`);
    if (element) {
      element.style.left = `${node.x.toFixed(2)}%`;
      element.style.top = `${node.y.toFixed(2)}%`;
    }
  });
  world.querySelectorAll(".graph-link").forEach((element) => {
    const linkId = element.dataset.linkId;
    const link = simulation.linkMap.get(linkId);
    if (!link) return;
    const from = positions.get(link.from);
    const to = positions.get(link.to);
    if (!from || !to) return;
    element.setAttribute("d", graphLinkPath(from, to, link.type));
  });
  world.querySelectorAll(".graph-link-label").forEach((element) => {
    const linkId = element.dataset.linkId;
    const link = simulation.linkMap.get(linkId);
    if (!link) return;
    const from = positions.get(link.from);
    const to = positions.get(link.to);
    if (!from || !to) return;
    element.setAttribute("x", ((from.x + to.x) / 2).toFixed(2));
    element.setAttribute("y", ((from.y + to.y) / 2).toFixed(2));
  });
  applyMapVisualTuning();
  renderHoverProbe();
}

function tickMapSimulation(timestamp) {
  const simulation = state.mapSimulation;
  if (!simulation || state.view !== "map") return;
  const frame = clamp((timestamp - simulation.lastFrame) / 16.7, 0.72, 1.72);
  simulation.lastFrame = timestamp;
  if (state.mapFrozen) {
    simulation.rafId = null;
    syncMapPositionsFromSimulation(simulation);
    return;
  }
  const nodes = Array.from(simulation.nodes.values());
  const anchor = simulation.nodes.get(simulation.anchorKey) || nodes[0];
  const centerX = 50;
  const centerY = 51.5;
  const repulsion = 0.018 + state.mapPhysics.repel * 0.11;
  const spring = 0.01 + state.mapPhysics.link * 0.045;
  const gravity = 0.004 + state.mapPhysics.center * 0.02;
  const focusGravity = 0.005 + state.mapPhysics.focus * 0.032;
  const preferredDistance = 0.7 + state.mapPhysics.distance * 0.85;

  for (let left = 0; left < nodes.length; left += 1) {
    for (let right = left + 1; right < nodes.length; right += 1) {
      const a = nodes[left];
      const b = nodes[right];
      const dx = b.x - a.x;
      const dy = b.y - a.y;
      const distance = Math.max(1.2, Math.hypot(dx, dy));
      const force = repulsion * ((a.mass + b.mass) / distance);
      const fx = (dx / distance) * force;
      const fy = (dy / distance) * force;
      a.vx -= fx / a.mass;
      a.vy -= fy / a.mass;
      b.vx += fx / b.mass;
      b.vy += fy / b.mass;
    }
  }

  simulation.links.forEach((link) => {
    const from = simulation.nodes.get(link.from);
    const to = simulation.nodes.get(link.to);
    if (!from || !to) return;
    const dx = to.x - from.x;
    const dy = to.y - from.y;
    const distance = Math.max(0.8, Math.hypot(dx, dy));
    const profile = relationPhysicsProfile(link.type);
    const desired = baseLinkDistance(link.type) * preferredDistance * spreadMultiplier();
    const error = distance - desired;
    const tension = spring * profile.tension * error;
    const nx = dx / distance;
    const ny = dy / distance;
    from.vx += nx * tension * profile.fromBias / from.mass;
    from.vy += ny * tension * profile.fromBias / from.mass;
    to.vx -= nx * tension * profile.toBias / to.mass;
    to.vy -= ny * tension * profile.toBias / to.mass;

    if (profile.alignX) {
      const align = dx * profile.alignX * 0.01;
      from.vx += align / from.mass;
      to.vx -= align / to.mass;
    }
    if (profile.alignY) {
      const alignY = dy * profile.alignY * 0.01;
      from.vy += alignY / from.mass;
      to.vy -= alignY / to.mass;
    }
    if (profile.directional) {
      const directional = profile.directional * 0.02;
      to.vx += nx * directional;
      to.vy += ny * directional * 0.4;
    }
    if (profile.vector) {
      const vector = profile.vector * 0.01;
      to.vx += nx * vector;
      to.vy += ny * vector;
    }
    if (profile.cluster) {
      const cluster = profile.cluster * 0.018;
      from.vx += (to.targetX - from.x) * cluster;
      from.vy += (to.targetY - from.y) * cluster;
      to.vx += (from.targetX - to.x) * cluster;
      to.vy += (from.targetY - to.y) * cluster;
    }
    if (profile.radial) {
      const radial = profile.radial * 0.015;
      to.vx += (to.targetX - to.x) * radial;
      to.vy += (to.targetY - to.y) * radial;
    }
  });

  let energy = 0;
  nodes.forEach((node) => {
    const memory = node.primary ? gravity * 1.28 : gravity;
    node.vx += (node.targetX - node.x) * memory;
    node.vy += (node.targetY - node.y) * memory;

    if (anchor && state.mapFieldRegime === "focused" && node.key !== anchor.key) {
      const depthFactor = 1 / Math.max(1, (node.depth ?? 1));
      node.vx += (anchor.x - node.x) * focusGravity * depthFactor * 0.12;
      node.vy += (anchor.y - node.y) * focusGravity * depthFactor * 0.12;
    }

    if (node.primary || node.key === simulation.anchorKey) {
      node.vx += (centerX - node.x) * gravity * 0.22;
      node.vy += (centerY - node.y) * gravity * 0.22;
    }

    if (state.mapAnimate) {
      const pulse = timestamp * 0.0012 + node.seed * Math.PI * 2;
      node.vx += Math.cos(pulse) * 0.0026;
      node.vy += Math.sin(pulse * 0.82) * 0.0021;
    }

    const damping = state.mapAnimate ? 0.88 : 0.81;
    node.vx *= damping;
    node.vy *= damping;
    node.x = clamp(node.x + node.vx * frame, 6, 94);
    node.y = clamp(node.y + node.vy * frame, 8, 92);
    energy += Math.abs(node.vx) + Math.abs(node.vy);
  });

  syncMapPositionsFromSimulation(simulation);
  applySimulationFrame(simulation);

  if (!state.mapAnimate && energy < 0.012) {
    simulation.rafId = null;
    return;
  }
  simulation.rafId = requestAnimationFrame(tickMapSimulation);
}

function startMapSimulation(model) {
  const previous = state.mapSimulation?.nodes || new Map();
  stopMapSimulation();
  if (!model?.nodes?.length) return;
  const nodes = new Map(
    model.nodes.map((node) => {
      const previousNode = previous.get(node.key);
      return [
        node.key,
        {
          ...node,
          x: previousNode?.x ?? node.x,
          y: previousNode?.y ?? node.y,
          vx: previousNode?.vx ?? 0,
          vy: previousNode?.vy ?? 0,
          mass: graphNodeMass(node.kind),
          seed: stableNodeSeed(node.key)
        }
      ];
    })
  );
  const simulation = {
    anchorKey: model.anchorKey,
    nodes,
    links: model.links.map((link) => ({ ...link })),
    linkMap: new Map(model.links.map((link) => [link.id, { ...link }])),
    lastFrame: performance.now(),
    rafId: null
  };
  state.mapSimulation = simulation;
  syncMapPositionsFromSimulation(simulation);
  applySimulationFrame(simulation);
  if (!state.mapFrozen) {
    simulation.rafId = requestAnimationFrame(tickMapSimulation);
  }
}

function buildRawMapModel(cycle) {
  const activities = relatedActivities(cycle.id);
  const documents = relatedDocuments(cycle.id);
  const contextualCycles = state.cycles.filter((item) => item.id !== cycle.id).slice(0, 4);
  const entities = state.entities.slice(0, 6);
  const riskNodes = buildRiskNodes(cycle);
  const nodes = [
    {
      kind: "cycle",
      id: cycle.id,
      key: nodeKey("cycle", cycle.id),
      title: cycleLabel(cycle),
      stateLabel: statusLabel(cycle.status),
      summary: cycleNarrative(cycle),
      selected: state.selected.type === "cycle" && state.selected.id === cycle.id
    },
    ...contextualCycles.map((item) => ({
      kind: "cycle",
      id: item.id,
      key: nodeKey("cycle", item.id),
      title: cycleLabel(item),
      stateLabel: statusLabel(item.status),
      summary: cycleNarrative(item),
      selected: state.selected.type === "cycle" && state.selected.id === item.id
    })),
    ...activities.map((item) => ({
      kind: "activity",
      id: item.id,
      key: nodeKey("activity", item.id),
      title: item.title,
      stateLabel: statusLabel(item.status),
      summary: activityNarrative(item),
      selected: state.selected.type === "activity" && state.selected.id === item.id
    })),
    ...documents.map((item) => ({
      kind: "document",
      id: item.id,
      key: nodeKey("document", item.id),
      title: item.title,
      stateLabel: statusLabel(item.status),
      summary: documentNarrative(item),
      selected: state.selected.type === "document" && state.selected.id === item.id
    })),
    ...entities.map((item) => ({
      kind: "entity",
      id: item.id,
      key: nodeKey("entity", item.id),
      title: item.name,
      stateLabel: titleCase(item.type),
      summary: `${item.name} remains part of the structural context around the focused cycle.`,
      selected: false
    })),
    ...riskNodes
  ];

  const links = [];
  contextualCycles.forEach((item) => {
    links.push({ id: `${cycle.id}:${item.id}:context`, from: nodeKey("cycle", cycle.id), to: nodeKey("cycle", item.id), type: "references" });
  });
  activities.forEach((item) => {
    links.push({ id: `${cycle.id}:${item.id}:activity`, from: nodeKey("cycle", cycle.id), to: nodeKey("activity", item.id), type: item.status === "blocked" ? "blocks" : "impacts" });
  });
  documents.forEach((item) => {
    links.push({ id: `${cycle.id}:${item.id}:document`, from: nodeKey("cycle", cycle.id), to: nodeKey("document", item.id), type: "supports" });
  });
  entities.forEach((item) => {
    links.push({ id: `${cycle.id}:${item.id}:entity`, from: nodeKey("cycle", cycle.id), to: nodeKey("entity", item.id), type: "owns" });
  });
  riskNodes.forEach((item) => {
    links.push({ id: `${cycle.id}:${item.id}:risk`, from: nodeKey("cycle", cycle.id), to: item.key, type: item.id.endsWith("-evidence") ? "impacts" : "blocks" });
  });
  activities.forEach((activity) => {
    const supportingDocument = supportingDocumentForActivity(activity);
    if (!supportingDocument) return;
    links.push({ id: `${activity.id}:${supportingDocument.id}:support`, from: nodeKey("activity", activity.id), to: nodeKey("document", supportingDocument.id), type: activity.status === "blocked" ? "requires" : "supports" });
  });
  state.relations.forEach((relation) => {
    const from = nodeKey("entity", relation.entity_a_id);
    const to = nodeKey("entity", relation.entity_b_id);
    if (!nodes.some((node) => node.key === from) || !nodes.some((node) => node.key === to)) return;
    links.push({ id: relation.id, from, to, type: relationTone(relation.type) });
  });
  return { nodes, links };
}

function renderMiniMapField(targetId, cycle, copy) {
  const target = document.getElementById(targetId);
  if (!target) return;
  if (!cycle) {
    target.innerHTML = '<div class="empty-state">No cycle context is available yet.</div>';
    return;
  }
  const model = buildMapModel(cycle);
  const anchorKey = model.anchorKey || currentMapAnchorKey() || nodeKey("cycle", cycle.id);
  const nodes = model.nodes.filter((node) => (node.depth ?? 99) <= 2);
  const allowed = new Set(nodes.map((node) => node.key));
  const links = model.links.filter((link) => allowed.has(link.from) && allowed.has(link.to));
  const positions = Object.fromEntries(nodes.map((node) => [node.key, node]));
  const linkMarkup = links.map((link) => {
    const from = positions[link.from];
    const to = positions[link.to];
    if (!from || !to) return "";
    return `<path class="mini-map-link ${escapeHtml(relationTone(link.type))}" d="${graphLinkPath(from, to, link.type)}"></path>`;
  }).join("");
  const nodeMarkup = nodes.map((node) => {
    const dim = (node.depth ?? 99) === 2 ? "dim" : "";
    const showLabel = node.kind === "cycle" || node.key === anchorKey;
    return `
      <button
        class="mini-map-node ${escapeHtml(node.kind)} ${dim}"
        type="button"
        style="left:${node.x}%; top:${node.y}%"
        data-mini-map-jump="${escapeHtml(node.key)}"
        aria-label="Open ${escapeHtml(node.title)} in MAP"
      ></button>
      ${showLabel ? `<div class="mini-map-label" style="left:${node.x}%; top:${node.y}%">${escapeHtml(node.title)}</div>` : ""}
    `;
  }).join("");
  target.innerHTML = `
    <div class="mini-map-field">
      <svg class="mini-map-svg" viewBox="0 0 100 100" preserveAspectRatio="none">${linkMarkup}</svg>
      ${nodeMarkup}
      <div class="mini-map-overlay">
        <div class="mini-map-copy">${escapeHtml(copy || cycleNarrative(cycle))}</div>
        <button class="mini-map-jump" type="button" data-view="map">Open MAP</button>
      </div>
    </div>
  `;
}

function buildMapModel(cycle) {
  const raw = buildRawMapModel(cycle);
  const anchorKey = resolveMapAnchorKey(raw, cycle);
  const filteredNodes = raw.nodes.filter((node) => nodeFilterEnabled(node.kind));
  const allowedNodeKeys = new Set(filteredNodes.map((node) => node.key));
  let filteredLinks = raw.links.filter((link) => {
    return allowedNodeKeys.has(link.from) && allowedNodeKeys.has(link.to) && relationFilterEnabled(link.type);
  });

  const filteredModel = { nodes: filteredNodes, links: filteredLinks };
  const depthMap = neighborhoodDepthMap(filteredModel, anchorKey);
  const depthLimit = depthLimitValue();
  let visibleNodes = filteredNodes.filter((node) => {
    const level = depthMap.get(node.key);
    if (state.mapFieldRegime === "global" && depthLimit === Number.POSITIVE_INFINITY) return true;
    if (state.mapFieldRegime === "focused" && depthLimit === Number.POSITIVE_INFINITY) return Number.isFinite(level);
    return level <= depthLimit;
  });

  let visibleNodeKeys = new Set(visibleNodes.map((node) => node.key));
  filteredLinks = filteredLinks.filter((link) => visibleNodeKeys.has(link.from) && visibleNodeKeys.has(link.to));

  if (!state.mapShowIsolated || state.mapFieldRegime === "focused") {
    visibleNodes = pruneIsolatedNodes(visibleNodes, filteredLinks, anchorKey);
    visibleNodeKeys = new Set(visibleNodes.map((node) => node.key));
    filteredLinks = filteredLinks.filter((link) => visibleNodeKeys.has(link.from) && visibleNodeKeys.has(link.to));
  }

  const visibleModel = { nodes: visibleNodes, links: filteredLinks };
  const visibleDepth = neighborhoodDepthMap(visibleModel, anchorKey);
  return {
    anchorKey,
    nodes: layoutMapNodes(visibleNodes, anchorKey, visibleDepth),
    links: filteredLinks.map((link) => ({ ...link, tone: relationTone(link.type), priority: relationPriority(link.type) })),
    depthMap: visibleDepth
  };
}

function activeMapNodeKey() {
  return state.hoveredNodeId || state.isolatedNodeId || state.focusedNodeId || currentMapAnchorKey();
}

function visibleMapNodeKeys(model) {
  return new Set(model.nodes.map((node) => node.key));
}

function fadedMapNodeKeys(model) {
  const faded = new Set();
  model.nodes.forEach((node) => {
    if ((node.depth ?? 99) >= 2) faded.add(node.key);
  });
  return faded;
}

function renderHoverProbe() {
  const probe = document.getElementById("hover-probe");
  const stage = document.getElementById("graph-stage");
  const key = state.hoveredNodeId;
  if (!probe || !stage || !key) {
    if (probe) probe.hidden = true;
    return;
  }
  const target = stage.querySelector(`[data-node-key="${CSS.escape(key)}"]`);
  if (!target) {
    probe.hidden = true;
    return;
  }
  const rect = target.getBoundingClientRect();
  const stageRect = stage.getBoundingClientRect();
  const title = target.querySelector(".graph-node-title")?.textContent || "Focused object";
  probe.hidden = false;
  probe.innerHTML = `<div class="hover-probe-title">${escapeHtml(title)}</div><div class="hover-probe-copy">${escapeHtml(target.dataset.nodeSummary || "")}</div>`;
  const left = clamp(rect.left - stageRect.left + rect.width + 12, 18, Math.max(18, stageRect.width - 280));
  const top = clamp(rect.top - stageRect.top - 8, 18, Math.max(18, stageRect.height - 120));
  probe.style.left = `${left}px`;
  probe.style.top = `${top}px`;
}

function applyMapTransform() {
  const world = document.getElementById("graph-world");
  if (!world) return;
  world.style.transform = `translate(${state.mapOffset.x}px, ${state.mapOffset.y}px) scale(${state.mapScale})`;
  renderHoverProbe();
}

function zoomMap(delta) {
  state.mapScale = clamp(Number((state.mapScale + delta).toFixed(2)), 0.76, 1.9);
  applyMapTransform();
  syncGraphAttention();
}

function resetMapView() {
  state.mapScale = 1;
  state.mapOffset = { x: 0, y: 0 };
  state.isolatedNodeId = null;
  state.hoveredNodeId = null;
  state.mapFieldRegime = "global";
  state.mapDepth = "all";
  state.mapSpread = "balanced";
  state.mapLabelDensity = "balanced";
  state.mapEntityFilters = defaultMapEntityFilters();
  state.mapRelationFilters = defaultMapRelationFilters();
  state.mapPhysics = defaultMapPhysics();
  state.mapNodeSize = 1;
  state.mapLinkThickness = 1;
  state.mapFrozen = false;
  state.mapAnimate = true;
  state.mapShowIsolated = false;
  renderMapView();
}

function toggleMapIsolation() {
  const activeKey = state.focusedNodeId || activeMapNodeKey();
  if (!activeKey) return;
  state.isolatedNodeId = state.isolatedNodeId === activeKey ? null : activeKey;
  renderMapView();
}

function labelVisibilityForNode(node, activeKey) {
  if (state.mapLabelDensity === "full") return true;
  if (state.mapLabelDensity === "balanced") {
    return node.primary || node.key === activeKey || (node.depth ?? 99) <= 1;
  }
  return node.primary || node.key === activeKey;
}

function renderMapLegend(model) {
  const totalNodes = model.nodes.length;
  const totalLinks = model.links.length;
  const activeRelations = Object.entries(state.mapRelationFilters)
    .filter(([, enabled]) => enabled)
    .map(([type]) => titleCase(type))
    .join(" • ");
  return `
    <div class="map-legend-grid">
      <div class="map-legend-row"><span>Regime</span><strong>${escapeHtml(state.mapFieldRegime === "focused" ? "Focused field" : "Global field")}</strong></div>
      <div class="map-legend-row"><span>Depth</span><strong>${escapeHtml(state.mapDepth === "all" ? "All visible topology" : `${state.mapDepth} hops`)}</strong></div>
      <div class="map-legend-row"><span>Field</span><strong>${totalNodes} nodes • ${totalLinks} relations</strong></div>
      <div class="map-legend-row"><span>Preset</span><strong>${escapeHtml(titleCase(state.mapMode))}</strong></div>
      <div class="map-legend-row"><span>Relations</span><strong>${escapeHtml(activeRelations || "None")}</strong></div>
    </div>
  `;
}

function renderMapToolbar(model, cycle) {
  return `
    <div class="graph-toolbar-header">
      <div>
        <div class="graph-toolbar-title">Field controls</div>
        <div class="graph-toolbar-copy">Shape the neighborhood without leaving the field.</div>
      </div>
      <div class="badge-row">
        <span class="badge ${statusBadgeClass(cycle.status)}">${escapeHtml(statusLabel(cycle.status))}</span>
      </div>
    </div>
    <div class="graph-control-stack">
      <div class="graph-control-row">
        <div class="graph-control-label">Regime</div>
        <div class="graph-control-group">
          <button class="graph-chip ${state.mapFieldRegime === "global" ? "active" : ""}" type="button" data-map-field="global">Global field</button>
          <button class="graph-chip ${state.mapFieldRegime === "focused" ? "active" : ""}" type="button" data-map-field="focused">Focused field</button>
        </div>
      </div>
      <div class="graph-control-row">
        <div class="graph-control-label">Depth</div>
        <div class="graph-control-group">
          ${["all", "1", "2", "3"].map((value) => `<button class="graph-chip ${state.mapDepth === value ? "active" : ""}" type="button" data-map-depth="${escapeHtml(value)}">${escapeHtml(value === "all" ? "All" : `${value} hop${value === "1" ? "" : "s"}`)}</button>`).join("")}
        </div>
      </div>
      <div class="graph-control-row">
        <div class="graph-control-label">Density</div>
        <div class="graph-control-group">
          ${["compact", "balanced", "spread"].map((value) => `<button class="graph-chip ${state.mapSpread === value ? "active" : ""}" type="button" data-map-density="${escapeHtml(value)}">${escapeHtml(titleCase(value))}</button>`).join("")}
        </div>
      </div>
      <div class="graph-control-row">
        <div class="graph-control-label">Labels</div>
        <div class="graph-control-group">
          ${["sparse", "balanced", "full"].map((value) => `<button class="graph-chip ${state.mapLabelDensity === value ? "active" : ""}" type="button" data-map-label-density="${escapeHtml(value)}">${escapeHtml(titleCase(value))}</button>`).join("")}
        </div>
      </div>
      <div class="graph-control-row">
        <div class="graph-control-label">Structure</div>
        <div class="graph-range-grid">
          <label class="graph-range compact">
            <div class="graph-range-head"><span>Node size</span><span>${escapeHtml(String(Math.round(state.mapNodeSize * 100)))}%</span></div>
            <input type="range" min="70" max="160" value="${escapeHtml(String(Math.round(state.mapNodeSize * 100)))}" data-map-node-size />
          </label>
          <label class="graph-range compact">
            <div class="graph-range-head"><span>Link thickness</span><span>${escapeHtml(String(Math.round(state.mapLinkThickness * 100)))}%</span></div>
            <input type="range" min="60" max="180" value="${escapeHtml(String(Math.round(state.mapLinkThickness * 100)))}" data-map-link-thickness />
          </label>
        </div>
      </div>
      <div class="graph-control-row">
        <div class="graph-control-label">Node filters</div>
        <div class="graph-filter-grid">
          ${Object.entries({
            cycles: "Cycles",
            activities: "Activities",
            documents: "Documents",
            risks: "Risks",
            entities: "Entities"
          }).map(([key, label]) => `<button class="graph-filter-chip ${state.mapEntityFilters[key] ? "active" : ""}" type="button" data-map-entity-filter="${escapeHtml(key)}">${escapeHtml(label)}</button>`).join("")}
        </div>
      </div>
      <div class="graph-control-row">
        <div class="graph-control-label">Relation filters</div>
        <div class="graph-filter-grid">
          ${Object.entries({
            blocks: "Blocks",
            supports: "Supports",
            requires: "Requires",
            impacts: "Impacts",
            references: "References",
            owns: "Owns"
          }).map(([key, label]) => `<button class="graph-filter-chip ${state.mapRelationFilters[key] ? "active" : ""}" type="button" data-map-relation-filter="${escapeHtml(key)}">${escapeHtml(label)}</button>`).join("")}
        </div>
      </div>
      <div class="graph-control-row">
        <div class="graph-control-group">
          <button class="graph-tool-button ${state.isolatedNodeId ? "active" : ""}" type="button" data-map-isolate>Isolate</button>
          <button class="graph-tool-button ${state.mapShowIsolated ? "active" : ""}" type="button" data-map-show-isolated>Keep isolated</button>
          <button class="graph-tool-button ${state.mapFrozen ? "active" : ""}" type="button" data-map-freeze>${state.mapFrozen ? "Resume" : "Freeze"}</button>
          <button class="graph-tool-button ${state.mapAnimate ? "active" : ""}" type="button" data-map-animate>${state.mapAnimate ? "Animate" : "Still"}</button>
          <button class="graph-tool-button" type="button" data-map-zoom="out">-</button>
          <button class="graph-tool-button" type="button" data-map-zoom="in">+</button>
          <button class="graph-tool-button" type="button" data-map-reset>Reset view</button>
        </div>
      </div>
    </div>
    <details ${state.mapControlsAdvanced ? "open" : ""} data-map-advanced>
      <summary data-map-advanced-toggle>Advanced field physics</summary>
      <div class="graph-advanced-grid">
        ${[
          ["center", "Global gravity"],
          ["repel", "Repulsion"],
          ["link", "Link tension"],
          ["focus", "Focus gravity"],
          ["distance", "Preferred distance"]
        ].map(([key, label]) => `
          <label class="graph-range">
            <div class="graph-range-head"><span>${escapeHtml(label)}</span><span>${escapeHtml(String(Math.round(state.mapPhysics[key] * 100)))}</span></div>
            <input type="range" min="0" max="100" value="${escapeHtml(String(Math.round(state.mapPhysics[key] * 100)))}" data-map-physics="${escapeHtml(key)}" />
          </label>
        `).join("")}
      </div>
    </details>
  `;
}

function syncGraphAttention() {
  const model = state.mapModel;
  const stage = document.getElementById("graph-stage");
  if (!model || !stage) return;
  const activeKey = activeMapNodeKey();
  const visibleKeys = visibleMapNodeKeys(model);
  const fadedKeys = fadedMapNodeKeys(model);
  stage.querySelectorAll(".graph-node").forEach((element) => {
    const key = element.dataset.nodeKey;
    const hidden = key && !visibleKeys.has(key);
    const node = model.nodes.find((item) => item.key === key);
    element.hidden = hidden;
    element.classList.toggle("focused", Boolean(key && activeKey && key === activeKey));
    element.classList.toggle("muted", Boolean(key && !hidden && (fadedKeys.has(key) || (activeKey && key !== activeKey && !modeHighlightsNode(node)))));
    const stateLabel = element.querySelector(".graph-node-state");
    if (stateLabel) {
      stateLabel.hidden = !labelVisibilityForNode(node || { primary: false }, activeKey);
    }
  });
  stage.querySelectorAll(".graph-link").forEach((element) => {
    const from = element.dataset.fromKey;
    const to = element.dataset.toKey;
    const type = element.dataset.relationType;
    const hidden = !visibleKeys.has(from) || !visibleKeys.has(to);
    element.hidden = hidden;
    const active = Boolean(activeKey && (from === activeKey || to === activeKey));
    const allowedByMode = modeAllowsRelation(type);
    const priority = relationPriority(type);
    element.style.opacity = hidden ? "0" : !allowedByMode ? "0.08" : priority === "primary" ? "1" : priority === "secondary" ? "0.45" : "0.2";
    element.classList.toggle("primary-tone", priority === "primary");
    element.classList.toggle("secondary", priority === "secondary");
    element.classList.toggle("contextual", priority === "contextual");
    element.classList.toggle("active", active);
    element.classList.toggle("muted", !active && !hidden && Boolean(activeKey && (!allowedByMode || fadedKeys.has(from) || fadedKeys.has(to))));
  });
  stage.querySelectorAll(".graph-link-label").forEach((element) => {
    const from = element.dataset.fromKey;
    const to = element.dataset.toKey;
    const type = element.dataset.relationType;
    const hidden = !visibleKeys.has(from) || !visibleKeys.has(to);
    element.hidden = hidden;
    const active = Boolean(activeKey && (from === activeKey || to === activeKey));
    const showByDensity = state.mapLabelDensity === "full" || (state.mapLabelDensity === "balanced" ? active || state.isolatedNodeId : active);
    element.classList.toggle("active", active);
    element.classList.toggle("visible", showByDensity && modeAllowsRelation(type));
  });
  renderHoverProbe();
}

function renderMapView() {
  const cycle = pickFocusedCycle();
  if (!cycle) {
    stopMapSimulation();
    state.mapModel = null;
    setHtml("graph-stage", '<div class="empty-state" style="margin:18px">No cycle is available yet.</div>');
    setText("map-guide-copy", "Initialize and seed the workspace to populate the field.");
    setText("map-cycle-narrative", "Cycle context will appear here once the workspace contains operational data.");
    return;
  }
  document.querySelectorAll("[data-map-mode]").forEach((button) => {
    button.classList.toggle("active", button.dataset.mapMode === state.mapMode);
  });
  const model = buildMapModel(cycle);
  state.mapModel = model;
  const summary = summarizeCycle(cycle);
  const positions = Object.fromEntries(model.nodes.map((node) => [node.key, node]));
  const activeKey = activeMapNodeKey();
  const visibleKeys = visibleMapNodeKeys(model);
  const links = model.links
    .map((link) => {
      const from = positions[link.from];
      const to = positions[link.to];
      if (!from || !to) return "";
      const active = activeKey && (link.from === activeKey || link.to === activeKey);
      const hidden = !visibleKeys.has(link.from) || !visibleKeys.has(link.to);
      const midX = (from.x + to.x) / 2;
      const midY = (from.y + to.y) / 2;
      return `
        <path
          class="graph-link ${escapeHtml(link.tone)} ${active ? "active" : activeKey ? "muted" : ""}"
          data-link-id="${escapeHtml(link.id)}"
          data-from-key="${escapeHtml(link.from)}"
          data-to-key="${escapeHtml(link.to)}"
          data-relation-type="${escapeHtml(link.type)}"
          ${hidden ? "hidden" : ""}
          d="${graphLinkPath(from, to, link.type)}"
        ></path>
        <text
          class="graph-link-label ${active ? "active" : ""}"
          data-link-id="${escapeHtml(link.id)}"
          data-from-key="${escapeHtml(link.from)}"
          data-to-key="${escapeHtml(link.to)}"
          data-relation-type="${escapeHtml(link.type)}"
          ${hidden ? "hidden" : ""}
          x="${midX}"
          y="${midY}"
          text-anchor="middle"
        >${escapeHtml(relationLabel(link.type))}</text>
      `;
    })
    .join("");
  setHtml(
    "graph-stage",
    `
      <div class="map-stage-overlay">
        <div class="map-stage-kicker">${escapeHtml(state.mapFieldRegime === "focused" ? "Focused field" : "Global field")}</div>
        <div class="map-stage-title">${escapeHtml(cycleLabel(cycle))}</div>
        <div class="map-stage-copy">${escapeHtml(cycleNarrative(cycle))}</div>
        <div class="map-stage-metrics">
          <span class="badge ${statusBadgeClass(cycle.status)}">${escapeHtml(statusLabel(cycle.status))}</span>
          <span class="badge ${statusBadgeClass(summary.pressure === "Critical" ? "blocked" : summary.pressure === "Elevated" ? "pending" : "completed")}">${escapeHtml(summary.pressure)}</span>
          <span class="badge ${statusBadgeClass(summary.evidence === "Fragile" ? "warning" : summary.evidence === "Degraded" ? "error" : "completed")}">${escapeHtml(summary.evidence)}</span>
        </div>
      </div>
      <div class="graph-viewport">
        <div id="graph-world" class="graph-world">
          <svg class="graph-svg" viewBox="0 0 100 100" preserveAspectRatio="none">${links}</svg>
          ${model.nodes.map(graphNodeMarkup).join("")}
        </div>
      </div>
      <div id="hover-probe" class="hover-probe" hidden></div>
      <div id="map-field-controls" class="graph-toolbar">${renderMapToolbar(model, cycle)}</div>
    `
  );
  setHtml("map-legend", renderMapLegend(model));
  setText("map-guide-copy", "Start with the cycle, then narrow the field through depth, filters, and focus.");
  setText("map-cycle-narrative", cycleNarrative(cycle));
  applyMapTransform();
  syncGraphAttention();
  if (state.view === "map") {
    startMapSimulation(model);
  } else {
    stopMapSimulation();
  }
}

function activityCardMarkup(activity, emphasize = false) {
  return `
    <div class="activity-card ${state.selected.type === "activity" && state.selected.id === activity.id ? "active" : ""} ${emphasize ? "flow-emphasis" : ""}">
      <button type="button" data-select-activity="${escapeHtml(activity.id)}">
        <div class="card-kicker">Activity</div>
        <div class="card-title">${escapeHtml(activity.title)}</div>
        <div class="card-secondary">${escapeHtml(activityCardSummary(activity))}</div>
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
        <div class="card-secondary">${escapeHtml(documentCardSummary(document))}</div>
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
    ["flow-attention", "flow-moving", "flow-stable", "flow-documents", "document-primary"].forEach((id) => setHtml(id, '<div class="empty-state">No focused cycle is available.</div>'));
    ["flow-attention-meta", "flow-moving-meta", "flow-stable-meta"].forEach((id) => setHtml(id, ""));
    renderMiniMapField("flow-field", null);
    return;
  }
  const activities = relatedActivities(cycle.id);
  const filter = document.getElementById("flow-status-filter")?.value || "";
  const attention = activities.filter((item) => ["pending", "blocked"].includes(item.status));
  const moving = activities.filter((item) => item.status === "in_progress");
  const stable = activities.filter((item) => item.status === "completed");
  setHtml(
    "flow-attention-meta",
    `<span class="badge warning">${attention.length} in tension</span>${attention.some((item) => item.status === "blocked") ? '<span class="badge danger">blocked work present</span>' : ""}`
  );
  setHtml(
    "flow-moving-meta",
    `<span class="badge">${moving.length} advancing</span>${moving.length ? '<span class="badge success">active momentum</span>' : ""}`
  );
  setHtml(
    "flow-stable-meta",
    `<span class="badge success">${stable.length} stabilized</span><span class="badge">${relatedDocuments(cycle.id).length} support docs</span>`
  );
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
    "document-primary",
    documents.slice(0, 1).length ? documents.slice(0, 1).map(documentCardMarkup).join("") : '<div class="empty-state">No contextual support is currently anchored.</div>'
  );
  setHtml(
    "flow-documents",
    documents.slice(1).length ? documents.slice(1).map(documentCardMarkup).join("") : '<div class="empty-state">No more support documents are linked to this cycle.</div>'
  );
  setHtml(
    "document-strip",
    documents.slice(1, 4).length ? documents.slice(1, 4).map(documentCardMarkup).join("") : '<div class="empty-state">No additional support is in focus.</div>'
  );
  renderMiniMapField("flow-field", cycle, "Flow remains a reading mode of the same field. Use the field to see what is pressing the cycle now.");
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
      ? `<div class="inspect-card detail-callout"><div class="card-kicker">Supporting document</div><div class="card-title">${escapeHtml(document.title)}</div><div class="card-secondary">${escapeHtml(documentCardSummary(document))}</div></div>`
      : '<div class="empty-state">No supporting document is linked to this activity yet.</div>';
  } else if (state.selected.type === "document") {
    const activity = supportingActivityForDocument(selection);
    primaryHtml = documentCardMarkup(selection);
    secondaryHtml = activity
      ? `<div class="inspect-card detail-callout"><div class="card-kicker">Operational anchor</div><div class="card-title">${escapeHtml(activity.title)}</div><div class="card-secondary">${escapeHtml(activityCardSummary(activity))}</div></div>`
      : '<div class="empty-state">No single activity is currently anchored by this document.</div>';
  } else {
    primaryHtml = `<div class="inspect-card detail-callout"><div class="card-kicker">Focused cycle</div><div class="card-title">${escapeHtml(cycleLabel(selection))}</div><div class="card-secondary">${escapeHtml(cycleNarrative(selection))}</div></div>`;
    const firstActivity = relatedActivities(selection.id)[0];
    secondaryHtml = firstActivity
      ? `<div class="inspect-card detail-callout"><div class="card-kicker">Next activity</div><div class="card-title">${escapeHtml(firstActivity.title)}</div><div class="card-secondary">${escapeHtml(activityCardSummary(firstActivity))}</div></div>`
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
      `
        <div class="inspect-surface">
          <div class="inspect-reading-surface">${escapeHtml(activityNarrative(selection))}</div>
          ${renderMetaGrid([
            ["Activity", selection.title],
            ["Cycle", cycleLabel(cycleById(selection.cycle_id))],
            ["State", statusLabel(selection.status)],
            ["Priority", selection.priority <= 2 ? "High" : selection.priority >= 4 ? "Low" : "Normal"],
            ["Created", formatDateTime(selection.created_at)]
          ])}
        </div>
      `
    );
    return;
  }
  if (state.selected.type === "document") {
    const integrity = integrityFor(selection.id);
    setHtml(
      "inspect-context",
      `
        <div class="inspect-surface">
          <div class="inspect-reading-surface">${escapeHtml(documentNarrative(selection))}</div>
          ${renderMetaGrid([
            ["Document", selection.title],
            ["Type", documentTypeLabel(selection.type)],
            ["Lifecycle", statusLabel(selection.status)],
            ["Cycle", selection.cycle_id ? cycleLabel(cycleById(selection.cycle_id)) : "General support material"],
            ["Integrity", integrity ? statusLabel(integrity.integrity_state) : "Unknown"]
          ])}
        </div>
      `
    );
    return;
  }
  const summary = summarizeCycle(selection);
  setHtml(
    "inspect-context",
    `
      <div class="inspect-surface">
        <div class="inspect-reading-surface">${escapeHtml(cycleNarrative(selection))}</div>
        ${renderMetaGrid([
          ["Cycle", cycleLabel(selection)],
          ["State", statusLabel(selection.status)],
          ["Activities", String(selection.activity_count)],
          ["Supporting documents", String(summary.documents.length)],
          ["Pressure", summary.pressure],
          ["Risk", summary.risk]
        ])}
      </div>
    `
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
        <div class="inspect-surface">
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
        </div>
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
        <div class="inspect-surface">
          <div class="detail-callout flow-emphasis">
            <div class="card-kicker">Supporting evidence</div>
            <div class="card-title">${escapeHtml(document.title)}</div>
            <div class="card-secondary">${escapeHtml(documentCardSummary(document))}</div>
          </div>
          <div class="${details?.error ? "preview error" : "preview"}">${escapeHtml(details?.content_preview || details?.error || "(empty document)")}</div>
        </div>
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
        <div class="inspect-surface">
          <div class="detail-callout">
            <div class="card-kicker">Controlled status transition</div>
            <div class="card-secondary">Operational state changes remain explicit, traceable, and immediately visible.</div>
            <div class="action-row">${activityStatusControls(selection)}</div>
          </div>
          ${relatedAudit.map(renderAuditSnippet).join("") || '<div class="empty-state">No audit memory yet for this activity.</div>'}
        </div>
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
        <div class="inspect-surface">
          <div class="detail-callout">
            <div class="card-kicker">Lifecycle and reconciliation</div>
            <div class="card-secondary">Keep the document legitimate before you let it carry operational consequence.</div>
            <div class="action-row">${documentStatusControls(selection)}
              <button class="inline-button ${canReconcile(integrity) ? "primary" : ""}" type="button" data-reconcile-document="${escapeHtml(selection.id)}" ${canReconcile(integrity) && !state.pendingMutation ? "" : "disabled"}>Reconcile metadata</button>
            </div>
          </div>
          ${relatedAudit.map(renderAuditSnippet).join("") || '<div class="empty-state">No audit memory yet for this document.</div>'}
        </div>
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
      <div class="inspect-surface">
        <div class="detail-callout">
          <div class="card-kicker">Cycle governance</div>
          <div class="card-secondary">Judge whether the cycle still has enough evidence, legitimacy, and room to move safely.</div>
        </div>
        ${relatedAudit.map(renderAuditSnippet).join("") || '<div class="empty-state">No audit memory yet for this cycle.</div>'}
      </div>
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
        <div>
          <div class="audit-title">${escapeHtml(auditObjectLabel(entry))}</div>
          <div class="audit-subtitle">${escapeHtml(auditContextLabel(entry))}</div>
        </div>
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
    renderMiniMapField("inspect-field", null);
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
  renderMiniMapField("inspect-field", pickFocusedCycle(), "Inspect stays anchored in the same field so judgment never detaches from context.");
}

function renderAuditView() {
  if (!state.audit.length) {
    setHtml("audit-timeline", '<div class="empty-state">Audit memory will appear here once the workspace records events.</div>');
    setHtml("audit-snapshot", '<div class="empty-state">No recent audit activity.</div>');
    renderMiniMapField("audit-field", null);
    return;
  }
  const focusedCycleId = state.focusedCycleId;
  const narrowed = focusedCycleId
    ? state.audit.filter((entry) => cycleIdForAuditEntry(entry) === focusedCycleId)
    : state.audit;
  const entries = narrowed.length >= 4 ? narrowed : state.audit;
  const groups = groupAuditEntries(entries);
  setHtml(
    "audit-timeline",
    groups
      .map(
        ({ spec, entries }) => `
          <section class="surface audit-group">
            <div class="audit-group-title">${escapeHtml(spec.title)}</div>
            <div class="audit-group-copy">${escapeHtml(spec.copy)}</div>
            ${entries
              .map(
                (entry) => `
                  <article class="audit-entry">
                    <div class="audit-head">
                      <div>
                        <div class="audit-title">${escapeHtml(auditObjectLabel(entry))}</div>
                        <div class="audit-subtitle">${escapeHtml(auditContextLabel(entry))}</div>
                      </div>
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
    entries.slice(0, 4).map(renderAuditSnippet).join("")
  );
  renderMiniMapField("audit-field", pickFocusedCycle(), "Audit remains tied to the same field. Read memory as consequence, then jump back into MAP.");
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
  state.focusedNodeId = state.selected.id ? nodeKey(state.selected.type, state.selected.id) : null;
  await renderEverything();
  setReadiness(
    "Workspace ready",
    "The institutional map, operational flow, judgment surface, and audit memory are fully loaded.",
    "ready",
    true
  );
}

function renderEmptyWorkspace() {
  setHtml("overview-grid", '<div class="empty-state">Workspace not initialized.</div>');
  ["overview-field", "flow-field", "inspect-field", "audit-field"].forEach((id) => setHtml(id, '<div class="empty-state">Workspace not initialized.</div>'));
  setHtml("cycle-index", '<li class="empty-state">No cycles are available.</li>');
  setHtml("ontology-list", '<div class="empty-state">No local structural context yet.</div>');
  setHtml("workspace-pulse", '<div class="empty-state">Workspace pulse will appear after initialization.</div>');
  setHtml("graph-stage", '<div class="empty-state" style="margin:18px">Workspace not initialized.</div>');
  setHtml("flow-attention", '<div class="empty-state">Workspace not initialized.</div>');
  setHtml("flow-moving", '<div class="empty-state">Workspace not initialized.</div>');
  setHtml("flow-stable", '<div class="empty-state">Workspace not initialized.</div>');
  setHtml("flow-documents", '<div class="empty-state">Workspace not initialized.</div>');
  setHtml("document-primary", '<div class="empty-state">Workspace not initialized.</div>');
  setHtml("document-strip", '<div class="empty-state">Workspace not initialized.</div>');
  setHtml("audit-timeline", '<div class="empty-state">Workspace not initialized.</div>');
  setHtml("audit-snapshot", '<div class="empty-state">Workspace not initialized.</div>');
  setHtml("selected-primary", '<div class="empty-state">Workspace not initialized.</div>');
  setHtml("selected-secondary", "");
  setText("operator-guidance", "Initialize the workspace before using the cockpit.");
}

async function renderEverything() {
  renderOverviewView();
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
    const viewButton = event.target.closest("[data-view]");
    if (viewButton && !viewButton.closest("#main-nav")) {
      activateView(viewButton.dataset.view);
      return;
    }
    const cycleButton = event.target.closest("[data-select-cycle]");
    if (cycleButton) {
      state.mapFieldRegime = "global";
      state.focusedNodeId = nodeKey("cycle", cycleButton.dataset.selectCycle);
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
      state.mapFieldRegime = "focused";
      state.focusedNodeId = nodeKey(type, id);
      if (type === "cycle" || type === "activity" || type === "document") {
        state.selected = { type: type === "cycle" ? "cycle" : type, id };
        if (type === "cycle") {
          state.focusedCycleId = id;
        }
      }
      void renderEverything();
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
    const miniMapJump = event.target.closest("[data-mini-map-jump]");
    if (miniMapJump) {
      const [type, id] = miniMapJump.dataset.miniMapJump.split(":");
      if (type !== "entity" && type !== "risk") {
        selectObject(type === "cycle" ? "cycle" : type, id);
      }
      activateView("map");
      return;
    }
    const modeButton = event.target.closest("[data-map-mode]");
    if (modeButton) {
      state.mapMode = modeButton.dataset.mapMode;
      renderMapView();
      return;
    }
    const fieldButton = event.target.closest("[data-map-field]");
    if (fieldButton) {
      state.mapFieldRegime = fieldButton.dataset.mapField;
      renderMapView();
      revealRails();
      return;
    }
    const depthButton = event.target.closest("[data-map-depth]");
    if (depthButton) {
      state.mapDepth = depthButton.dataset.mapDepth;
      renderMapView();
      revealRails();
      return;
    }
    const densityButton = event.target.closest("[data-map-density]");
    if (densityButton) {
      state.mapSpread = densityButton.dataset.mapDensity;
      renderMapView();
      revealRails();
      return;
    }
    const labelButton = event.target.closest("[data-map-label-density]");
    if (labelButton) {
      state.mapLabelDensity = labelButton.dataset.mapLabelDensity;
      syncGraphAttention();
      revealRails();
      return;
    }
    const entityFilterButton = event.target.closest("[data-map-entity-filter]");
    if (entityFilterButton) {
      const key = entityFilterButton.dataset.mapEntityFilter;
      state.mapEntityFilters[key] = !state.mapEntityFilters[key];
      renderMapView();
      revealRails();
      return;
    }
    const relationFilterButton = event.target.closest("[data-map-relation-filter]");
    if (relationFilterButton) {
      const key = relationFilterButton.dataset.mapRelationFilter;
      state.mapRelationFilters[key] = !state.mapRelationFilters[key];
      renderMapView();
      revealRails();
      return;
    }
    const showIsolatedButton = event.target.closest("[data-map-show-isolated]");
    if (showIsolatedButton) {
      state.mapShowIsolated = !state.mapShowIsolated;
      renderMapView();
      revealRails();
      return;
    }
    const advancedToggle = event.target.closest("[data-map-advanced-toggle]");
    if (advancedToggle) {
      state.mapControlsAdvanced = !state.mapControlsAdvanced;
      renderMapView();
      revealRails();
      return;
    }
    const zoomButton = event.target.closest("[data-map-zoom]");
    if (zoomButton) {
      zoomMap(zoomButton.dataset.mapZoom === "in" ? 0.14 : -0.14);
      revealRails();
      return;
    }
    const isolateButton = event.target.closest("[data-map-isolate]");
    if (isolateButton) {
      toggleMapIsolation();
      revealRails();
      return;
    }
    const freezeButton = event.target.closest("[data-map-freeze]");
    if (freezeButton) {
      state.mapFrozen = !state.mapFrozen;
      renderMapView();
      revealRails();
      return;
    }
    const animateButton = event.target.closest("[data-map-animate]");
    if (animateButton) {
      state.mapAnimate = !state.mapAnimate;
      renderMapView();
      revealRails();
      return;
    }
    const resetButton = event.target.closest("[data-map-reset]");
    if (resetButton) {
      resetMapView();
      revealRails();
    }
  });

  document.addEventListener("mouseover", (event) => {
    const node = event.target.closest(".graph-node");
    if (!node) return;
    if (event.relatedTarget && node.contains(event.relatedTarget)) return;
    state.hoveredNodeId = node.dataset.nodeKey || null;
    syncGraphAttention();
    revealRails();
  });

  document.addEventListener("mouseout", (event) => {
    const node = event.target.closest(".graph-node");
    if (!node) return;
    if (event.relatedTarget && node.contains(event.relatedTarget)) return;
    state.hoveredNodeId = null;
    syncGraphAttention();
  });

  document.addEventListener("mousemove", (event) => {
    if (!state.dragState) return;
    state.mapOffset = {
      x: state.dragState.originOffset.x + (event.clientX - state.dragState.startX),
      y: state.dragState.originOffset.y + (event.clientY - state.dragState.startY)
    };
    applyMapTransform();
    revealRails();
  });

  document.addEventListener("input", (event) => {
    const nodeSize = event.target.closest("[data-map-node-size]");
    if (nodeSize) {
      state.mapNodeSize = Number(nodeSize.value) / 100;
      applyMapVisualTuning();
      renderMapView();
      revealRails();
      return;
    }
    const linkThickness = event.target.closest("[data-map-link-thickness]");
    if (linkThickness) {
      state.mapLinkThickness = Number(linkThickness.value) / 100;
      applyMapVisualTuning();
      renderMapView();
      revealRails();
      return;
    }
    const range = event.target.closest("[data-map-physics]");
    if (!range) return;
    const key = range.dataset.mapPhysics;
    state.mapPhysics[key] = Number(range.value) / 100;
    renderMapView();
    revealRails();
  });

  document.addEventListener("mouseup", () => {
    state.dragState = null;
  });

  document.getElementById("graph-stage")?.addEventListener("wheel", (event) => {
    event.preventDefault();
    zoomMap(event.deltaY < 0 ? 0.08 : -0.08);
    revealRails();
  }, { passive: false });

  document.getElementById("graph-stage")?.addEventListener("mousedown", (event) => {
    if (event.target.closest(".graph-node, .graph-toolbar, .map-stage-overlay, .hover-probe")) {
      return;
    }
    state.dragState = {
      startX: event.clientX,
      startY: event.clientY,
      originOffset: { ...state.mapOffset }
    };
    revealRails();
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
