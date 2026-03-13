const CHEAT_SHEET = [
  {
    title: "Variables",
    note: "Store values and keep naming readable.",
    code: `name = "Alice"\nage = 25\nis_active = True`,
  },
  {
    title: "Functions",
    note: "Wrap reusable logic and return explicit values.",
    code: `def add(a, b):\n    return a + b`,
  },
  {
    title: "Docstrings",
    note: "Document purpose, inputs, and outputs.",
    code: `def fetch_data(url):\n    \"\"\"Fetch JSON from a URL and return dict.\"\"\"\n    ...`,
  },
  {
    title: "Comments",
    note: "Explain intent, not obvious syntax.",
    code: `# Retry once because provider rate limits can spike\nresponse = client.get(payload)`,
  },
  {
    title: "Imports",
    note: "Use standard library first, then external modules.",
    code: `import json\nfrom pathlib import Path\nfrom datetime import datetime`,
  },
  {
    title: "Error Handling",
    note: "Catch known failures and keep logs useful.",
    code: `try:\n    data = api_call()\nexcept TimeoutError as exc:\n    logger.error("api timeout: %s", exc)`,
  },
];

function renderCheatSheet() {
  const container = document.getElementById("cheatsheet");
  container.innerHTML = CHEAT_SHEET.map(
    (item) => `
      <article class="cheat-item">
        <h3>${item.title}</h3>
        <p>${item.note}</p>
        <pre><code>${item.code.replace(/</g, "&lt;")}</code></pre>
      </article>
    `,
  ).join("");
}

function renderStats(overview) {
  const stats = document.getElementById("stats");
  const items = [
    ["Services", overview.service_count],
    ["Basic", overview.basic_count],
    ["Intermediate", overview.intermediate_count],
    ["Advanced", overview.advanced_count],
  ];

  stats.innerHTML = items
    .map(
      ([label, value]) => `
      <div class="stat-card">
        <div class="stat-label">${label}</div>
        <div class="stat-value">${value}</div>
      </div>
    `,
    )
    .join("");
}

function renderRoadmap(roadmap) {
  const container = document.getElementById("roadmap");
  container.innerHTML = roadmap
    .map(
      (item) => `
      <article class="timeline-item">
        <h3>${item.phase}</h3>
        <p><strong>Focus:</strong> ${item.focus.join(", ")}</p>
        <p><strong>Practice with:</strong> ${item.practice_with.join(", ")}</p>
      </article>
    `,
    )
    .join("");
}

function renderServices(services) {
  const container = document.getElementById("services");
  container.innerHTML = services
    .map(
      (service) => `
      <article class="service-card">
        <h3>${service.name}</h3>
        <p><span class="level ${service.level}">${service.level}</span></p>
        <p><strong>Path:</strong> ${service.path}</p>
        <p><strong>Entrypoint:</strong> ${service.entrypoint || "(none)"}</p>
        <p><strong>Python files:</strong> ${service.python_files}</p>
        <p><strong>Topics:</strong> ${service.topics.join(", ")}</p>
        <div class="tags">
          ${service.tech_stack.map((tech) => `<span class="tag">${tech}</span>`).join("")}
        </div>
      </article>
    `,
    )
    .join("");
}

async function init() {
  renderCheatSheet();

  const response = await fetch("data/catalog.json");
  const data = await response.json();

  renderStats(data.overview);
  renderRoadmap(data.roadmap);
  renderServices(data.services);

  const generatedAt = new Date(data.generated_at).toLocaleString();
  document.getElementById("generatedAt").textContent = `Catalog generated at ${generatedAt}`;
}

init().catch((error) => {
  document.getElementById("generatedAt").textContent = `Failed to load catalog: ${error}`;
});
