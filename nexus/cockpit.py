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
        --bg: #f3f5f7;
        --panel: #ffffff;
        --border: #d9e0e7;
        --text: #1d2733;
        --muted: #5d6b79;
        --accent: #1e5eff;
        --accent-soft: #e8efff;
      }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        font-family: "Segoe UI", system-ui, sans-serif;
        background: linear-gradient(180deg, #eef3f8 0%, #f7f9fb 100%);
        color: var(--text);
      }
      main {
        max-width: 1200px;
        margin: 0 auto;
        padding: 24px;
      }
      .hero {
        display: flex;
        justify-content: space-between;
        gap: 16px;
        align-items: end;
        margin-bottom: 20px;
      }
      h1, h2, h3, p { margin: 0; }
      .subtitle {
        color: var(--muted);
        margin-top: 6px;
      }
      .panel {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0 10px 30px rgba(25, 40, 60, 0.06);
      }
      .grid {
        display: grid;
        gap: 16px;
      }
      .stats-grid {
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        margin-bottom: 20px;
      }
      .stat-card {
        background: var(--accent-soft);
        border-radius: 14px;
        padding: 14px;
        border: 1px solid #d7e3ff;
      }
      .stat-card strong {
        display: block;
        font-size: 1.8rem;
        margin-top: 6px;
      }
      .two-column {
        grid-template-columns: minmax(0, 1.3fr) minmax(320px, 0.9fr);
        align-items: start;
      }
      .stack {
        display: grid;
        gap: 16px;
      }
      .resource-list, .detail-list {
        list-style: none;
        padding: 0;
        margin: 12px 0 0;
        display: grid;
        gap: 10px;
      }
      .resource-item {
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 12px;
        background: #fbfcfd;
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
      .resource-meta, .label {
        color: var(--muted);
        font-size: 0.92rem;
      }
      .status-line {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-top: 10px;
        color: var(--muted);
        font-size: 0.92rem;
      }
      .detail-preview {
        margin-top: 14px;
        padding: 12px;
        border-radius: 12px;
        background: #0f1720;
        color: #f7fbff;
        white-space: pre-wrap;
        font-family: "Cascadia Code", "Consolas", monospace;
        font-size: 0.9rem;
        min-height: 180px;
      }
      .inline-note {
        margin-top: 10px;
        color: var(--muted);
        font-size: 0.92rem;
      }
      .error {
        color: #b00020;
      }
      @media (max-width: 900px) {
        .hero { align-items: start; flex-direction: column; }
        .two-column { grid-template-columns: 1fr; }
      }
    </style>
  </head>
  <body>
    <main>
      <section class="hero">
        <div>
          <h1>Nexus Cockpit</h1>
          <p class="subtitle">Read-only local supervision over the current workspace and API.</p>
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
            <div class="status-line" id="workspace-summary"></div>
            <div class="inline-note" id="workspace-notes"></div>
          </article>

          <article class="panel">
            <h2>Operational Summary</h2>
            <div class="status-line" id="operations-summary"></div>
          </article>

          <article class="panel">
            <h2>Entities</h2>
            <ul class="resource-list" id="entities-list">
              <li class="resource-meta">Loading entities...</li>
            </ul>
          </article>

          <article class="panel">
            <h2>Documents</h2>
            <ul class="resource-list" id="documents-list">
              <li class="resource-meta">Loading documents...</li>
            </ul>
          </article>
        </div>

        <aside class="stack">
          <article class="panel">
            <h2>Document Inspection</h2>
            <div id="document-detail">
              <p class="resource-meta">Select a document to inspect its metadata and Markdown preview.</p>
            </div>
          </article>
        </aside>
      </section>
    </main>

    <script>
      const api = {
        status: "/api/system/status",
        entities: "/api/entities",
        documents: "/api/documents"
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

      function renderWorkspaceStatus(data) {
        setText("count-entities", String(data.counts?.entities ?? 0));
        setText("count-documents", String(data.counts?.documents ?? 0));
        setText("count-relations", String(data.counts?.relations ?? 0));
        setText("count-cycles", String(data.counts?.cycles ?? 0));
        setText("count-activities", String(data.counts?.activities ?? 0));

        const badge = document.getElementById("workspace-badge");
        badge.textContent = data.is_workspace
          ? `Workspace: ${data.workspace_name || "default"}`
          : "Workspace not initialized";

        const summary = document.getElementById("workspace-summary");
        summary.innerHTML = [
          `Schema ${data.schema_version || "unknown"}`,
          data.db_present ? "DB present" : "DB missing",
          `Root ${data.workspace_root}`
        ].map((item) => `<span>${item}</span>`).join("");

        const notes = document.getElementById("workspace-notes");
        notes.innerHTML = "";
        if (data.notes?.length) {
          notes.innerHTML = data.notes.map((note) => `<div>${note}</div>`).join("");
        }

        const operations = document.getElementById("operations-summary");
        const activity = data.activity_summary || {};
        operations.innerHTML = [
          `Active cycles: ${data.counts?.active_cycles ?? 0}`,
          `Pending: ${activity.pending ?? 0}`,
          `In progress: ${activity.in_progress ?? 0}`,
          `Completed: ${activity.completed ?? 0}`,
          `Blocked: ${activity.blocked ?? 0}`
        ].map((item) => `<span>${item}</span>`).join("");
      }

      function renderEntities(data) {
        const list = document.getElementById("entities-list");
        if (!data.length) {
          list.innerHTML = '<li class="resource-meta">No entities found.</li>';
          return;
        }
        list.innerHTML = data.map((item) => `
          <li class="resource-item">
            <div class="resource-title">${escapeHtml(item.name)}</div>
            <div class="resource-meta">${escapeHtml(item.type)} | ${escapeHtml(item.context || "-")}</div>
          </li>
        `).join("");
      }

      function renderDocuments(data) {
        const list = document.getElementById("documents-list");
        if (!data.length) {
          list.innerHTML = '<li class="resource-meta">No documents found.</li>';
          return;
        }
        list.innerHTML = data.map((item) => `
          <li class="resource-item">
            <button type="button" data-document-id="${escapeAttribute(item.id)}">
              <div class="resource-title">${escapeHtml(item.title)}</div>
              <div class="resource-meta">${escapeHtml(item.type)} | ${escapeHtml(item.status)} | ${escapeHtml(item.path)}</div>
            </button>
          </li>
        `).join("");
        list.querySelectorAll("button[data-document-id]").forEach((button) => {
          button.addEventListener("click", () => loadDocument(button.dataset.documentId));
        });
      }

      async function loadDocument(documentId) {
        const detail = document.getElementById("document-detail");
        detail.innerHTML = '<p class="resource-meta">Loading document...</p>';
        try {
          const doc = await fetchJson(`/api/documents/${encodeURIComponent(documentId)}`);
          detail.innerHTML = `
            <h3>${escapeHtml(doc.title)}</h3>
            <ul class="detail-list">
              <li><strong>ID:</strong> ${escapeHtml(doc.id)}</li>
              <li><strong>Type:</strong> ${escapeHtml(doc.type)}</li>
              <li><strong>Status:</strong> ${escapeHtml(doc.status)}</li>
              <li><strong>Path:</strong> ${escapeHtml(doc.path)}</li>
              <li><strong>Version:</strong> ${escapeHtml(doc.version)}</li>
              <li><strong>Cycle:</strong> ${escapeHtml(doc.cycle_id || "-")}</li>
            </ul>
            <div class="detail-preview">${escapeHtml(doc.content_preview)}</div>
          `;
        } catch (error) {
          detail.innerHTML = `<p class="error">${escapeHtml(error.message)}</p>`;
        }
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
        try {
          const [status, entities, documents] = await Promise.all([
            fetchJson(api.status),
            fetchJson(api.entities),
            fetchJson(api.documents)
          ]);
          renderWorkspaceStatus(status);
          renderEntities(entities);
          renderDocuments(documents);
          if (documents[0]) {
            loadDocument(documents[0].id);
          }
        } catch (error) {
          document.getElementById("workspace-badge").textContent = "Cockpit load failed";
          document.getElementById("workspace-notes").innerHTML = `<span class="error">${escapeHtml(error.message)}</span>`;
        }
      }

      bootCockpit();
    </script>
  </body>
</html>
"""
