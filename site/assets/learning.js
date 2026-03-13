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
  return String(snippet).replace(/\\n/g, "\n");
}

function getProgressKey(track, itemName) {
  return `learning_progress:${track}:${itemName}`;
}

function isCompleted(track, itemName) {
  return localStorage.getItem(getProgressKey(track, itemName)) === "1";
}

function setCompleted(track, itemName, completed) {
  localStorage.setItem(getProgressKey(track, itemName), completed ? "1" : "0");
}

function renderStats(data) {
  const stats = document.getElementById("stats");
  if (!stats) {
    return;
  }

  const totalCheats = Array.isArray(data.cheat_sheets) ? data.cheat_sheets.length : 0;
  const totalRoadmap = Array.isArray(data.roadmap) ? data.roadmap.length : 0;
  const totalServices = Array.isArray(data.recommended_services) ? data.recommended_services.length : 0;
  const totalDone = Array.isArray(data.roadmap)
    ? data.roadmap.filter((item) => isCompleted(data.site || "track", item.stage || item.phase || "")).length
    : 0;

  stats.innerHTML = [
    ["Cheat Items", totalCheats],
    ["Roadmap Stages", totalRoadmap],
    ["Completed", `${totalDone}/${totalRoadmap}`],
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

function bindRoadmapActions(track, data) {
  const checkboxes = document.querySelectorAll(".progress-toggle");
  checkboxes.forEach((checkbox) => {
    checkbox.addEventListener("change", () => {
      const itemName = checkbox.dataset.item || "";
      setCompleted(track, itemName, checkbox.checked);
      renderStats(data);
    });
  });

  const runButtons = document.querySelectorAll(".run-example-btn");
  runButtons.forEach((button) => {
    button.addEventListener("click", async () => {
      const exampleFile = button.dataset.exampleFile || "";
      if (!exampleFile) {
        return;
      }

      const output = document.getElementById("runnerOutput");
      if (output) {
        output.textContent = `Running: ${exampleFile} ...`;
      }

      try {
        const response = await fetch("/api/run-example", {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({ example_file: exampleFile }),
        });
        const payload = await response.json();

        const lines = [
          `ok: ${payload.ok}`,
          payload.command ? `command: ${payload.command}` : "",
          payload.error ? `error: ${payload.error}` : "",
          payload.stdout ? `\nstdout:\n${payload.stdout}` : "",
          payload.stderr ? `\nstderr:\n${payload.stderr}` : "",
        ].filter(Boolean);

        if (output) {
          output.textContent = lines.join("\n");
        }
      } catch (error) {
        if (output) {
          output.textContent = `Runner request failed: ${error}`;
        }
      }
    });
  });
}

function renderRoadmap(items, track, data) {
  const container = document.getElementById("roadmap");
  if (!container || !Array.isArray(items)) {
    return;
  }

  container.innerHTML = items
    .map((item, index) => {
      const itemName = item.stage || item.phase || `item-${index}`;
      const checked = isCompleted(track, itemName) ? "checked" : "";
      const runButton = item.example_file
        ? `<button class="run-example-btn" data-example-file="${escapeHtml(item.example_file)}">Run example</button>`
        : "";

      return `
      <article class="timeline-item">
        <h3>${escapeHtml(itemName)}</h3>
        <p><strong>Goals:</strong> ${escapeHtml((item.goals || item.focus || []).join(", "))}</p>
        <p><strong>Build:</strong> ${escapeHtml((item.build || item.practice_with || []).join(", "))}</p>
        <p><strong>Tools:</strong> ${escapeHtml((item.tools || []).join(", "))}</p>
        ${item.example_path ? `<p><strong>Example code:</strong> <code>${escapeHtml(item.example_path)}</code></p>` : ""}
        <div class="roadmap-actions">
          <label>
            <input type="checkbox" class="progress-toggle" data-item="${escapeHtml(itemName)}" ${checked} />
            Mark completed
          </label>
          ${runButton}
        </div>
      </article>
    `;
    })
    .join("");

  bindRoadmapActions(track, data);
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

function renderMiniProjects(items) {
  const container = document.getElementById("miniProjects");
  if (!container) {
    return;
  }

  if (!Array.isArray(items) || items.length === 0) {
    container.innerHTML = "";
    return;
  }

  container.innerHTML = items
    .map(
      (item) => `
      <article class="service-card">
        <h3>${escapeHtml(item.name || "")}</h3>
        <p><strong>Path:</strong> <code>${escapeHtml(item.path || "")}</code></p>
        <p><strong>Focus:</strong> ${escapeHtml(item.focus || "")}</p>
        <div class="tags">
          ${(item.stack || []).map((tech) => `<span class="tag">${escapeHtml(tech)}</span>`).join("")}
        </div>
      </article>
    `,
    )
    .join("");
}

function renderArchitectureDiagrams(items) {
  const container = document.getElementById("diagrams");
  const panel = document.getElementById("diagramPanel");
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
      <article class="service-card diagram-card">
        <h3>${escapeHtml(item.title || "")}</h3>
        <img src="${escapeHtml(item.file || "")}" alt="${escapeHtml(item.title || "diagram")}" />
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
  const track = data.site || "track";

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
  renderRoadmap(data.roadmap || [], track, data);
  renderStackMap(data.java_python_map || []);
  renderArchitectureDiagrams(data.architecture_diagrams || []);
  renderOpenSourceStacks(data.open_source_stacks || []);
  renderMiniProjects(data.mini_projects || []);
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
