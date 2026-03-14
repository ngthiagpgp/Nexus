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
        color-scheme: light;
        --page: #eff4f8;
        --panel: #ffffff;
        --panel-muted: #f8fafc;
        --border: #d7e0e8;
        --text: #1d2833;
        --muted: #607080;
        --accent: #165dff;
        --accent-soft: #e7efff;
        --success-soft: #e8f7ef;
        --warning-soft: #fff5db;
        --danger-soft: #ffe9e8;
        --danger: #b42318;
      }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        font-family: "Segoe UI", system-ui, sans-serif;
        color: var(--text);
        background:
          radial-gradient(circle at top left, rgba(22, 93, 255, 0.08), transparent 24%),
          linear-gradient(180deg, #ecf2f7 0%, #f8fafc 100%);
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
      }
      .panel {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 18px;
        box-shadow: 0 16px 40px rgba(30, 50, 70, 0.06);
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
        background: var(--accent-soft);
        border: 1px solid #d2dfff;
        border-radius: 16px;
        padding: 14px;
      }
      .stat-card strong {
        display: block;
        margin-top: 8px;
        font-size: 1.9rem;
      }
      .status-strip {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        color: var(--muted);
        font-size: 0.95rem;
        margin-top: 12px;
      }
      .two-column {
        grid-template-columns: minmax(0, 1.3fr) minmax(380px, 0.95fr);
        align-items: start;
      }
      .stack {
        display: grid;
        gap: 16px;
      }
      .tabs {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 14px;
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
        color: #0d3fa8;
        background: var(--accent-soft);
        border-color: #c8d8ff;
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
        background: #fff;
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
        background: linear-gradient(90deg, #eff5ff 0%, #f8fbff 100%);
        border: 1px solid #d7e4ff;
      }
      .focus-banner strong {
        display: block;
        margin-bottom: 4px;
      }
      .view {
        display: none;
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
      .resource-meta,
      .label {
        color: var(--muted);
        font-size: 0.92rem;
      }
      .selection-panel {
        background: linear-gradient(180deg, #ffffff 0%, #fbfcfd 100%);
      }
      .detail-card {
        margin-top: 14px;
        padding: 14px;
        border: 1px solid var(--border);
        border-radius: 14px;
        background: var(--panel-muted);
      }
      .detail-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 10px;
        margin-top: 14px;
      }
      .detail-grid div {
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 10px;
        background: #fff;
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
      .detail-preview {
        margin-top: 14px;
        padding: 14px;
        border-radius: 14px;
        background: #111a24;
        color: #f7fbff;
        white-space: pre-wrap;
        font-family: "Cascadia Code", Consolas, monospace;
        font-size: 0.9rem;
        min-height: 180px;
      }
      .detail-preview.error-state {
        background: var(--danger-soft);
        color: var(--danger);
        font-family: inherit;
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
        color: #1845b5;
      }
      .badge.success {
        background: var(--success-soft);
        color: #17683a;
      }
      .badge.warning {
        background: var(--warning-soft);
        color: #8a5b00;
      }
      .badge.danger {
        background: var(--danger-soft);
        color: var(--danger);
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
        background: #fff;
      }
      [hidden] { display: none !important; }
      @media (max-width: 960px) {
        .hero { align-items: start; flex-direction: column; }
        .two-column { grid-template-columns: 1fr; }
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
            Read-only local supervision with cycles as the main operational surface for activities and documents.
          </p>
        </div>
        <div id="workspace-badge" class="panel" aria-live="polite">Loading workspace...</div>
      </section>

      <section class="grid stats-grid" id="summary-grid" aria-live="polite">
        <article class="stat-card"><span class="label">Entities</span><strong id="count-entities">-</strong></article>
        <article class="stat-card"><span class="label">Documents</span><strong id="count-documents">-</strong></article>
        <article class="stat-card"><span class="label">Relations</span><strong id="count-relations">-</strong></article>
        <article class="stat-card"><span class="label">Cycles</span><strong id="count-cycles">-</strong></article>
        <article class="stat-card"><span class="label">Activities</span><strong id="count-activities">-</strong></article>
      </section>

      <section class="grid two-column">
        <div class="stack">
          <article class="panel">
            <h2>Workspace Status</h2>
            <div class="status-strip" id="workspace-summary"></div>
            <div class="inline-note" id="workspace-notes"></div>
          </article>

          <article class="panel">
            <h2>Operational Summary</h2>
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

          <article class="panel">
            <nav class="tabs" id="cockpit-tabs" aria-label="Cockpit views">
              <button class="tab-button active" id="tab-cycles" type="button" data-view="cycles-view">Cycles</button>
              <button class="tab-button" id="tab-activities" type="button" data-view="activities-view">Activities</button>
              <button class="tab-button" id="tab-documents" type="button" data-view="documents-view">Documents</button>
              <button class="tab-button" id="tab-entities" type="button" data-view="entities-view">Entities</button>
            </nav>

            <section class="view active" id="cycles-view">
              <h2>Cycles</h2>
              <div class="toolbar">
                <input id="cycles-filter" type="search" placeholder="Filter by id or type" />
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

            <section class="view" id="activities-view">
              <h2>Activities</h2>
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
              <ul class="resource-list" id="activities-list">
                <li class="resource-meta">Loading activities...</li>
              </ul>
            </section>

            <section class="view" id="documents-view">
              <h2>Documents</h2>
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

            <section class="view" id="entities-view">
              <h2>Entities</h2>
              <div class="toolbar">
                <input id="entities-filter" type="search" placeholder="Filter by name, type, or context" />
              </div>
              <ul class="resource-list" id="entities-list">
                <li class="resource-meta">Loading entities...</li>
              </ul>
            </section>
          </article>
        </div>

        <aside class="stack">
          <article class="panel selection-panel">
            <h2>Inspection</h2>
            <p class="inline-note" id="selection-hint">
              Use cycles as the main navigation point, then inspect linked activities and supporting documents.
            </p>

            <section class="detail-card" id="cycle-detail">
              <h3>Cycle Inspection</h3>
              <div class="empty" id="cycle-empty">No cycle selected.</div>
              <div id="cycle-content" hidden>
                <div class="detail-grid" id="cycle-meta-grid"></div>
                <div class="compact-badges" id="cycle-breakdown"></div>
                <div class="detail-section">
                  <h4>Related Activities</h4>
                  <ul class="resource-list" id="cycle-activities"></ul>
                </div>
                <div class="detail-section">
                  <h4>Related Documents</h4>
                  <ul class="resource-list" id="cycle-documents"></ul>
                </div>
              </div>
            </section>

            <section class="detail-card" id="activity-detail">
              <h3>Activity Inspection</h3>
              <div class="empty" id="activity-empty">No activity selected.</div>
              <div id="activity-content" hidden>
                <div class="detail-grid" id="activity-meta-grid"></div>
                <div class="compact-badges" id="activity-flags"></div>
                <div class="detail-actions" id="activity-actions"></div>
              </div>
            </section>

            <section class="detail-card" id="document-detail">
              <h3>Document Inspection</h3>
              <div class="empty" id="document-empty">No document selected.</div>
              <div id="document-content" hidden>
                <div class="detail-grid" id="document-meta-grid"></div>
                <div class="compact-badges" id="document-flags"></div>
                <div class="detail-actions" id="document-actions"></div>
                <div class="detail-preview" id="document-preview"></div>
              </div>
            </section>
          </article>
        </aside>
      </section>
    </main>

    <script>
      const api = {
        status: "/api/system/status",
        entities: "/api/entities",
        documents: "/api/documents",
        cycles: "/api/cycles",
        activities: "/api/activities"
      };

      const state = {
        status: null,
        entities: [],
        documents: [],
        cycles: [],
        activities: [],
        activeView: "cycles-view",
        focusedCycleId: null,
        selectedDocumentId: null,
        selectedCycleId: null,
        selectedActivityId: null
      };

      async function fetchJson(url) {
        const response = await fetch(url, { headers: { "Accept": "application/json" } });
        const payload = await response.json();
        if (!response.ok || payload.status !== "ok") {
          throw new Error(payload.message || "Unexpected API error");
        }
        return payload.data;
      }

      function setText(id, value) {
        const node = document.getElementById(id);
        if (node) node.textContent = value;
      }

      function setHtml(id, value) {
        const node = document.getElementById(id);
        if (node) node.innerHTML = value;
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

      function bindTabs() {
        document.querySelectorAll(".tab-button").forEach((button) => {
          button.addEventListener("click", () => activateView(button.dataset.view));
        });
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
        document.getElementById("clear-cycle-focus").addEventListener("click", clearCycleFocus);
      }

      function bindDynamicActions() {
        document.querySelectorAll("[data-focus-cycle-id]").forEach((button) => {
          button.addEventListener("click", () => {
            focusCycle(button.dataset.focusCycleId);
            activateView("cycles-view");
          });
        });
      }

      function populateCycleFilterOptions() {
        const options = ['<option value="">All cycles</option>']
          .concat(
            state.cycles.map((cycle) => (
              `<option value="${escapeAttribute(cycle.id)}">${escapeHtml(cycle.id)} | ${escapeHtml(cycle.type)}</option>`
            ))
          )
          .join("");
        setHtml("activities-cycle-filter", options);
        setHtml("documents-cycle-filter", options);
      }

      function getFocusedCycle() {
        return state.cycles.find((cycle) => cycle.id === state.focusedCycleId) || null;
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
          document.getElementById("clear-cycle-focus").addEventListener("click", clearCycleFocus);
          return;
        }

        setHtml(
          "cycle-focus-banner",
          `
            <div>
              <strong>Focused cycle: ${escapeHtml(cycle.id)}</strong>
              <div class="resource-meta" id="cycle-focus-meta">
                ${escapeHtml(cycle.type)} | ${escapeHtml(cycle.status)} | pending ${escapeHtml(cycle.pending_count)} | in progress ${escapeHtml(cycle.in_progress_count)} | completed ${escapeHtml(cycle.completed_count)}
              </div>
            </div>
            <button class="inline-button primary" id="clear-cycle-focus" type="button">Clear focus</button>
          `
        );
        document.getElementById("clear-cycle-focus").addEventListener("click", clearCycleFocus);
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
          ? `Workspace: ${data.workspace_name || "default"}`
          : "Workspace not initialized";

        setHtml(
          "workspace-summary",
          [
            `Schema ${escapeHtml(data.schema_version || "unknown")}`,
            data.db_present ? "DB present" : "DB missing",
            `Root ${escapeHtml(data.workspace_root)}`
          ].map((item) => `<span>${item}</span>`).join("")
        );

        setHtml(
          "workspace-notes",
          data.notes?.length
            ? data.notes.map((note) => `<div>${escapeHtml(note)}</div>`).join("")
            : "Current workspace contract is available."
        );

        const activity = data.activity_summary || {};
        setHtml(
          "operations-summary",
          [
            `Active cycles: ${data.counts?.active_cycles ?? 0}`,
            `Pending: ${activity.pending ?? 0}`,
            `In progress: ${activity.in_progress ?? 0}`,
            `Completed: ${activity.completed ?? 0}`,
            `Blocked: ${activity.blocked ?? 0}`
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
          <li class="resource-item">
            <button type="button" data-document-id="${escapeAttribute(item.id)}">
              <div class="resource-title">${escapeHtml(item.title)}</div>
              <div class="resource-meta">${escapeHtml(item.type)} | ${escapeHtml(item.status)} | ${escapeHtml(item.path)} | cycle ${escapeHtml(item.cycle_id || "-")}</div>
            </button>
          </li>
        `).join("");
        list.querySelectorAll("button[data-document-id]").forEach((button) => {
          button.addEventListener("click", () => loadDocument(button.dataset.documentId));
        });
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
          <li class="resource-item">
            <button type="button" data-cycle-id="${escapeAttribute(item.id)}">
              <div class="resource-title">${escapeHtml(item.id)}</div>
              <div class="resource-meta">${escapeHtml(item.type)} | ${escapeHtml(item.status)} | activities ${escapeHtml(item.activity_count)} | pending ${escapeHtml(item.pending_count)} | in progress ${escapeHtml(item.in_progress_count)} | completed ${escapeHtml(item.completed_count)}</div>
            </button>
          </li>
        `).join("");
        list.querySelectorAll("button[data-cycle-id]").forEach((button) => {
          button.addEventListener("click", () => {
            focusCycle(button.dataset.cycleId);
            activateView("cycles-view");
          });
        });
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
        list.innerHTML = filtered.map((item) => `
          <li class="resource-item">
            <button type="button" data-activity-id="${escapeAttribute(item.id)}">
              <div class="resource-title">${escapeHtml(item.title)}</div>
              <div class="resource-meta">${escapeHtml(item.status)} | priority ${escapeHtml(item.priority)} | ${escapeHtml(item.cycle_id)}</div>
            </button>
          </li>
        `).join("");
        list.querySelectorAll("button[data-activity-id]").forEach((button) => {
          button.addEventListener("click", () => loadActivity(button.dataset.activityId));
        });
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

      async function loadDocument(documentId) {
        state.selectedDocumentId = documentId;
        activateView("documents-view");
        const empty = document.getElementById("document-empty");
        const content = document.getElementById("document-content");
        const preview = document.getElementById("document-preview");
        empty.hidden = true;
        content.hidden = false;
        setHtml("document-meta-grid", "");
        setHtml("document-flags", "");
        setHtml("document-actions", "");
        preview.classList.remove("error-state");
        preview.textContent = "Loading document...";
        try {
          const doc = await fetchJson(`/api/documents/${encodeURIComponent(documentId)}`);
          setHtml("document-meta-grid", renderMetaGrid([
            ["Title", doc.title],
            ["Type", doc.type],
            ["Status", doc.status],
            ["Path", doc.path],
            ["Version", doc.version],
            ["Cycle", doc.cycle_id || "-"],
            ["Created", doc.created_at],
            ["Modified", doc.modified_at]
          ]));
          setHtml(
            "document-flags",
            [
              `<span class="badge">${escapeHtml(doc.type)}</span>`,
              `<span class="badge success">${escapeHtml(doc.status)}</span>`,
              doc.cycle_id ? `<span class="badge">cycle ${escapeHtml(doc.cycle_id)}</span>` : "",
              doc.approved_at ? `<span class="badge">${escapeHtml(doc.approved_at)}</span>` : ""
            ].join("")
          );
          setHtml(
            "document-actions",
            doc.cycle_id
              ? `<button class="inline-button primary" type="button" data-focus-cycle-id="${escapeAttribute(doc.cycle_id)}">Focus cycle ${escapeHtml(doc.cycle_id)}</button>`
              : ""
          );
          bindDynamicActions();
          preview.textContent = doc.content_preview || "(empty document)";
        } catch (error) {
          setHtml("document-meta-grid", renderMetaGrid([
            ["Document id", documentId],
            ["State", "Unavailable"]
          ]));
          setHtml("document-flags", '<span class="badge danger">backing file issue</span>');
          setHtml("document-actions", "");
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
        setHtml("cycle-meta-grid", "");
        setHtml("cycle-breakdown", "");
        setHtml("cycle-activities", '<li class="resource-meta">Loading cycle activities...</li>');
        setHtml("cycle-documents", '<li class="resource-meta">Loading related documents...</li>');
        try {
          const [cycle, activities] = await Promise.all([
            fetchJson(`/api/cycles/${encodeURIComponent(cycleId)}`),
            fetchJson(`/api/activities?cycle_id=${encodeURIComponent(cycleId)}`)
          ]);
          const relatedDocuments = state.documents.filter((item) => item.cycle_id === cycleId);
          setHtml("cycle-meta-grid", renderMetaGrid([
            ["Cycle", cycle.id],
            ["Type", cycle.type],
            ["Status", cycle.status],
            ["Start", cycle.start_date],
            ["End", cycle.end_date || "-"],
            ["Created", cycle.created_at]
          ]));
          setHtml(
            "cycle-breakdown",
            [
              `<span class="badge">${escapeHtml(cycle.status)}</span>`,
              `<span class="badge">activities ${escapeHtml(cycle.activity_count)}</span>`,
              `<span class="badge warning">pending ${escapeHtml(cycle.pending_count)}</span>`,
              `<span class="badge">in progress ${escapeHtml(cycle.in_progress_count)}</span>`,
              `<span class="badge success">completed ${escapeHtml(cycle.completed_count)}</span>`,
              cycle.blocked_count ? `<span class="badge danger">blocked ${escapeHtml(cycle.blocked_count)}</span>` : "",
              `<span class="badge">documents ${escapeHtml(relatedDocuments.length)}</span>`
            ].join("")
          );
          const activitiesList = document.getElementById("cycle-activities");
          if (!activities.length) {
            activitiesList.innerHTML = '<li class="empty">No activities linked to this cycle.</li>';
          } else {
            activitiesList.innerHTML = activities.map((item) => `
              <li class="resource-item">
                <button type="button" data-linked-activity-id="${escapeAttribute(item.id)}">
                  <div class="resource-title">${escapeHtml(item.title)}</div>
                  <div class="resource-meta">${escapeHtml(item.status)} | priority ${escapeHtml(item.priority)}</div>
                </button>
              </li>
            `).join("");
            activitiesList.querySelectorAll("button[data-linked-activity-id]").forEach((button) => {
              button.addEventListener("click", () => loadActivity(button.dataset.linkedActivityId));
            });
          }
          const documentsList = document.getElementById("cycle-documents");
          if (!relatedDocuments.length) {
            documentsList.innerHTML = '<li class="empty">No documents currently linked to this cycle.</li>';
          } else {
            documentsList.innerHTML = relatedDocuments.map((item) => `
              <li class="resource-item">
                <button type="button" data-linked-document-id="${escapeAttribute(item.id)}">
                  <div class="resource-title">${escapeHtml(item.title)}</div>
                  <div class="resource-meta">${escapeHtml(item.type)} | ${escapeHtml(item.status)} | ${escapeHtml(item.path)}</div>
                </button>
              </li>
            `).join("");
            documentsList.querySelectorAll("button[data-linked-document-id]").forEach((button) => {
              button.addEventListener("click", () => loadDocument(button.dataset.linkedDocumentId));
            });
          }
          renderAllLists();
        } catch (error) {
          setHtml("cycle-meta-grid", renderMetaGrid([
            ["Cycle", cycleId],
            ["State", "Unavailable"]
          ]));
          setHtml("cycle-breakdown", '<span class="badge danger">cycle load failed</span>');
          setHtml("cycle-activities", `<li class="empty error">${escapeHtml(error.message)}</li>`);
          setHtml("cycle-documents", '<li class="empty">Related documents could not be resolved.</li>');
        }
      }

      async function loadActivity(activityId) {
        state.selectedActivityId = activityId;
        activateView("activities-view");
        const empty = document.getElementById("activity-empty");
        const content = document.getElementById("activity-content");
        empty.hidden = true;
        content.hidden = false;
        setHtml("activity-meta-grid", "");
        setHtml("activity-flags", "");
        setHtml("activity-actions", "");
        try {
          const activity = await fetchJson(`/api/activities/${encodeURIComponent(activityId)}`);
          setHtml("activity-meta-grid", renderMetaGrid([
            ["Title", activity.title],
            ["Status", activity.status],
            ["Priority", String(activity.priority)],
            ["Cycle", activity.cycle_id],
            ["Cycle Type", activity.cycle_type || "-"],
            ["Cycle Start", activity.cycle_start_date || "-"],
            ["Created", activity.created_at],
            ["Type", activity.activity_type || "-"]
          ]));
          setHtml(
            "activity-flags",
            [
              activity.status === "pending" ? '<span class="badge warning">pending</span>' : "",
              activity.status === "in_progress" ? '<span class="badge">in progress</span>' : "",
              activity.status === "completed" ? '<span class="badge success">completed</span>' : "",
              activity.status === "blocked" ? '<span class="badge danger">blocked</span>' : "",
              `<span class="badge">priority ${escapeHtml(activity.priority)}</span>`,
              `<span class="badge">cycle ${escapeHtml(activity.cycle_id)}</span>`
            ].join("")
          );
          setHtml(
            "activity-actions",
            `<button class="inline-button primary" type="button" data-focus-cycle-id="${escapeAttribute(activity.cycle_id)}">Focus cycle ${escapeHtml(activity.cycle_id)}</button>`
          );
          bindDynamicActions();
        } catch (error) {
          setHtml("activity-meta-grid", renderMetaGrid([
            ["Activity", activityId],
            ["State", "Unavailable"]
          ]));
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
        ["entities-list", "documents-list", "cycles-list", "activities-list"].forEach((id) => {
          setHtml(id, '<li class="empty">Workspace is not initialized.</li>');
        });
        setHtml("activities-breakdown", "");
        setHtml("cycle-documents", '<li class="empty">Workspace is not initialized.</li>');
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
        bindTabs();
        bindFilters();
        updateCycleFocusBanner();
        try {
          const status = await fetchJson(api.status);
          renderWorkspaceStatus(status);
          if (!status.is_workspace) {
            setWorkspaceEmptyState();
            return;
          }

          const [entities, documents, cycles, activities] = await Promise.all([
            fetchJson(api.entities),
            fetchJson(api.documents),
            fetchJson(api.cycles),
            fetchJson(api.activities)
          ]);

          state.entities = entities;
          state.documents = documents;
          state.cycles = cycles;
          state.activities = activities;
          populateCycleFilterOptions();
          renderAllLists();
          activateView("cycles-view");

          if (cycles[0]) {
            await loadCycle(cycles[0].id);
          }
          if (activities[0]) {
            await loadActivity(activities[0].id);
          }
          if (documents[0]) {
            await loadDocument(documents[0].id);
          }
          activateView("cycles-view");
        } catch (error) {
          document.getElementById("workspace-badge").textContent = "Cockpit load failed";
          document.getElementById("workspace-notes").innerHTML = `<span class="error">${escapeHtml(error.message)}</span>`;
          setWorkspaceEmptyState();
        }
      }

      bootCockpit();
    </script>
  </body>
</html>
"""
