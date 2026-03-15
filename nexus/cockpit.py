from __future__ import annotations


def render_cockpit_page() -> str:
    return """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Nexus Cockpit</title>
    <style>
      :root {
        color-scheme: dark;
        --page: #0d1117;
        --page-accent: #121a24;
        --panel: #141b23;
        --panel-soft: #10161d;
        --panel-muted: #18212b;
        --panel-elevated: #1b2632;
        --border: #263241;
        --border-soft: #1f2935;
        --text: #e8eef5;
        --text-soft: #c4d0dc;
        --muted: #8c9bab;
        --accent: #7ca6ff;
        --accent-soft: rgba(124, 166, 255, 0.14);
        --accent-strong: #cfe0ff;
        --success-soft: rgba(63, 185, 80, 0.16);
        --warning-soft: rgba(210, 153, 34, 0.16);
        --danger-soft: rgba(248, 81, 73, 0.16);
        --danger: #ff8f87;
      }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        font-family: "Aptos", "Segoe UI", system-ui, sans-serif;
        color: var(--text);
        background:
          radial-gradient(circle at top left, rgba(124, 166, 255, 0.12), transparent 24%),
          radial-gradient(circle at top right, rgba(90, 144, 255, 0.06), transparent 20%),
          linear-gradient(180deg, #0c1116 0%, #111821 100%);
      }
      main {
        max-width: 1320px;
        margin: 0 auto;
        padding: 24px;
      }
      h1, h2, h3, h4, p { margin: 0; }
      h4 {
        font-size: 0.95rem;
        color: var(--muted);
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
      }
      .hero {
        display: flex;
        justify-content: space-between;
        gap: 16px;
        align-items: end;
        margin-bottom: 20px;
      }
      .subtitle {
        color: var(--muted);
        margin-top: 8px;
        max-width: 720px;
        line-height: 1.5;
      }
      .panel {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 18px;
        box-shadow: 0 14px 36px rgba(2, 8, 20, 0.34);
      }
      .grid {
        display: grid;
        gap: 16px;
      }
      .stats-grid {
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        margin-bottom: 20px;
      }
      .stat-card {
        background: linear-gradient(180deg, rgba(124, 166, 255, 0.12) 0%, rgba(20, 27, 35, 0.96) 100%);
        border: 1px solid rgba(124, 166, 255, 0.22);
        border-radius: 16px;
        padding: 14px;
      }
      .stat-card strong {
        display: block;
        margin-top: 8px;
        font-size: 1.75rem;
        color: var(--accent-strong);
      }
      .status-strip {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        color: var(--muted);
        font-size: 0.95rem;
        margin-top: 12px;
      }
      .readiness-panel {
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-bottom: 20px;
      }
      .readiness-panel strong {
        font-size: 1.02rem;
      }
      .readiness-panel.loading {
        border-color: rgba(124, 166, 255, 0.28);
        background: linear-gradient(180deg, rgba(124, 166, 255, 0.1) 0%, rgba(18, 26, 36, 0.96) 100%);
      }
      .readiness-panel.ready {
        border-color: rgba(63, 185, 80, 0.28);
        background: linear-gradient(180deg, rgba(63, 185, 80, 0.08) 0%, rgba(18, 26, 36, 0.96) 100%);
      }
      .readiness-panel.warning {
        border-color: rgba(210, 153, 34, 0.3);
        background: linear-gradient(180deg, rgba(210, 153, 34, 0.08) 0%, rgba(18, 26, 36, 0.96) 100%);
      }
      .readiness-panel.error {
        border-color: rgba(248, 81, 73, 0.3);
        background: linear-gradient(180deg, rgba(248, 81, 73, 0.08) 0%, rgba(18, 26, 36, 0.96) 100%);
      }
      .overview-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
        margin-bottom: 20px;
      }
      .cockpit-flow {
        grid-template-columns: minmax(280px, 0.95fr) minmax(360px, 1.15fr) minmax(360px, 1fr);
        align-items: start;
      }
      .secondary-grid {
        grid-template-columns: minmax(0, 1.1fr) minmax(0, 0.9fr);
        margin-top: 20px;
        align-items: start;
      }
      .stack {
        display: grid;
        gap: 16px;
      }
      .tab-button,
      .inline-button {
        appearance: none;
        border: 1px solid var(--border);
        background: var(--panel-muted);
        color: var(--muted);
        border-radius: 999px;
        padding: 8px 14px;
        font: inherit;
        cursor: pointer;
      }
      .tab-button.active,
      .inline-button.primary {
        color: var(--accent-strong);
        background: var(--accent-soft);
        border-color: rgba(124, 166, 255, 0.32);
      }
      .inline-button {
        padding: 7px 12px;
      }
      .toolbar {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 12px;
      }
      .toolbar input,
      .toolbar select {
        appearance: none;
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 10px 12px;
        background: var(--panel-soft);
        color: var(--text);
        font: inherit;
        min-width: 150px;
      }
      .focus-banner {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
        margin-top: 14px;
        padding: 14px;
        border-radius: 14px;
        background: linear-gradient(90deg, rgba(124, 166, 255, 0.12) 0%, rgba(20, 27, 35, 0.96) 100%);
        border: 1px solid rgba(124, 166, 255, 0.22);
      }
      .focus-banner strong {
        display: block;
        margin-bottom: 4px;
      }
      .view {
        margin-top: 16px;
      }
      .view.active {
        display: block;
      }
      .resource-list,
      .detail-list {
        list-style: none;
        padding: 0;
        margin: 14px 0 0;
        display: grid;
        gap: 10px;
      }
      .resource-item {
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 12px;
        background: var(--panel-muted);
      }
      .resource-item.selected {
        border-color: rgba(124, 166, 255, 0.34);
        background: linear-gradient(180deg, rgba(124, 166, 255, 0.16) 0%, rgba(27, 38, 50, 0.94) 100%);
      }
      .selected {
        border-color: rgba(124, 166, 255, 0.34) !important;
        background: linear-gradient(180deg, rgba(124, 166, 255, 0.16) 0%, rgba(27, 38, 50, 0.94) 100%) !important;
      }
      .resource-item button {
        appearance: none;
        border: 0;
        background: none;
        color: inherit;
        width: 100%;
        text-align: left;
        padding: 0;
        cursor: pointer;
      }
      .resource-item button:hover .resource-title {
        color: var(--accent);
      }
      .resource-title {
        font-weight: 600;
        margin-bottom: 4px;
      }
      .resource-subtle {
        color: var(--muted);
        font-size: 0.82rem;
        margin-top: 8px;
      }
      .resource-meta,
      .label {
        color: var(--muted);
        font-size: 0.92rem;
      }
      .selection-panel {
        background: linear-gradient(180deg, rgba(21, 29, 38, 0.98) 0%, rgba(16, 22, 29, 0.98) 100%);
      }
      .section-copy {
        margin-top: 6px;
        color: var(--muted);
        line-height: 1.45;
      }
      .selection-summary {
        margin-top: 10px;
        color: var(--text-soft);
        line-height: 1.55;
      }
      .detail-card {
        margin-top: 14px;
        padding: 14px;
        border: 1px solid var(--border);
        border-radius: 14px;
        background: var(--panel-muted);
        transition: border-color 120ms ease, background 120ms ease, opacity 120ms ease;
      }
      .detail-card.primary-focus {
        border-color: rgba(124, 166, 255, 0.34);
        background: linear-gradient(180deg, rgba(124, 166, 255, 0.12) 0%, rgba(24, 33, 43, 0.98) 100%);
        box-shadow: 0 16px 34px rgba(3, 10, 20, 0.24);
      }
      .detail-card.secondary-focus {
        opacity: 0.86;
        background: linear-gradient(180deg, rgba(24, 33, 43, 0.82) 0%, rgba(17, 24, 31, 0.92) 100%);
      }
      .detail-role {
        color: var(--muted);
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 10px;
      }
      .narrative-block {
        margin-top: 12px;
        padding: 14px;
        border-radius: 14px;
        border: 1px solid var(--border-soft);
        background: rgba(9, 14, 20, 0.34);
        color: var(--text-soft);
        line-height: 1.6;
      }
      .detail-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 10px;
        margin-top: 14px;
      }
      .detail-grid div {
        border: 1px solid var(--border-soft);
        border-radius: 12px;
        padding: 10px;
        background: rgba(10, 16, 23, 0.55);
      }
      .detail-grid strong {
        display: block;
        margin-top: 4px;
        color: var(--text);
      }
      .detail-section {
        margin-top: 14px;
      }
      .detail-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 12px;
      }
      .detail-actions button[disabled] {
        opacity: 0.55;
        cursor: default;
      }
      .detail-preview {
        margin-top: 14px;
        padding: 14px;
        border-radius: 14px;
        border: 1px solid var(--border);
        background: rgba(7, 11, 16, 0.82);
        color: #d6e1ed;
        white-space: pre-wrap;
        font-family: "Cascadia Code", Consolas, monospace;
        font-size: 0.9rem;
        line-height: 1.55;
        min-height: 300px;
      }
      .detail-preview.error-state {
        background: var(--danger-soft);
        color: var(--danger);
        font-family: inherit;
      }
      .document-header {
        border: 1px solid var(--border-soft);
        border-radius: 14px;
        padding: 14px;
        background: rgba(10, 16, 23, 0.55);
      }
      .document-header strong {
        display: block;
        font-size: 1.08rem;
      }
      .document-path {
        margin-top: 6px;
        color: var(--muted);
        font-size: 0.92rem;
        word-break: break-word;
      }
      .status-group-list {
        list-style: none;
        padding: 0;
        margin: 14px 0 0;
        display: grid;
        gap: 12px;
      }
      .status-group-card {
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 12px;
        background: rgba(10, 16, 23, 0.52);
      }
      .status-group-card h4 {
        margin-bottom: 10px;
      }
      .status-group-items {
        list-style: none;
        margin: 0;
        padding: 0;
        display: grid;
        gap: 8px;
      }
      .status-group-items li {
        border: 1px solid var(--border);
        border-radius: 12px;
        background: var(--panel-muted);
        padding: 10px;
      }
      .status-group-items button {
        appearance: none;
        border: 0;
        background: none;
        color: inherit;
        width: 100%;
        text-align: left;
        padding: 0;
        cursor: pointer;
      }
      .audit-panel {
        padding: 0;
        overflow: hidden;
      }
      .audit-panel summary {
        list-style: none;
        cursor: pointer;
        padding: 18px;
        font-weight: 600;
      }
      .audit-panel summary::-webkit-details-marker {
        display: none;
      }
      .audit-panel .audit-body {
        padding: 0 18px 18px;
      }
      .audit-entry {
        display: grid;
        gap: 8px;
      }
      .audit-entry-header {
        display: flex;
        justify-content: space-between;
        gap: 10px;
        align-items: start;
      }
      .audit-title {
        font-weight: 600;
        color: var(--text-soft);
      }
      .audit-time {
        color: var(--muted);
        font-size: 0.84rem;
        white-space: nowrap;
      }
      .audit-reason {
        color: var(--text-soft);
        line-height: 1.45;
      }
      .compact-badges {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 12px;
      }
      .badge {
        border-radius: 999px;
        padding: 6px 10px;
        font-size: 0.88rem;
        background: var(--accent-soft);
        color: var(--accent-strong);
      }
      .badge.success {
        background: var(--success-soft);
        color: #9dd7ac;
      }
      .badge.warning {
        background: var(--warning-soft);
        color: #f1c56d;
      }
      .badge.danger {
        background: var(--danger-soft);
        color: var(--danger);
      }
      .quiet-details {
        margin-top: 12px;
        border: 1px solid var(--border-soft);
        border-radius: 12px;
        background: rgba(9, 14, 20, 0.24);
      }
      .quiet-details summary {
        cursor: pointer;
        padding: 10px 12px;
        color: var(--muted);
        font-size: 0.9rem;
        list-style: none;
      }
      .quiet-details summary::-webkit-details-marker {
        display: none;
      }
      .technical-list {
        display: grid;
        gap: 8px;
        padding: 0 12px 12px;
      }
      .technical-row {
        display: grid;
        gap: 4px;
      }
      .technical-label {
        color: var(--muted);
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
      }
      .technical-value {
        color: var(--text-soft);
        font-size: 0.88rem;
        word-break: break-word;
      }
      .inline-note {
        margin-top: 10px;
        color: var(--muted);
        font-size: 0.92rem;
      }
      .error {
        color: var(--danger);
      }
      .empty {
        color: var(--muted);
        border: 1px dashed var(--border);
        border-radius: 12px;
        padding: 14px;
        margin-top: 14px;
        background: rgba(10, 16, 23, 0.45);
      }
      [hidden] { display: none !important; }
      @media (max-width: 960px) {
        .hero { align-items: start; flex-direction: column; }
        .overview-grid,
        .cockpit-flow,
        .secondary-grid { grid-template-columns: 1fr; }
        .detail-grid { grid-template-columns: 1fr; }
        .focus-banner { flex-direction: column; align-items: start; }
      }
    </style>
  </head>
  <body>
    <main>
      <section class="hero">
        <div>
          <h1>Nexus Cockpit</h1>
          <p class="subtitle">
            A calm supervision surface for reading active cycles, the work moving inside them, and the supporting documents that deserve trust checks.
          </p>
        </div>
        <div id="workspace-badge" class="panel" aria-live="polite">Checking workspace...</div>
      </section>

      <section id="page-readiness" class="panel readiness-panel loading" aria-live="polite">
        <strong id="page-readiness-title">Preparing cockpit...</strong>
        <div class="inline-note" id="page-readiness-detail">
          Loading workspace status and local operational surfaces.
        </div>
      </section>

      <div id="cockpit-surfaces" hidden>
      <section class="grid overview-grid">
        <article class="panel">
          <h2>Workspace</h2>
          <div class="status-strip" id="workspace-summary"></div>
          <div class="inline-note" id="workspace-notes"></div>
          <details class="quiet-details" id="workspace-technical">
            <summary>Technical workspace details</summary>
            <div class="technical-list" id="workspace-technical-list"></div>
          </details>
        </article>

        <article class="panel">
          <h2>Operational Focus</h2>
          <p class="section-copy">Cycles organize operational work, activities, and supporting documents.</p>
          <div class="status-strip" id="operations-summary"></div>
          <div class="focus-banner" id="cycle-focus-banner">
            <div>
              <strong>Cycle focus not set</strong>
              <div class="resource-meta" id="cycle-focus-meta">
                Select a cycle to drive the activity and document inspection surface.
              </div>
            </div>
            <button class="inline-button" id="clear-cycle-focus" type="button" hidden>Clear focus</button>
          </div>
        </article>
      </section>

      <section class="grid stats-grid" id="summary-grid" aria-live="polite">
        <article class="stat-card"><span class="label">Entities</span><strong id="count-entities">-</strong></article>
        <article class="stat-card"><span class="label">Documents</span><strong id="count-documents">-</strong></article>
        <article class="stat-card"><span class="label">Relations</span><strong id="count-relations">-</strong></article>
        <article class="stat-card"><span class="label">Cycles</span><strong id="count-cycles">-</strong></article>
        <article class="stat-card"><span class="label">Activities</span><strong id="count-activities">-</strong></article>
      </section>

      <section class="grid cockpit-flow">
        <article class="panel">
          <h2>Current Work Cycles</h2>
          <p class="section-copy">
            Start here. Pick the cycle that frames the current operational work, then inspect its activities and supporting documents.
          </p>
          <section class="view active" id="cycles-view">
            <div class="toolbar">
              <input id="cycles-filter" type="search" placeholder="Filter by cycle window or role" />
              <select id="cycles-status-filter">
                <option value="">All statuses</option>
                <option value="active">Active</option>
                <option value="completed">Completed</option>
                <option value="archived">Archived</option>
              </select>
            </div>
            <ul class="resource-list" id="cycles-list">
              <li class="resource-meta">Loading cycles...</li>
            </ul>
          </section>

          <section class="detail-card" id="cycle-detail">
            <h3>Cycle Overview</h3>
            <div class="empty" id="cycle-empty">No cycle selected.</div>
            <div id="cycle-content" hidden>
              <div class="narrative-block" id="cycle-story"></div>
              <div class="detail-grid" id="cycle-meta-grid"></div>
              <div class="compact-badges" id="cycle-breakdown"></div>
              <div class="detail-section">
                <h4>Activities in This Cycle</h4>
                <ul class="resource-list" id="cycle-activities"></ul>
              </div>
              <div class="detail-section">
                <h4>Supporting Documents</h4>
                <ul class="resource-list" id="cycle-documents"></ul>
              </div>
              <div id="cycle-technical"></div>
            </div>
          </section>
        </article>

        <article class="panel">
          <h2>Cycle to Activity Flow</h2>
          <p class="section-copy" id="activity-panel-hint">
            Focus a cycle to see the activities that need attention and the documents that support them.
          </p>

          <section class="view" id="activities-view">
            <h3>Activities in Selected Cycle</h3>
            <div class="toolbar">
              <input id="activities-filter" type="search" placeholder="Filter by title or cycle" />
              <select id="activities-cycle-filter">
                <option value="">All cycles</option>
              </select>
              <select id="activities-status-filter">
                <option value="">All statuses</option>
                <option value="pending">Pending</option>
                <option value="in_progress">In progress</option>
                <option value="completed">Completed</option>
                <option value="blocked">Blocked</option>
              </select>
            </div>
            <div class="compact-badges" id="activities-breakdown"></div>
            <ul class="status-group-list" id="activities-list">
              <li class="resource-meta">Loading activities...</li>
            </ul>
          </section>

          <section class="view" id="documents-view">
            <h3>Supporting Documents</h3>
            <p class="section-copy" id="documents-panel-hint">
              Documents stay visually secondary here so the work path remains cycle first, then activity, then supporting material.
            </p>
            <div class="toolbar">
              <input id="documents-filter" type="search" placeholder="Filter by title or path" />
              <select id="documents-cycle-filter">
                <option value="">All cycles</option>
              </select>
              <select id="documents-status-filter">
                <option value="">All statuses</option>
                <option value="draft">Draft</option>
                <option value="approved">Approved</option>
                <option value="archived">Archived</option>
              </select>
            </div>
            <ul class="resource-list" id="documents-list">
              <li class="resource-meta">Loading documents...</li>
            </ul>
          </section>
        </article>

        <aside class="stack">
          <article class="panel selection-panel">
            <h2>Selected Detail</h2>
            <div class="selection-summary" id="selection-summary">
              Activity focus stays primary until you open a supporting document for deeper reading.
            </div>
            <p class="inline-note" id="selection-hint">
              Inspect the selected activity first. Open a document when you need the narrative or lifecycle context behind the work.
            </p>

            <section class="detail-card" id="activity-detail">
              <div class="detail-role" id="activity-role">Primary focus</div>
              <h3>Selected Activity</h3>
              <div class="empty" id="activity-empty">No activity selected.</div>
              <div id="activity-content" hidden>
                <div class="narrative-block" id="activity-summary"></div>
                <div class="detail-grid" id="activity-meta-grid"></div>
                <div class="compact-badges" id="activity-flags"></div>
                <div class="detail-actions" id="activity-status-controls"></div>
                <div class="detail-actions" id="activity-actions"></div>
                <div class="inline-note" id="activity-status-feedback"></div>
                <div id="activity-technical"></div>
              </div>
            </section>

            <section class="detail-card" id="document-detail">
              <div class="detail-role" id="document-role">Supporting document</div>
              <h3>Selected Document</h3>
              <div class="empty" id="document-empty">No document selected.</div>
              <div id="document-content" hidden>
                <div class="document-header" id="document-header"></div>
                <div class="compact-badges" id="document-flags"></div>
                <div class="detail-grid" id="document-meta-grid"></div>
                <div class="detail-actions" id="document-status-controls"></div>
                <div class="detail-actions" id="document-actions"></div>
                <div class="inline-note" id="document-status-feedback"></div>
                <div id="document-technical"></div>
                <div class="detail-section">
                  <h4>Content Preview</h4>
                  <div class="detail-preview" id="document-preview"></div>
                </div>
              </div>
            </section>
          </article>
        </aside>
      </section>

      <section class="grid secondary-grid">
        <article class="panel">
          <h2>Reference Entities</h2>
          <p class="section-copy">Entities remain available as context, but they should not compete with the active cycle flow on the main surface.</p>
          <section class="view" id="entities-view">
            <div class="toolbar">
              <input id="entities-filter" type="search" placeholder="Filter by name, type, or context" />
            </div>
            <ul class="resource-list" id="entities-list">
              <li class="resource-meta">Loading entities...</li>
            </ul>
          </section>
        </article>

        <details class="panel audit-panel" id="audit-panel">
          <summary>Recent Audit Trace</summary>
          <div class="audit-body">
            <p class="inline-note">
              Auditability stays available for supervision, but this panel is tuned for quiet reading rather than raw operational noise.
            </p>
            <ul class="resource-list" id="audit-log-list">
              <li class="resource-meta">Loading audit trail...</li>
            </ul>
          </div>
        </details>
      </section>
      </div>
    </main>

    <script>
      const api = {
        status: "/api/system/status",
        auditLog: "/api/audit-log",
        entities: "/api/entities",
        documents: "/api/documents",
        documentIntegrity: "/api/document-integrity",
        documentReconcile: "/api/documents",
        cycles: "/api/cycles",
        activities: "/api/activities"
      };

      const state = {
        status: null,
        entities: [],
        documents: [],
        documentIntegrity: {},
        auditLog: [],
        cycles: [],
        activities: [],
        activeView: "cycles-view",
        focusedCycleId: null,
        selectedDocumentId: null,
        selectedCycleId: null,
        selectedActivityId: null,
        detailFocus: "activity",
        pendingActivityMutation: null,
        pendingDocumentMutation: null,
        pendingReconcileDocumentId: null
      };

      async function fetchJson(url) {
        const response = await fetch(url, { headers: { "Accept": "application/json" } });
        const payload = await response.json();
        if (!response.ok || payload.status !== "ok") {
          throw new Error(payload.message || "Unexpected API error");
        }
        return payload.data;
      }

      async function patchJson(url, payload) {
        const response = await fetch(url, {
          method: "PATCH",
          headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
          },
          body: JSON.stringify(payload)
        });
        const data = await response.json();
        if (!response.ok || data.status !== "ok") {
          throw new Error(data.message || "Unexpected API error");
        }
        return data.data;
      }

      async function postJson(url) {
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Accept": "application/json"
          }
        });
        const data = await response.json();
        if (!response.ok || data.status !== "ok") {
          throw new Error(data.message || "Unexpected API error");
        }
        return data.data;
      }

      function setText(id, value) {
        const node = document.getElementById(id);
        if (node) node.textContent = value;
      }

      function setHtml(id, value) {
        const node = document.getElementById(id);
        if (node) node.innerHTML = value;
      }

      function indexDocumentIntegrity(records) {
        return Object.fromEntries(records.map((record) => [record.document_id, record]));
      }

      function getDocumentIntegrity(documentId) {
        return state.documentIntegrity[documentId] || null;
      }

      function titleCase(value) {
        return String(value || "")
          .split(/[_\\s-]+/)
          .filter(Boolean)
          .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
          .join(" ");
      }

      function formatStatusLabel(status) {
        const labels = {
          draft: "Draft",
          approved: "Approved",
          archived: "Archived",
          pending: "Pending",
          in_progress: "In progress",
          completed: "Completed",
          blocked: "Blocked",
          active: "Active"
        };
        return labels[status] || titleCase(status);
      }

      function formatCycleTypeLabel(type) {
        const labels = {
          daily: "Daily cycle",
          weekly: "Weekly cycle",
          monthly: "Monthly cycle"
        };
        return labels[type] || `${titleCase(type)} cycle`;
      }

      function formatDocumentTypeLabel(type) {
        const labels = {
          daily: "Daily note",
          weekly: "Weekly note",
          monthly: "Monthly note",
          note: "Supporting note",
          report: "Report"
        };
        return labels[type] || titleCase(type);
      }

      function formatPriorityLabel(priority) {
        const labels = {
          1: "Urgent priority",
          2: "High priority",
          3: "Normal priority",
          4: "Low priority"
        };
        return labels[priority] || `Priority ${priority}`;
      }

      function formatDate(value) {
        if (!value || value === "-") {
          return "-";
        }
        if (/^\\d{4}-\\d{2}-\\d{2}$/.test(String(value))) {
          return new Intl.DateTimeFormat(undefined, {
            month: "short",
            day: "numeric",
            year: "numeric",
            timeZone: "UTC"
          }).format(new Date(`${value}T00:00:00Z`));
        }
        const date = new Date(value);
        if (Number.isNaN(date.getTime())) {
          return String(value);
        }
        return new Intl.DateTimeFormat(undefined, {
          month: "short",
          day: "numeric",
          year: "numeric"
        }).format(date);
      }

      function formatDateTime(value) {
        if (!value || value === "-") {
          return "-";
        }
        const date = new Date(value);
        if (Number.isNaN(date.getTime())) {
          return String(value);
        }
        return new Intl.DateTimeFormat(undefined, {
          month: "short",
          day: "numeric",
          hour: "numeric",
          minute: "2-digit"
        }).format(date);
      }

      function findCycle(cycleId) {
        return state.cycles.find((cycle) => cycle.id === cycleId) || null;
      }

      function formatCycleWindow(cycle) {
        if (!cycle) return "Cycle window unavailable";
        if (cycle.end_date) {
          return `${formatDate(cycle.start_date)} to ${formatDate(cycle.end_date)}`;
        }
        return `Starts ${formatDate(cycle.start_date)}`;
      }

      function formatCycleLabel(cycle) {
        if (!cycle) return "Cycle";
        return formatCycleTypeLabel(cycle.type);
      }

      function formatCycleReference(cycleId) {
        const cycle = findCycle(cycleId);
        if (!cycle) {
          return cycleId || "Unlinked cycle";
        }
        return `${formatCycleLabel(cycle)} · ${formatCycleWindow(cycle)}`;
      }

      function renderTechnicalDetails(summary, entries) {
        const rows = entries.filter(([, value]) => value !== null && value !== undefined && value !== "");
        if (!rows.length) {
          return "";
        }
        return `
          <details class="quiet-details">
            <summary>${escapeHtml(summary)}</summary>
            <div class="technical-list">
              ${rows.map(([label, value]) => `
                <div class="technical-row">
                  <div class="technical-label">${escapeHtml(label)}</div>
                  <div class="technical-value">${escapeHtml(value)}</div>
                </div>
              `).join("")}
            </div>
          </details>
        `;
      }

      function setDetailFocus(focus) {
        state.detailFocus = focus;
        const activityCard = document.getElementById("activity-detail");
        const documentCard = document.getElementById("document-detail");
        const activityRole = document.getElementById("activity-role");
        const documentRole = document.getElementById("document-role");
        const selectionSummary = document.getElementById("selection-summary");
        const selectionHint = document.getElementById("selection-hint");
        const activityPrimary = focus !== "document";

        activityCard.classList.toggle("primary-focus", activityPrimary);
        activityCard.classList.toggle("secondary-focus", !activityPrimary);
        documentCard.classList.toggle("primary-focus", !activityPrimary);
        documentCard.classList.toggle("secondary-focus", activityPrimary);

        activityRole.textContent = activityPrimary ? "Primary focus" : "Related activity";
        documentRole.textContent = activityPrimary ? "Supporting document" : "Primary focus";

        if (activityPrimary) {
          selectionSummary.textContent = "The work item stays in front. Supporting material remains available without competing for the main reading path.";
          selectionHint.textContent = "Read the selected activity first, then open the supporting document only when you need evidence, lifecycle context, or integrity confirmation.";
        } else {
          selectionSummary.textContent = "The supporting document is now in focus. The related activity remains visible as the operational reason this material matters.";
          selectionHint.textContent = "Use the selected document to inspect evidence, status, and integrity, then return to the activity when you are ready to act.";
        }
      }

      function documentIntegrityBadgeMarkup(documentId) {
        const integrity = getDocumentIntegrity(documentId);
        if (!integrity) {
          return '<span class="badge">integrity unknown</span>';
        }
        const badgeClass =
          integrity.integrity_state === "ok"
            ? "success"
            : integrity.integrity_state === "warning"
            ? "warning"
            : "danger";
        return `<span class="badge ${badgeClass}">integrity ${escapeHtml(integrity.integrity_state)}</span>`;
      }

      function renderAuditLog() {
        const list = document.getElementById("audit-log-list");
        if (!state.auditLog.length) {
          list.innerHTML = '<li class="empty">No audit entries recorded yet.</li>';
          return;
        }

        list.innerHTML = state.auditLog.map((entry) => `
          <li class="resource-item">
            <div class="audit-entry">
              <div class="audit-entry-header">
                <div class="audit-title">${escapeHtml(describeAuditEntry(entry))}</div>
                <div class="audit-time">${escapeHtml(formatDateTime(entry.timestamp))}</div>
              </div>
              <div class="audit-reason">${escapeHtml(entry.reason || "No reason recorded")}</div>
              ${renderTechnicalDetails("Technical trace", [
                ["Action", entry.action],
                ["Object type", entry.entity_type],
                ["Object id", entry.entity_id || "-"],
                ["Agent", entry.agent || "-"],
                ["Timestamp", entry.timestamp]
              ])}
            </div>
          </li>
        `).join("");
      }

      function describeAuditEntry(entry) {
        const actionMap = {
          create: "Created",
          update: "Updated",
          reconcile: "Reconciled"
        };
        const typeMap = {
          activity: "activity",
          document: "document",
          cycle: "cycle",
          relation: "relation",
          entity: "entity"
        };
        const action = actionMap[entry.action] || titleCase(entry.action);
        const objectType = typeMap[entry.entity_type] || entry.entity_type;
        return `${action} ${objectType}`;
      }

      function activateView(viewId) {
        state.activeView = viewId;
        document.querySelectorAll(".tab-button").forEach((button) => {
          button.classList.toggle("active", button.dataset.view === viewId);
        });
        document.querySelectorAll(".view").forEach((view) => {
          view.classList.toggle("active", view.id === viewId);
        });
      }

      function setReadiness(title, detail, tone, revealSurfaces) {
        const panel = document.getElementById("page-readiness");
        panel.className = `panel readiness-panel ${tone}`;
        setText("page-readiness-title", title);
        setText("page-readiness-detail", detail);
        document.getElementById("cockpit-surfaces").hidden = !revealSurfaces;
      }

      function bindFilters() {
        [
          "entities-filter",
          "documents-filter",
          "documents-cycle-filter",
          "documents-status-filter",
          "cycles-filter",
          "cycles-status-filter",
          "activities-filter",
          "activities-cycle-filter",
          "activities-status-filter"
        ].forEach((id) => {
          const node = document.getElementById(id);
          if (node) {
            node.addEventListener("input", renderAllLists);
            node.addEventListener("change", renderAllLists);
          }
        });
      }

      function bindUiActions() {
        document.addEventListener("click", async (event) => {
          const button = event.target.closest("button");
          if (!button) {
            return;
          }

          if (button.dataset.view) {
            activateView(button.dataset.view);
            return;
          }

          if (button.id === "clear-cycle-focus") {
            clearCycleFocus();
            return;
          }

          if (button.dataset.setActivityStatus && !button.disabled) {
            await updateActivityStatus(
              button.dataset.activityId,
              button.dataset.setActivityStatus
            );
            return;
          }

          if (button.dataset.setDocumentStatus && !button.disabled) {
            await updateDocumentStatus(
              button.dataset.documentId,
              button.dataset.setDocumentStatus
            );
            return;
          }

          if (button.dataset.reconcileDocument && !button.disabled) {
            await reconcileDocument(button.dataset.reconcileDocument);
            return;
          }

          if (button.dataset.focusCycleId) {
            focusCycle(button.dataset.focusCycleId);
            activateView("cycles-view");
            return;
          }

          if (button.dataset.cycleId) {
            focusCycle(button.dataset.cycleId);
            activateView("cycles-view");
            return;
          }

          if (button.dataset.linkedActivityId) {
            await loadActivity(button.dataset.linkedActivityId);
            return;
          }

          if (button.dataset.linkedDocumentId) {
            await loadDocument(button.dataset.linkedDocumentId);
            return;
          }

          if (button.dataset.activityId) {
            await loadActivity(button.dataset.activityId);
            return;
          }

          if (button.dataset.documentId) {
            await loadDocument(button.dataset.documentId);
          }
        });
      }

      function populateCycleFilterOptions() {
        const options = ['<option value="">All cycles</option>']
          .concat(
            state.cycles.map((cycle) => (
              `<option value="${escapeAttribute(cycle.id)}">${escapeHtml(formatCycleLabel(cycle))} · ${escapeHtml(formatCycleWindow(cycle))}</option>`
            ))
          )
          .join("");
        setHtml("activities-cycle-filter", options);
        setHtml("documents-cycle-filter", options);
      }

      function getFocusedCycle() {
        return state.cycles.find((cycle) => cycle.id === state.focusedCycleId) || null;
      }

      function getCycleDocuments(cycleId) {
        return state.documents.filter((item) => item.cycle_id === cycleId);
      }

      function getEffectiveFilterValue(controlId) {
        const node = document.getElementById(controlId);
        if (!node) return "";
        return node.value || state.focusedCycleId || "";
      }

      function focusCycle(cycleId) {
        state.focusedCycleId = cycleId || null;
        updateCycleFocusBanner();
        renderAllLists();
        if (cycleId) {
          loadCycle(cycleId);
        }
      }

      function clearCycleFocus() {
        state.focusedCycleId = null;
        updateCycleFocusBanner();
        renderAllLists();
      }

      function updateCycleFocusBanner() {
        const cycle = getFocusedCycle();
        const activityHint = document.getElementById("activity-panel-hint");
        const documentHint = document.getElementById("documents-panel-hint");
        if (!cycle) {
          setHtml(
            "cycle-focus-banner",
            `
              <div>
                <strong>Cycle focus not set</strong>
                <div class="resource-meta" id="cycle-focus-meta">
                  Select a cycle to drive the activity and document inspection surface.
                </div>
              </div>
              <button class="inline-button" id="clear-cycle-focus" type="button" hidden>Clear focus</button>
            `
          );
          if (activityHint) {
            activityHint.textContent = "Focus a cycle to see the activities that need attention and the documents that support them.";
          }
          if (documentHint) {
            documentHint.textContent = "Documents stay visually secondary here so the work path remains cycle first, then activity, then supporting material.";
          }
          return;
        }

        const relatedDocuments = getCycleDocuments(cycle.id);

        setHtml(
          "cycle-focus-banner",
          `
            <div>
              <strong>${escapeHtml(formatCycleLabel(cycle))}</strong>
              <div class="resource-meta" id="cycle-focus-meta">
                ${escapeHtml(formatCycleWindow(cycle))} · ${escapeHtml(formatStatusLabel(cycle.status))} · ${escapeHtml(cycle.activity_count)} activities · ${escapeHtml(relatedDocuments.length)} supporting documents
              </div>
            </div>
            <button class="inline-button primary" id="clear-cycle-focus" type="button">Clear focus</button>
          `
        );
        if (activityHint) {
          activityHint.textContent = `Showing work inside the focused ${formatCycleTypeLabel(cycle.type).toLowerCase()}. Use this surface to see what is blocked, moving, or complete before opening supporting material.`;
        }
        if (documentHint) {
          documentHint.textContent = `Showing documents linked to this cycle. Treat them as support material for the selected work rather than as a separate stream of attention.`;
        }
      }

      function renderWorkspaceStatus(data) {
        state.status = data;
        setText("count-entities", String(data.counts?.entities ?? 0));
        setText("count-documents", String(data.counts?.documents ?? 0));
        setText("count-relations", String(data.counts?.relations ?? 0));
        setText("count-cycles", String(data.counts?.cycles ?? 0));
        setText("count-activities", String(data.counts?.activities ?? 0));

        const badge = document.getElementById("workspace-badge");
        badge.textContent = data.is_workspace
          ? `${data.workspace_name || "Workspace"} ready`
          : "Workspace not initialized";

        setHtml(
          "workspace-summary",
          [
            data.db_present ? "Local state connected" : "Local state missing",
            "Markdown support material available",
            `${escapeHtml(data.counts?.cycles ?? 0)} cycles under supervision`
          ].map((item) => `<span>${item}</span>`).join("")
        );

        setHtml(
          "workspace-notes",
          data.notes?.length
            ? data.notes.map((note) => `<div>${escapeHtml(note)}</div>`).join("")
            : "The current workspace is ready for cycle-first supervision."
        );
        setHtml(
          "workspace-technical-list",
          [
            ["Workspace root", data.workspace_root],
            ["Schema version", data.schema_version || "unknown"],
            ["Database path", data.paths?.database_path || "-"],
            ["Documents dir", data.paths?.documents_dir || "-"],
            ["Marker dir", data.paths?.marker_dir || "-"]
          ].map(([label, value]) => `
            <div class="technical-row">
              <div class="technical-label">${escapeHtml(label)}</div>
              <div class="technical-value">${escapeHtml(value)}</div>
            </div>
          `).join("")
        );

        const activity = data.activity_summary || {};
        setHtml(
          "operations-summary",
          [
            `${data.counts?.active_cycles ?? 0} active cycles`,
            `${data.counts?.draft_documents ?? 0} draft documents`,
            `${data.counts?.approved_documents ?? 0} approved documents`,
            `${activity.pending ?? 0} pending activities`,
            `${activity.in_progress ?? 0} in progress`,
            `${activity.blocked ?? 0} blocked`
          ].map((item) => `<span>${item}</span>`).join("")
        );
      }

      function renderAllLists() {
        renderEntities();
        renderDocuments();
        renderCycles();
        renderActivities();
      }

      function renderEntities() {
        const filterValue = document.getElementById("entities-filter").value.trim().toLowerCase();
        const list = document.getElementById("entities-list");
        const filtered = state.entities.filter((item) => {
          const haystack = `${item.name} ${item.type} ${item.context || ""}`.toLowerCase();
          return !filterValue || haystack.includes(filterValue);
        });
        if (!filtered.length) {
          list.innerHTML = '<li class="empty">No entities match the current filter.</li>';
          return;
        }
        list.innerHTML = filtered.map((item) => `
          <li class="resource-item">
            <div class="resource-title">${escapeHtml(item.name)}</div>
            <div class="resource-meta">${escapeHtml(item.type)} | ${escapeHtml(item.context || "-")}</div>
          </li>
        `).join("");
      }

      function renderDocuments() {
        const filterValue = document.getElementById("documents-filter").value.trim().toLowerCase();
        const statusValue = document.getElementById("documents-status-filter").value;
        const cycleValue = getEffectiveFilterValue("documents-cycle-filter");
        const list = document.getElementById("documents-list");
        const filtered = state.documents.filter((item) => {
          const haystack = `${item.title} ${item.path} ${item.cycle_id || ""}`.toLowerCase();
          const matchesFilter = !filterValue || haystack.includes(filterValue);
          const matchesStatus = !statusValue || item.status === statusValue;
          const matchesCycle = !cycleValue || item.cycle_id === cycleValue;
          return matchesFilter && matchesStatus && matchesCycle;
        });
        if (!filtered.length) {
          list.innerHTML = '<li class="empty">No documents match the current filter.</li>';
          return;
        }
        list.innerHTML = filtered.map((item) => `
          <li class="resource-item ${item.id === state.selectedDocumentId ? "selected" : ""}">
            <button type="button" data-document-id="${escapeAttribute(item.id)}">
              <div class="resource-title">${escapeHtml(item.title)}</div>
              <div class="resource-meta">${escapeHtml(formatDocumentTypeLabel(item.type))} · ${escapeHtml(formatStatusLabel(item.status))}</div>
              <div class="resource-meta">${escapeHtml(item.cycle_id ? formatCycleReference(item.cycle_id) : "General support material")}</div>
              <div class="compact-badges">${documentIntegrityBadgeMarkup(item.id)}</div>
            </button>
          </li>
        `).join("");
      }

      function renderCycles() {
        const filterValue = document.getElementById("cycles-filter").value.trim().toLowerCase();
        const statusValue = document.getElementById("cycles-status-filter").value;
        const list = document.getElementById("cycles-list");
        const filtered = state.cycles.filter((item) => {
          const haystack = `${item.id} ${item.type}`.toLowerCase();
          const matchesFilter = !filterValue || haystack.includes(filterValue);
          const matchesStatus = !statusValue || item.status === statusValue;
          return matchesFilter && matchesStatus;
        });
        if (!filtered.length) {
          list.innerHTML = '<li class="empty">No cycles match the current filter.</li>';
          return;
        }
        list.innerHTML = filtered.map((item) => `
          <li class="resource-item ${item.id === state.focusedCycleId ? "selected" : ""}">
            <button type="button" data-cycle-id="${escapeAttribute(item.id)}">
              <div class="resource-title">${escapeHtml(formatCycleLabel(item))}</div>
              <div class="resource-meta">${escapeHtml(formatCycleWindow(item))} · ${escapeHtml(formatStatusLabel(item.status))}</div>
              <div class="resource-meta">${escapeHtml(item.activity_count)} activities · ${escapeHtml(item.pending_count)} pending · ${escapeHtml(item.in_progress_count)} in progress · ${escapeHtml(item.completed_count)} completed</div>
              <div class="compact-badges">
                ${item.id === state.focusedCycleId ? '<span class="badge">focus</span>' : ""}
                ${item.blocked_count ? `<span class="badge danger">blocked ${escapeHtml(item.blocked_count)}</span>` : ""}
              </div>
            </button>
          </li>
        `).join("");
      }

      function renderActivities() {
        const filterValue = document.getElementById("activities-filter").value.trim().toLowerCase();
        const statusValue = document.getElementById("activities-status-filter").value;
        const cycleValue = getEffectiveFilterValue("activities-cycle-filter");
        const list = document.getElementById("activities-list");
        const filtered = state.activities.filter((item) => {
          const haystack = `${item.title} ${item.cycle_id} ${item.cycle_type || ""}`.toLowerCase();
          const matchesFilter = !filterValue || haystack.includes(filterValue);
          const matchesStatus = !statusValue || item.status === statusValue;
          const matchesCycle = !cycleValue || item.cycle_id === cycleValue;
          return matchesFilter && matchesStatus && matchesCycle;
        });
        const breakdown = summarizeActivities(filtered);
        setHtml(
          "activities-breakdown",
          [
            `<span class="badge warning">pending ${escapeHtml(breakdown.pending)}</span>`,
            `<span class="badge">in progress ${escapeHtml(breakdown.in_progress)}</span>`,
            `<span class="badge success">completed ${escapeHtml(breakdown.completed)}</span>`,
            breakdown.blocked ? `<span class="badge danger">blocked ${escapeHtml(breakdown.blocked)}</span>` : ""
          ].join("")
        );
        if (!filtered.length) {
          list.innerHTML = '<li class="empty">No activities match the current filter.</li>';
          return;
        }
        const orderedStatuses = ["blocked", "in_progress", "pending", "completed"];
        const labels = {
          pending: "Pending",
          in_progress: "In Progress",
          completed: "Completed",
          blocked: "Blocked"
        };
        list.innerHTML = orderedStatuses
          .filter((status) => filtered.some((item) => item.status === status))
          .map((status) => `
            <li class="status-group-card">
              <h4>${escapeHtml(labels[status])}</h4>
              <ul class="status-group-items">
                ${filtered
                  .filter((item) => item.status === status)
                  .map((item) => `
                    <li class="${item.id === state.selectedActivityId ? "selected" : ""}">
                      <button type="button" data-activity-id="${escapeAttribute(item.id)}">
                        <div class="resource-title">${escapeHtml(item.title)}</div>
                        <div class="resource-meta">${escapeHtml(formatPriorityLabel(item.priority))} · ${escapeHtml(formatCycleReference(item.cycle_id))}</div>
                      </button>
                    </li>
                  `)
                  .join("")}
              </ul>
            </li>
          `)
          .join("");
      }

      function summarizeActivities(activities) {
        const summary = { pending: 0, in_progress: 0, completed: 0, blocked: 0 };
        activities.forEach((activity) => {
          if (Object.prototype.hasOwnProperty.call(summary, activity.status)) {
            summary[activity.status] += 1;
          }
        });
        return summary;
      }

      function renderActivityStatusControls(activity) {
        const controls = document.getElementById("activity-status-controls");
        const statuses = ["pending", "in_progress", "completed", "blocked"];
        controls.innerHTML = statuses.map((status) => `
          <button
            class="inline-button ${activity.status === status ? "primary" : ""}"
            type="button"
            data-activity-id="${escapeAttribute(activity.id)}"
            data-set-activity-status="${escapeAttribute(status)}"
            ${activity.status === status ? "disabled" : ""}
          >
            ${escapeHtml(formatStatusLabel(status))}
          </button>
        `).join("");
      }

      function documentStatusBadgeClass(status) {
        if (status === "draft") return "warning";
        if (status === "approved") return "success";
        if (status === "archived") return "danger";
        return "";
      }

      function renderDocumentStatusControls(documentRecord) {
        const controls = document.getElementById("document-status-controls");
        const allowedTransitions = {
          draft: ["approved"],
          approved: ["archived"],
          archived: []
        };
        const targets = [documentRecord.status].concat(allowedTransitions[documentRecord.status] || []);
        controls.innerHTML = targets.map((status) => `
          <button
            class="inline-button ${documentRecord.status === status ? "primary" : ""}"
            type="button"
            data-document-id="${escapeAttribute(documentRecord.id)}"
            data-set-document-status="${escapeAttribute(status)}"
            ${documentRecord.status === status ? "disabled" : ""}
          >
            ${escapeHtml(formatStatusLabel(status))}
          </button>
        `).join("");
      }

      function canOfferDocumentReconcile(integrity) {
        return Boolean(
          integrity &&
          integrity.backing_file_exists &&
          (
            integrity.content_hash_matches === false ||
            (integrity.path_matches_expected === false && integrity.expected_path_exists)
          )
        );
      }

      async function refreshOperationalData() {
        const [status, auditLog, documents, documentIntegrity, cycles, activities] = await Promise.all([
          fetchJson(api.status),
          fetchJson(`${api.auditLog}?limit=6`),
          fetchJson(api.documents),
          fetchJson(api.documentIntegrity),
          fetchJson(api.cycles),
          fetchJson(api.activities)
        ]);
        renderWorkspaceStatus(status);
        state.auditLog = auditLog;
        renderAuditLog();
        state.documents = documents;
        state.documentIntegrity = indexDocumentIntegrity(documentIntegrity);
        state.cycles = cycles;
        state.activities = activities;
        populateCycleFilterOptions();
        renderAllLists();
      }

      async function updateActivityStatus(activityId, status) {
        const feedback = document.getElementById("activity-status-feedback");
        const currentView = state.activeView;
        const mutationKey = `${activityId}:${status}`;
        if (state.pendingActivityMutation === mutationKey) {
          return;
        }
        state.pendingActivityMutation = mutationKey;
        feedback.textContent = "Updating activity status...";
        feedback.classList.remove("error");
        try {
          const updated = await patchJson(`/api/activities/${encodeURIComponent(activityId)}`, { status });
          await refreshOperationalData();
          await loadActivity(updated.id);
          if (state.focusedCycleId) {
            await loadCycle(state.focusedCycleId);
          }
          activateView(currentView);
          feedback.textContent = `Status updated to ${updated.status}.`;
        } catch (error) {
          feedback.textContent = error.message;
          feedback.classList.add("error");
        } finally {
          state.pendingActivityMutation = null;
        }
      }

      async function updateDocumentStatus(documentId, status) {
        const feedback = document.getElementById("document-status-feedback");
        const currentView = state.activeView;
        const mutationKey = `${documentId}:${status}`;
        if (state.pendingDocumentMutation === mutationKey) {
          return;
        }
        state.pendingDocumentMutation = mutationKey;
        feedback.textContent = "Updating document status...";
        feedback.classList.remove("error");
        try {
          const updated = await patchJson(`/api/documents/${encodeURIComponent(documentId)}`, { status });
          await refreshOperationalData();
          await loadDocument(updated.id);
          if (state.focusedCycleId) {
            await loadCycle(state.focusedCycleId);
          }
          activateView(currentView);
          feedback.textContent = `Status updated to ${updated.status}.`;
        } catch (error) {
          feedback.textContent = error.message;
          feedback.classList.add("error");
        } finally {
          state.pendingDocumentMutation = null;
        }
      }

      async function reconcileDocument(documentId) {
        const feedback = document.getElementById("document-status-feedback");
        const currentView = state.activeView;
        if (state.pendingReconcileDocumentId === documentId) {
          return;
        }
        state.pendingReconcileDocumentId = documentId;
        feedback.textContent = "Reconciling document metadata...";
        feedback.classList.remove("error");
        try {
          const updated = await postJson(`${api.documentReconcile}/${encodeURIComponent(documentId)}/reconcile`);
          await refreshOperationalData();
          await loadDocument(updated.record.id);
          if (state.focusedCycleId) {
            await loadCycle(state.focusedCycleId);
          }
          activateView(currentView);
          feedback.textContent = updated.reconciled_fields.length
            ? `Reconciled: ${updated.reconciled_fields.join(", ")}.`
            : "Document metadata was already aligned.";
        } catch (error) {
          feedback.textContent = error.message;
          feedback.classList.add("error");
        } finally {
          state.pendingReconcileDocumentId = null;
        }
      }

      async function loadDocument(documentId, options = {}) {
        const { preserveFocus = false, activateDocumentView = true } = options;
        state.selectedDocumentId = documentId;
        if (activateDocumentView) {
          activateView("documents-view");
        }
        if (!preserveFocus) {
          setDetailFocus("document");
        }
        const empty = document.getElementById("document-empty");
        const content = document.getElementById("document-content");
        const preview = document.getElementById("document-preview");
        const header = document.getElementById("document-header");
        empty.hidden = true;
        content.hidden = false;
        setHtml("document-header", "");
        setHtml("document-meta-grid", "");
        setHtml("document-flags", "");
        setHtml("document-status-controls", "");
        setHtml("document-actions", "");
        setHtml("document-technical", "");
        setText("document-status-feedback", "");
        preview.classList.remove("error-state");
        preview.textContent = "Loading document...";
        let integrity = getDocumentIntegrity(documentId);
        try {
          integrity = await fetchJson(`${api.documentIntegrity}/${encodeURIComponent(documentId)}`);
          state.documentIntegrity[documentId] = integrity;
          const doc = await fetchJson(`/api/documents/${encodeURIComponent(documentId)}`);
          const integrityBadgeClass =
            integrity.integrity_state === "ok"
              ? "success"
              : integrity.integrity_state === "warning"
              ? "warning"
              : "danger";
          const linkedCycle = findCycle(doc.cycle_id);
          header.innerHTML = `
            <strong>${escapeHtml(doc.title)}</strong>
            <div class="inline-note">
              ${escapeHtml(formatDocumentTypeLabel(doc.type))} · ${escapeHtml(formatStatusLabel(doc.status))} · ${escapeHtml(doc.cycle_id ? formatCycleReference(doc.cycle_id) : "General support material")}
            </div>
          `;
          setHtml("document-meta-grid", renderMetaGrid([
            ["State", formatStatusLabel(doc.status)],
            ["Document kind", formatDocumentTypeLabel(doc.type)],
            ["Cycle context", doc.cycle_id ? formatCycleReference(doc.cycle_id) : "General support material"],
            ["Integrity", formatStatusLabel(integrity.integrity_state)],
            ["Approval", doc.approved_at ? `Approved ${formatDateTime(doc.approved_at)}` : "Not approved yet"],
            ["Reading status", integrity.integrity_state === "ok" ? "Trusted for reading" : "Needs attention"]
          ]));
          setHtml(
            "document-flags",
            [
              `<span class="badge">${escapeHtml(formatDocumentTypeLabel(doc.type))}</span>`,
              `<span class="badge ${documentStatusBadgeClass(doc.status)}">${escapeHtml(formatStatusLabel(doc.status))}</span>`,
              `<span class="badge ${integrityBadgeClass}">integrity ${escapeHtml(formatStatusLabel(integrity.integrity_state))}</span>`,
              linkedCycle ? `<span class="badge">${escapeHtml(formatCycleLabel(linkedCycle))}</span>` : "",
              integrity.issues.length ? `<span class="badge ${integrityBadgeClass}">${escapeHtml(integrity.issues.join(", "))}</span>` : "",
              doc.approved_at ? `<span class="badge">approved</span>` : ""
            ].join("")
          );
          renderDocumentStatusControls(doc);
          const reconcileAvailable = canOfferDocumentReconcile(integrity);
          setHtml(
            "document-actions",
            [
              doc.cycle_id
                ? `<button class="inline-button primary" type="button" data-focus-cycle-id="${escapeAttribute(doc.cycle_id)}">Focus cycle ${escapeHtml(doc.cycle_id)}</button>`
                : "",
              `<button class="inline-button ${reconcileAvailable ? "primary" : ""}" type="button" data-reconcile-document="${escapeAttribute(doc.id)}" ${reconcileAvailable ? "" : "disabled"}>
                Reconcile metadata
              </button>`
            ].join("")
          );
          setText(
            "document-status-feedback",
            reconcileAvailable
              ? "Safe reconcile is available for the current file metadata drift."
              : "Document metadata is aligned. Reconcile becomes available only when safe drift is detected."
          );
          setHtml(
            "document-technical",
            renderTechnicalDetails("Technical document details", [
              ["Document id", doc.id],
              ["Stored path", doc.path],
              ["Expected path", integrity.expected_path || "-"],
              ["Version", doc.version],
              ["Created at", doc.created_at],
              ["Modified at", doc.modified_at],
              ["Approved at", doc.approved_at || "-"]
            ])
          );
          preview.textContent = doc.content_preview || "(empty document)";
        } catch (error) {
          if (!integrity) {
            try {
              integrity = await fetchJson(`${api.documentIntegrity}/${encodeURIComponent(documentId)}`);
              state.documentIntegrity[documentId] = integrity;
            } catch {
              integrity = null;
            }
          }
          const integrityBadgeClass =
            integrity?.integrity_state === "warning"
              ? "warning"
              : integrity?.integrity_state === "ok"
              ? "success"
              : "danger";
          header.innerHTML = `
            <strong>${escapeHtml(integrity?.title || "Document unavailable")}</strong>
            <div class="inline-note">
              ${escapeHtml(formatStatusLabel(integrity?.status || "Unavailable"))} · integrity ${escapeHtml(formatStatusLabel(integrity?.integrity_state || "error"))}
            </div>
          `;
          setHtml("document-meta-grid", renderMetaGrid([
            ["State", integrity?.status ? formatStatusLabel(integrity.status) : "Unavailable"],
            ["Integrity", formatStatusLabel(integrity?.integrity_state || "error")],
            ["Reading status", "Needs operator attention"]
          ]));
          setHtml(
            "document-flags",
            [
              integrity ? `<span class="badge ${integrityBadgeClass}">integrity ${escapeHtml(formatStatusLabel(integrity.integrity_state))}</span>` : "",
              integrity?.issues?.length ? `<span class="badge ${integrityBadgeClass}">${escapeHtml(integrity.issues.join(", "))}</span>` : '<span class="badge danger">backing file issue</span>'
            ].join("")
          );
          setHtml("document-status-controls", "");
          setHtml(
            "document-actions",
            integrity
              ? `<button class="inline-button ${canOfferDocumentReconcile(integrity) ? "primary" : ""}" type="button" data-reconcile-document="${escapeAttribute(integrity.document_id)}" ${canOfferDocumentReconcile(integrity) ? "" : "disabled"}>
                  Reconcile metadata
                </button>`
              : ""
          );
          setText(
            "document-status-feedback",
            integrity && canOfferDocumentReconcile(integrity)
              ? "Safe reconcile is available for the current file metadata drift."
              : "Reconcile is unavailable until the backing file can be resolved safely."
          );
          setHtml(
            "document-technical",
            renderTechnicalDetails("Technical document details", [
              ["Document id", integrity?.document_id || documentId],
              ["Stored path", integrity?.path || "-"],
              ["Expected path", integrity?.expected_path || "-"],
              ["Absolute path", integrity?.absolute_path || "-"]
            ])
          );
          preview.classList.add("error-state");
          preview.textContent = `Document inspection failed. ${error.message}`;
        }
      }

      async function loadCycle(cycleId) {
        state.selectedCycleId = cycleId;
        state.focusedCycleId = cycleId;
        updateCycleFocusBanner();
        const empty = document.getElementById("cycle-empty");
        const content = document.getElementById("cycle-content");
        empty.hidden = true;
        content.hidden = false;
        setHtml("cycle-story", "");
        setHtml("cycle-meta-grid", "");
        setHtml("cycle-breakdown", "");
        setHtml("cycle-activities", '<li class="resource-meta">Loading cycle activities...</li>');
        setHtml("cycle-documents", '<li class="resource-meta">Loading related documents...</li>');
        setHtml("cycle-technical", "");
        try {
          const [cycle, activities] = await Promise.all([
            fetchJson(`/api/cycles/${encodeURIComponent(cycleId)}`),
            fetchJson(`/api/activities?cycle_id=${encodeURIComponent(cycleId)}`)
          ]);
          const relatedDocuments = getCycleDocuments(cycleId);
          setHtml(
            "cycle-story",
            `${escapeHtml(formatCycleLabel(cycle))} is ${escapeHtml(formatStatusLabel(cycle.status).toLowerCase())} and anchors ${escapeHtml(cycle.activity_count)} activities with ${escapeHtml(relatedDocuments.length)} supporting documents. ${escapeHtml(cycle.description || "Use it as the main frame for understanding what matters now.")}`
          );
          setHtml("cycle-meta-grid", renderMetaGrid([
            ["Cycle", formatCycleLabel(cycle)],
            ["Window", formatCycleWindow(cycle)],
            ["State", formatStatusLabel(cycle.status)],
            ["Activities", String(cycle.activity_count)],
            ["Supporting documents", String(relatedDocuments.length)],
            ["Blocked work", cycle.blocked_count ? `${cycle.blocked_count} blocked` : "No blocked work"]
          ]));
          setHtml(
            "cycle-breakdown",
            [
              `<span class="badge">${escapeHtml(formatStatusLabel(cycle.status))}</span>`,
              `<span class="badge">activities ${escapeHtml(cycle.activity_count)}</span>`,
              `<span class="badge warning">pending ${escapeHtml(cycle.pending_count)}</span>`,
              `<span class="badge">in progress ${escapeHtml(cycle.in_progress_count)}</span>`,
              `<span class="badge success">completed ${escapeHtml(cycle.completed_count)}</span>`,
              cycle.blocked_count ? `<span class="badge danger">blocked ${escapeHtml(cycle.blocked_count)}</span>` : "",
              `<span class="badge">documents ${escapeHtml(relatedDocuments.length)}</span>`
            ].join("")
          );
          setHtml(
            "cycle-technical",
            renderTechnicalDetails("Technical cycle details", [
              ["Cycle id", cycle.id],
              ["Type", cycle.type],
              ["Start date", cycle.start_date],
              ["End date", cycle.end_date || "-"],
              ["Created at", cycle.created_at]
            ])
          );
          const activitiesList = document.getElementById("cycle-activities");
          if (!activities.length) {
            activitiesList.innerHTML = '<li class="empty">No activities linked to this cycle.</li>';
          } else {
            activitiesList.innerHTML = activities.map((item) => `
              <li class="resource-item">
                <button type="button" data-linked-activity-id="${escapeAttribute(item.id)}">
                  <div class="resource-title">${escapeHtml(item.title)}</div>
                  <div class="resource-meta">${escapeHtml(formatStatusLabel(item.status))} · ${escapeHtml(formatPriorityLabel(item.priority))}</div>
                </button>
              </li>
            `).join("");
          }
          const documentsList = document.getElementById("cycle-documents");
          if (!relatedDocuments.length) {
            documentsList.innerHTML = '<li class="empty">No documents currently linked to this cycle.</li>';
          } else {
            documentsList.innerHTML = relatedDocuments.map((item) => `
              <li class="resource-item">
                <button type="button" data-linked-document-id="${escapeAttribute(item.id)}">
                  <div class="resource-title">${escapeHtml(item.title)}</div>
                  <div class="resource-meta">${escapeHtml(formatDocumentTypeLabel(item.type))} · ${escapeHtml(formatStatusLabel(item.status))}</div>
                  <div class="compact-badges">${documentIntegrityBadgeMarkup(item.id)}</div>
                </button>
              </li>
            `).join("");
          }
          if (
            activities.length &&
            !activities.some((item) => item.id === state.selectedActivityId)
          ) {
            await loadActivity(activities[0].id);
          }
          if (
            relatedDocuments.length &&
            !relatedDocuments.some((item) => item.id === state.selectedDocumentId)
          ) {
            await loadDocument(relatedDocuments[0].id, { preserveFocus: true, activateDocumentView: false });
          }
          renderAllLists();
        } catch (error) {
          setHtml("cycle-story", "This cycle could not be read from the local workspace.");
          setHtml("cycle-meta-grid", renderMetaGrid([
            ["Cycle", cycleId],
            ["State", "Unavailable"]
          ]));
          setHtml("cycle-breakdown", '<span class="badge danger">cycle load failed</span>');
          setHtml("cycle-activities", `<li class="empty error">${escapeHtml(error.message)}</li>`);
          setHtml("cycle-documents", '<li class="empty">Related documents could not be resolved.</li>');
        }
      }

      async function loadActivity(activityId, options = {}) {
        const { preserveFocus = false, activateActivityView = true } = options;
        state.selectedActivityId = activityId;
        if (activateActivityView) {
          activateView("activities-view");
        }
        if (!preserveFocus) {
          setDetailFocus("activity");
        }
        const empty = document.getElementById("activity-empty");
        const content = document.getElementById("activity-content");
        empty.hidden = true;
        content.hidden = false;
        setHtml("activity-summary", "");
        setHtml("activity-meta-grid", "");
        setHtml("activity-flags", "");
        setHtml("activity-status-controls", "");
        setHtml("activity-actions", "");
        setHtml("activity-technical", "");
        setText("activity-status-feedback", "");
        try {
          const activity = await fetchJson(`/api/activities/${encodeURIComponent(activityId)}`);
          setHtml(
            "activity-summary",
            `<strong>${escapeHtml(activity.title)}</strong><div class="section-copy">${escapeHtml(activity.description || "This work item carries the main operational action inside the selected cycle.")}</div>`
          );
          setHtml("activity-meta-grid", renderMetaGrid([
            ["State", formatStatusLabel(activity.status)],
            ["Priority", formatPriorityLabel(activity.priority)],
            ["Cycle context", formatCycleReference(activity.cycle_id)],
            ["Work type", activity.activity_type ? titleCase(activity.activity_type) : "General work"],
            ["Cycle start", activity.cycle_start_date ? formatDate(activity.cycle_start_date) : "-"],
            ["Reading status", activity.status === "blocked" ? "Needs support before it can move" : "Ready for operational review"]
          ]));
          setHtml(
            "activity-flags",
            [
              activity.status === "pending" ? '<span class="badge warning">pending</span>' : "",
              activity.status === "in_progress" ? '<span class="badge">in progress</span>' : "",
              activity.status === "completed" ? '<span class="badge success">completed</span>' : "",
              activity.status === "blocked" ? '<span class="badge danger">blocked</span>' : "",
              `<span class="badge">${escapeHtml(formatPriorityLabel(activity.priority))}</span>`,
              `<span class="badge">${escapeHtml(formatCycleLabel(findCycle(activity.cycle_id) || { type: activity.cycle_type || "cycle" }))}</span>`
            ].join("")
          );
          renderActivityStatusControls(activity);
          setHtml(
            "activity-actions",
            [
              `<button class="inline-button primary" type="button" data-focus-cycle-id="${escapeAttribute(activity.cycle_id)}">Focus cycle ${escapeHtml(activity.cycle_id)}</button>`,
              state.documents.some((item) => item.cycle_id === activity.cycle_id)
                ? `<button class="inline-button" type="button" data-linked-document-id="${escapeAttribute(state.documents.find((item) => item.cycle_id === activity.cycle_id).id)}">Open a supporting document</button>`
                : ""
            ].join("")
          );
          setHtml(
            "activity-technical",
            renderTechnicalDetails("Technical activity details", [
              ["Activity id", activity.id],
              ["Cycle id", activity.cycle_id],
              ["Cycle type", activity.cycle_type || "-"],
              ["Created at", activity.created_at],
              ["Raw status", activity.status]
            ])
          );
        } catch (error) {
          setHtml("activity-summary", "The selected activity could not be read from the local workspace.");
          setHtml("activity-meta-grid", renderMetaGrid([
            ["Activity", activityId],
            ["State", "Unavailable"]
          ]));
          setHtml("activity-status-controls", "");
          setHtml("activity-flags", `<span class="badge danger">${escapeHtml(error.message)}</span>`);
          setHtml("activity-actions", "");
        }
      }

      function renderMetaGrid(entries) {
        return entries.map(([label, value]) => `
          <div>
            <div class="label">${escapeHtml(label)}</div>
            <strong>${escapeHtml(value)}</strong>
          </div>
        `).join("");
      }

      function setWorkspaceEmptyState() {
        ["entities-list", "documents-list", "cycles-list", "activities-list", "audit-log-list"].forEach((id) => {
          setHtml(id, '<li class="empty">Workspace is not initialized.</li>');
        });
        setHtml("activities-breakdown", "");
        setHtml("cycle-activities", '<li class="empty">Workspace is not initialized.</li>');
        setHtml("cycle-documents", '<li class="empty">Workspace is not initialized.</li>');
        setHtml("workspace-technical-list", "");
      }

      function escapeHtml(value) {
        return String(value)
          .replaceAll("&", "&amp;")
          .replaceAll("<", "&lt;")
          .replaceAll(">", "&gt;")
          .replaceAll('"', "&quot;")
          .replaceAll("'", "&#39;");
      }

      function escapeAttribute(value) {
        return escapeHtml(value);
      }

      async function bootCockpit() {
        bindUiActions();
        bindFilters();
        setDetailFocus("activity");
        updateCycleFocusBanner();
        setReadiness(
          "Preparing cockpit...",
          "Checking the workspace and preparing the cycle-centered supervision surface.",
          "loading",
          false
        );
        try {
          const status = await fetchJson(api.status);
          renderWorkspaceStatus(status);
          if (!status.is_workspace) {
            setWorkspaceEmptyState();
            setReadiness(
              "Workspace not initialized",
              "Run `python -m nexus init ./sandbox-workspace` and seed data before opening the cockpit.",
              "warning",
              false
            );
            return;
          }

          setReadiness(
            "Workspace found",
            "Loading cycles, activities, documents, and the supporting supervision context.",
            "loading",
            false
          );

          const [entities, documents, documentIntegrity, auditLog, cycles, activities] = await Promise.all([
            fetchJson(api.entities),
            fetchJson(api.documents),
            fetchJson(api.documentIntegrity),
            fetchJson(`${api.auditLog}?limit=6`),
            fetchJson(api.cycles),
            fetchJson(api.activities)
          ]);

          state.entities = entities;
          state.documents = documents;
          state.documentIntegrity = indexDocumentIntegrity(documentIntegrity);
          state.auditLog = auditLog;
          state.cycles = cycles;
          state.activities = activities;
          renderAuditLog();
          populateCycleFilterOptions();
          renderAllLists();
          activateView("cycles-view");

          if (cycles[0]) {
            await loadCycle(cycles[0].id);
          } else if (activities[0]) {
            await loadActivity(activities[0].id);
          }
          if (!cycles[0] && documents[0]) {
            await loadDocument(documents[0].id);
          }
          activateView("cycles-view");
          setReadiness(
            "Workspace ready",
            "The cycle, activity, document, and supervision surfaces are fully loaded.",
            "ready",
            true
          );
        } catch (error) {
          document.getElementById("workspace-badge").textContent = "Cockpit load failed";
          document.getElementById("workspace-notes").innerHTML = `<span class="error">${escapeHtml(error.message)}</span>`;
          setWorkspaceEmptyState();
          setReadiness(
            "Cockpit load failed",
            error.message,
            "error",
            false
          );
        }
      }

      bootCockpit();
    </script>
  </body>
</html>
"""
