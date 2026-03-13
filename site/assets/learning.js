function escapeHtml(input) {
  return String(input)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function normalizeSnippet(snippet) {
  if (snippet === null || snippet === undefined) {
    return "";
  }
  // Data can contain literal "\n"; convert to real line breaks for <pre><code>.
  return String(snippet).replace(/\\n/g, "\n");
}

function renderStats(data) {
  const stats = document.getElementById("stats");
  if (!stats) {
    return;
  }

  const totalCheats = Array.isArray(data.cheat_sheets) ? data.cheat_sheets.length : 0;
  const totalRoadmap = Array.isArray(data.roadmap) ? data.roadmap.length : 0;
  const totalServices = Array.isArray(data.recommended_services) ? data.recommended_services.length : 0;

  stats.innerHTML = [
    ["Cheat Items", totalCheats],
    ["Roadmap Stages", totalRoadmap],
    ["Services", totalServices],
    ["Track", data.site || "catalog"],
  ]
    .map(
      ([label, value]) => `
      <div class="stat-card">
        <div class="stat-label">${escapeHtml(label)}</div>
        <div class="stat-value">${escapeHtml(value)}</div>
      </div>
    `,
    )
    .join("");
}

function renderCheatSheet(items) {
  const container = document.getElementById("cheatsheet");
  if (!container || !Array.isArray(items)) {
    return;
  }

  container.innerHTML = items
    .map(
      (item) => `
      <article class="service-card cheat-item">
        <p><span class="tag category">${escapeHtml(item.category || "General")}</span></p>
        <h3>${escapeHtml(item.title || "")}</h3>
        <p>${escapeHtml(item.summary || "")}</p>
        <pre><code>${escapeHtml(normalizeSnippet(item.snippet || ""))}</code></pre>
        <p><strong>Application:</strong> ${escapeHtml(item.application || "")}</p>
        <div class="tags">
          ${(item.tags || []).map((tag) => `<span class="tag">${escapeHtml(tag)}</span>`).join("")}
        </div>
      </article>
    `,
    )
    .join("");
}

function renderRoadmap(items) {
  const container = document.getElementById("roadmap");
  if (!container || !Array.isArray(items)) {
    return;
  }

  container.innerHTML = items
    .map(
      (item) => `
      <article class="timeline-item">
        <h3>${escapeHtml(item.stage || item.phase || "")}</h3>
        <p><strong>Goals:</strong> ${escapeHtml((item.goals || item.focus || []).join(", "))}</p>
        <p><strong>Build:</strong> ${escapeHtml((item.build || item.practice_with || []).join(", "))}</p>
        <p><strong>Tools:</strong> ${escapeHtml((item.tools || []).join(", "))}</p>
        ${
          item.example_path
            ? `<p><strong>Example code:</strong> <code>${escapeHtml(item.example_path)}</code></p>`
            : ""
        }
      </article>
    `,
    )
    .join("");
}

function renderServices(services) {
  const container = document.getElementById("services");
  if (!container || !Array.isArray(services)) {
    return;
  }

  container.innerHTML = services
    .map(
      (service) => `
      <article class="service-card">
        <h3>${escapeHtml(service.name || "")}</h3>
        <p><span class="level ${escapeHtml(service.level || "basic")}">${escapeHtml(service.level || "basic")}</span></p>
        <p><strong>Path:</strong> ${escapeHtml(service.path || "")}</p>
        <p><strong>Entrypoint:</strong> ${escapeHtml(service.entrypoint || "(none)")}</p>
        <p><strong>Topics:</strong> ${escapeHtml((service.topics || []).join(", "))}</p>
        <div class="tags">
          ${(service.tech_stack || []).map((tech) => `<span class="tag">${escapeHtml(tech)}</span>`).join("")}
        </div>
      </article>
    `,
    )
    .join("");
}

function renderStackMap(items) {
  const container = document.getElementById("stackmap");
  const panel = document.getElementById("mapPanel");
  if (!panel || !container) {
    return;
  }

  if (!Array.isArray(items) || items.length === 0) {
    panel.style.display = "none";
    return;
  }

  container.innerHTML = items
    .map(
      (row) => `
      <article class="service-card">
        <h3>${escapeHtml(row.domain || "")}</h3>
        <p><strong>Java:</strong> ${escapeHtml(row.java_stack || "")}</p>
        <p><strong>Python:</strong> ${escapeHtml(row.python_stack || "")}</p>
        <p><strong>Use when:</strong> ${escapeHtml(row.when || "")}</p>
      </article>
    `,
    )
    .join("");
}

function renderCapstones(items) {
  const container = document.getElementById("capstones");
  const panel = document.getElementById("capstonePanel");
  if (!panel || !container) {
    return;
  }

  if (!Array.isArray(items) || items.length === 0) {
    panel.style.display = "none";
    return;
  }

  container.innerHTML = items
    .map(
      (item) => `
      <article class="service-card">
        <h3>${escapeHtml(item.name || "")}</h3>
        <p><strong>Scope:</strong> ${escapeHtml(item.scope || "")}</p>
        <div class="tags">
          ${(item.stack || []).map((s) => `<span class="tag">${escapeHtml(s)}</span>`).join("")}
        </div>
      </article>
    `,
    )
    .join("");
}

function renderOpenSourceStacks(items) {
  const container = document.getElementById("oss");
  const panel = document.getElementById("ossPanel");
  if (!panel || !container) {
    return;
  }

  if (!Array.isArray(items) || items.length === 0) {
    panel.style.display = "none";
    return;
  }

  container.innerHTML = items
    .map(
      (item) => `
      <article class="service-card">
        <h3>${escapeHtml(item.name || "")}</h3>
        <p><strong>Use case:</strong> ${escapeHtml(item.use_case || "")}</p>
        <div class="tags">
          ${(item.packages || []).map((pkg) => `<span class="tag">${escapeHtml(pkg)}</span>`).join("")}
        </div>
      </article>
    `,
    )
    .join("");
}

async function initLearningSite() {
  const source = document.body.dataset.source;
  if (!source) {
    return;
  }

  const response = await fetch(source);
  const data = await response.json();

  const title = document.getElementById("title");
  const subtitle = document.getElementById("subtitle");

  if (title) {
    title.textContent = data.title || title.textContent;
  }
  if (subtitle) {
    const root = data.example_root ? ` Example root: ${data.example_root}` : "";
    subtitle.textContent = `${data.subtitle || ""}${root}`;
  }

  renderStats(data);
  renderCheatSheet(data.cheat_sheets || []);
  renderRoadmap(data.roadmap || []);
  renderStackMap(data.java_python_map || []);
  renderOpenSourceStacks(data.open_source_stacks || []);
  renderCapstones(data.capstone_projects || []);
  renderServices(data.recommended_services || []);

  const generatedAt = new Date(data.generated_at).toLocaleString();
  const generatedNode = document.getElementById("generatedAt");
  if (generatedNode) {
    generatedNode.textContent = `Track data generated at ${generatedAt}`;
  }
}

initLearningSite().catch((error) => {
  const generatedNode = document.getElementById("generatedAt");
  if (generatedNode) {
    generatedNode.textContent = `Failed to load track data: ${error}`;
  }
});
