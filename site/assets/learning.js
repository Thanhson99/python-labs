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

function getGlobalLocaleKey() {
  return "python_labs_locale";
}

function isCompleted(track, itemName) {
  return localStorage.getItem(getProgressKey(track, itemName)) === "1";
}

function setCompleted(track, itemName, completed) {
  localStorage.setItem(getProgressKey(track, itemName), completed ? "1" : "0");
}

function isLocalizedMap(value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    return false;
  }
  const keys = Object.keys(value);
  return keys.includes("en") || keys.includes("vi");
}

function resolveLocalizedValue(value, locale, fallbackLocale = "en") {
  if (isLocalizedMap(value)) {
    return value[locale] ?? value[fallbackLocale] ?? Object.values(value)[0] ?? "";
  }
  return value;
}

function getNestedValue(source, path, fallback = "") {
  let current = source;
  for (const part of path) {
    if (!current || typeof current !== "object" || !(part in current)) {
      return fallback;
    }
    current = current[part];
  }
  return current;
}

function isLocalRunnerHost() {
  return ["localhost", "127.0.0.1"].includes(window.location.hostname);
}

function getSelectedLocale(data) {
  const defaultLocale = data.default_locale || "en";
  const saved = window.PythonLabsI18n?.getLocale?.() || localStorage.getItem(getGlobalLocaleKey());
  const supported = Array.isArray(data.supported_locales) ? data.supported_locales : ["en"];
  return supported.includes(saved) ? saved : defaultLocale;
}

function setSelectedLocale(locale) {
  if (window.PythonLabsI18n?.setLocale) {
    window.PythonLabsI18n.setLocale(locale);
    return;
  }
  localStorage.setItem(getGlobalLocaleKey(), locale);
}

const LEARNING_STATIC_TRANSLATIONS = {
  advanced: {
    vi: {
      title: "Lộ trình Kiến Trúc Python Nâng Cao",
      subtitle: "Lộ trình production: microservice, queue, stream, reliability và platform engineering.",
      ui: {
        hero: {
          eyebrow: "Python Labs",
          back_to_tracks: "Quay lại trang chọn lộ trình",
          example_root: "Thư mục ví dụ",
          static_note: "Chế độ static: GitHub Pages có thể duyệt lộ trình và ví dụ mà không cần API chạy Python.",
          local_runner_enabled: "Có thể chạy ví dụ trực tiếp khi mở site bằng localhost.",
        },
        sections: {
          cheat_sheets: "Thư viện Cheat Sheet Nâng Cao",
          roadmap: "Lộ trình Kiến Trúc",
          java_python_map: "Bản đồ Stack Java sang Python",
          architecture_diagrams: "Sơ đồ Kiến Trúc",
          mini_projects: "Mini Project",
          extra_examples: "Thư viện Pattern Mở rộng",
          open_source_stacks: "Stack Tích hợp Mã nguồn mở",
          capstone_projects: "Ứng dụng Capstone",
          recommended_services: "Service Nên Tham Khảo",
        },
        stats: {
          cheat_items: "Mục Cheat Sheet",
          roadmap_stages: "Chặng học",
          completed: "Hoàn thành",
          track: "Lộ trình",
        },
        fields: {
          application: "Ứng dụng",
          goals: "Mục tiêu",
          build: "Nên làm",
          tools: "Công cụ",
          example_code: "Mã ví dụ",
          path: "Đường dẫn",
          focus: "Trọng tâm",
          entrypoint: "Điểm vào",
          topics: "Chủ đề",
          use_case: "Tình huống dùng",
          java: "Java",
          python: "Python",
          when: "Dùng khi",
          scope: "Phạm vi",
        },
        roadmap: {
          mark_completed: "Đánh dấu hoàn thành",
          run_example: "Chạy ví dụ",
          run_file: "Chạy file",
        },
        runner: {
          heading: "Kết quả chạy ví dụ",
          placeholder: 'Chọn một mục trong lộ trình rồi bấm "Chạy ví dụ".',
          disabled: "Đang ở chế độ static. Hãy chạy ví dụ cục bộ từ repository nếu cần thực thi trực tiếp.",
          running: "Đang chạy",
          request_failed: "Gọi runner thất bại",
        },
        footer: { generated_at: "Dữ liệu lộ trình được tạo lúc" },
        common: { general: "Tổng quát", none: "(không có)" },
      },
    },
  },
};

function buildRuntimeData(data, locale) {
  const fallbackLocale = data.default_locale || "en";
  const localized = getNestedValue(data, ["locales", locale], {});
  const fallback = getNestedValue(data, ["locales", fallbackLocale], {});
  const staticLocale = getNestedValue(LEARNING_STATIC_TRANSLATIONS, [data.site || "track", locale], {});

  const pick = (key, defaultValue) => localized[key] ?? staticLocale[key] ?? fallback[key] ?? defaultValue;

  return {
    site: data.site || "track",
    locale,
    ui: pick("ui", {}),
    title: pick("title", resolveLocalizedValue(data.title, locale, fallbackLocale) || ""),
    subtitle: pick("subtitle", resolveLocalizedValue(data.subtitle, locale, fallbackLocale) || ""),
    example_root: data.example_root || "",
    cheat_sheets: pick("cheat_sheets", data.cheat_sheets || []),
    roadmap: pick("roadmap", data.roadmap || []),
    open_source_stacks: pick("open_source_stacks", data.open_source_stacks || []),
    mini_projects: pick("mini_projects", data.mini_projects || []),
    extra_examples: pick("extra_examples", data.extra_examples || []),
    database_practicals: pick("database_practicals", data.database_practicals || []),
    recommended_services: pick("recommended_services", data.recommended_services || []),
    java_python_map: pick("java_python_map", data.java_python_map || []),
    architecture_diagrams: pick("architecture_diagrams", data.architecture_diagrams || []),
    capstone_projects: pick("capstone_projects", data.capstone_projects || []),
  };
}

function getUiText(ui, path, fallback) {
  const value = getNestedValue(ui, path, fallback);
  return value === undefined || value === null || value === "" ? fallback : value;
}

function applyLanguageButtons(locale) {
  if (window.PythonLabsI18n?.applyButtons) {
    window.PythonLabsI18n.applyButtons(locale);
    return;
  }
  const buttons = document.querySelectorAll(".lang-btn");
  buttons.forEach((button) => {
    button.classList.toggle("active", button.dataset.lang === locale);
  });
}

function applyStaticText(runtimeData, supportsRunner) {
  const ui = runtimeData.ui || {};

  const setText = (id, text) => {
    const node = document.getElementById(id);
    if (node && text) {
      node.textContent = text;
    }
  };

  setText("eyebrow", getUiText(ui, ["hero", "eyebrow"], "Python Labs"));
  setText("backButton", getUiText(ui, ["hero", "back_to_tracks"], "Back to track selection"));
  setText("sectionCheatSheet", getUiText(ui, ["sections", "cheat_sheets"], "Cheat Sheet Library"));
  setText("sectionRoadmap", getUiText(ui, ["sections", "roadmap"], "Roadmap"));
  setText("sectionMiniProjects", getUiText(ui, ["sections", "mini_projects"], "Mini Projects"));
  setText("sectionDatabase", getUiText(ui, ["sections", "database_practicals"], "Database Practicals"));
  setText("sectionExtraExamples", getUiText(ui, ["sections", "extra_examples"], "Extra Example Library"));
  setText("sectionOpenSource", getUiText(ui, ["sections", "open_source_stacks"], "Open-Source Integration Stacks"));
  setText("sectionMap", getUiText(ui, ["sections", "java_python_map"], "Java to Python Stack Mapping"));
  setText("sectionDiagrams", getUiText(ui, ["sections", "architecture_diagrams"], "Architecture Diagrams"));
  setText("sectionCapstones", getUiText(ui, ["sections", "capstone_projects"], "Capstone Applications"));
  setText("sectionServices", getUiText(ui, ["sections", "recommended_services"], "Recommended Services"));
  setText("runnerHeading", getUiText(ui, ["runner", "heading"], "Example Runner Output"));

  const title = document.getElementById("title");
  const subtitle = document.getElementById("subtitle");
  const staticNote = document.getElementById("staticNote");
  const runnerOutput = document.getElementById("runnerOutput");

  if (title) {
    title.textContent = runtimeData.title || title.textContent;
  }

  if (subtitle) {
    const rootLabel = getUiText(ui, ["hero", "example_root"], "Example root");
    const root = runtimeData.example_root ? ` ${rootLabel}: ${runtimeData.example_root}` : "";
    subtitle.textContent = `${runtimeData.subtitle || ""}${root}`;
  }

  if (staticNote) {
    staticNote.textContent = supportsRunner
      ? getUiText(ui, ["hero", "local_runner_enabled"], "Local runner is available on localhost.")
      : getUiText(
          ui,
          ["hero", "static_note"],
          "Static hosting mode: GitHub Pages can browse the roadmap and examples without the Python runner API.",
        );
  }

  if (runnerOutput) {
    runnerOutput.textContent = supportsRunner
      ? getUiText(ui, ["runner", "placeholder"], 'Select a roadmap item and click "Run example".')
      : getUiText(
          ui,
          ["runner", "disabled"],
          "Static hosting mode detected. Run examples locally from the repository for live execution.",
        );
  }
}

function renderStats(runtimeData) {
  const stats = document.getElementById("stats");
  if (!stats) {
    return;
  }

  const ui = runtimeData.ui || {};
  const totalCheats = Array.isArray(runtimeData.cheat_sheets) ? runtimeData.cheat_sheets.length : 0;
  const totalRoadmap = Array.isArray(runtimeData.roadmap) ? runtimeData.roadmap.length : 0;
  const totalDone = Array.isArray(runtimeData.roadmap)
    ? runtimeData.roadmap.filter((item) => isCompleted(runtimeData.site, item.stage || item.phase || "")).length
    : 0;

  stats.innerHTML = [
    [getUiText(ui, ["stats", "cheat_items"], "Cheat Items"), totalCheats],
    [getUiText(ui, ["stats", "roadmap_stages"], "Roadmap Stages"), totalRoadmap],
    [getUiText(ui, ["stats", "completed"], "Completed"), `${totalDone}/${totalRoadmap}`],
    [getUiText(ui, ["stats", "track"], "Track"), runtimeData.site || "catalog"],
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

function renderCheatSheet(items, ui) {
  const container = document.getElementById("cheatsheet");
  if (!container || !Array.isArray(items)) {
    return;
  }

  const categoryFallback = getUiText(ui, ["common", "general"], "General");
  const applicationLabel = getUiText(ui, ["fields", "application"], "Application");

  container.innerHTML = items
    .map(
      (item) => `
      <article class="service-card cheat-item">
        <p><span class="tag category">${escapeHtml(item.category || categoryFallback)}</span></p>
        <h3>${escapeHtml(item.title || "")}</h3>
        <p>${escapeHtml(item.summary || "")}</p>
        <pre><code>${escapeHtml(normalizeSnippet(item.snippet || ""))}</code></pre>
        <p><strong>${escapeHtml(applicationLabel)}:</strong> ${escapeHtml(item.application || "")}</p>
        <div class="tags">
          ${(item.tags || []).map((tag) => `<span class="tag">${escapeHtml(tag)}</span>`).join("")}
        </div>
      </article>
    `,
    )
    .join("");
}

function bindRoadmapActions(track, runtimeData) {
  const checkboxes = document.querySelectorAll(".progress-toggle");
  checkboxes.forEach((checkbox) => {
    checkbox.addEventListener("change", () => {
      const itemName = checkbox.dataset.item || "";
      setCompleted(track, itemName, checkbox.checked);
      renderStats(runtimeData);
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
        output.textContent = `${getUiText(runtimeData.ui, ["runner", "running"], "Running")}: ${exampleFile} ...`;
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
          output.textContent = `${getUiText(runtimeData.ui, ["runner", "request_failed"], "Runner request failed")}: ${error}`;
        }
      }
    });
  });
}

function renderRoadmap(items, runtimeData, supportsRunner) {
  const container = document.getElementById("roadmap");
  if (!container || !Array.isArray(items)) {
    return;
  }

  const ui = runtimeData.ui || {};
  const goalsLabel = getUiText(ui, ["fields", "goals"], "Goals");
  const buildLabel = getUiText(ui, ["fields", "build"], "Build");
  const toolsLabel = getUiText(ui, ["fields", "tools"], "Tools");
  const exampleCodeLabel = getUiText(ui, ["fields", "example_code"], "Example code");
  const markCompletedLabel = getUiText(ui, ["roadmap", "mark_completed"], "Mark completed");
  const runExampleLabel = getUiText(ui, ["roadmap", "run_example"], "Run example");

  container.innerHTML = items
    .map((item, index) => {
      const itemName = item.stage || item.phase || `item-${index}`;
      const checked = isCompleted(runtimeData.site, itemName) ? "checked" : "";
      const runButton =
        supportsRunner && item.example_file
          ? `<button class="run-example-btn" data-example-file="${escapeHtml(item.example_file)}">${escapeHtml(runExampleLabel)}</button>`
          : "";

      return `
      <article class="timeline-item">
        <h3>${escapeHtml(itemName)}</h3>
        <p><strong>${escapeHtml(goalsLabel)}:</strong> ${escapeHtml((item.goals || item.focus || []).join(", "))}</p>
        <p><strong>${escapeHtml(buildLabel)}:</strong> ${escapeHtml((item.build || item.practice_with || []).join(", "))}</p>
        <p><strong>${escapeHtml(toolsLabel)}:</strong> ${escapeHtml((item.tools || []).join(", "))}</p>
        ${item.example_path ? `<p><strong>${escapeHtml(exampleCodeLabel)}:</strong> <code>${escapeHtml(item.example_path)}</code></p>` : ""}
        <div class="roadmap-actions">
          <label>
            <input type="checkbox" class="progress-toggle" data-item="${escapeHtml(itemName)}" ${checked} />
            ${escapeHtml(markCompletedLabel)}
          </label>
          ${runButton}
        </div>
      </article>
    `;
    })
    .join("");
}

function renderServices(services, ui) {
  const container = document.getElementById("services");
  if (!container || !Array.isArray(services)) {
    return;
  }

  const pathLabel = getUiText(ui, ["fields", "path"], "Path");
  const entrypointLabel = getUiText(ui, ["fields", "entrypoint"], "Entrypoint");
  const topicsLabel = getUiText(ui, ["fields", "topics"], "Topics");
  const noneLabel = getUiText(ui, ["common", "none"], "(none)");

  container.innerHTML = services
    .map(
      (service) => `
      <article class="service-card">
        <h3>${escapeHtml(service.name || "")}</h3>
        <p><span class="level ${escapeHtml(service.level || "basic")}">${escapeHtml(service.level || "basic")}</span></p>
        <p><strong>${escapeHtml(pathLabel)}:</strong> ${escapeHtml(service.path || "")}</p>
        <p><strong>${escapeHtml(entrypointLabel)}:</strong> ${escapeHtml(service.entrypoint || noneLabel)}</p>
        <p><strong>${escapeHtml(topicsLabel)}:</strong> ${escapeHtml((service.topics || []).join(", "))}</p>
        <div class="tags">
          ${(service.tech_stack || []).map((tech) => `<span class="tag">${escapeHtml(tech)}</span>`).join("")}
        </div>
      </article>
    `,
    )
    .join("");
}

function renderStackMap(items, ui) {
  const container = document.getElementById("stackmap");
  const panel = document.getElementById("mapPanel");
  if (!panel || !container) {
    return;
  }

  if (!Array.isArray(items) || items.length === 0) {
    panel.style.display = "none";
    return;
  }

  const javaLabel = getUiText(ui, ["fields", "java"], "Java");
  const pythonLabel = getUiText(ui, ["fields", "python"], "Python");
  const whenLabel = getUiText(ui, ["fields", "when"], "Use when");

  container.innerHTML = items
    .map(
      (row) => `
      <article class="service-card">
        <h3>${escapeHtml(row.domain || "")}</h3>
        <p><strong>${escapeHtml(javaLabel)}:</strong> ${escapeHtml(row.java_stack || "")}</p>
        <p><strong>${escapeHtml(pythonLabel)}:</strong> ${escapeHtml(row.python_stack || "")}</p>
        <p><strong>${escapeHtml(whenLabel)}:</strong> ${escapeHtml(row.when || "")}</p>
      </article>
    `,
    )
    .join("");
}

function renderCapstones(items, ui) {
  const container = document.getElementById("capstones");
  const panel = document.getElementById("capstonePanel");
  if (!panel || !container) {
    return;
  }

  if (!Array.isArray(items) || items.length === 0) {
    panel.style.display = "none";
    return;
  }

  const scopeLabel = getUiText(ui, ["fields", "scope"], "Scope");

  container.innerHTML = items
    .map(
      (item) => `
      <article class="service-card">
        <h3>${escapeHtml(item.name || "")}</h3>
        <p><strong>${escapeHtml(scopeLabel)}:</strong> ${escapeHtml(item.scope || "")}</p>
        <div class="tags">
          ${(item.stack || []).map((s) => `<span class="tag">${escapeHtml(s)}</span>`).join("")}
        </div>
      </article>
    `,
    )
    .join("");
}

function renderOpenSourceStacks(items, ui) {
  const container = document.getElementById("oss");
  const panel = document.getElementById("ossPanel");
  if (!panel || !container) {
    return;
  }

  if (!Array.isArray(items) || items.length === 0) {
    panel.style.display = "none";
    return;
  }

  const useCaseLabel = getUiText(ui, ["fields", "use_case"], "Use case");

  container.innerHTML = items
    .map(
      (item) => `
      <article class="service-card">
        <h3>${escapeHtml(item.name || "")}</h3>
        <p><strong>${escapeHtml(useCaseLabel)}:</strong> ${escapeHtml(item.use_case || "")}</p>
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

function renderPathLibrary(panelId, containerId, items, titlePrefix, ui, supportsRunner) {
  const panel = document.getElementById(panelId);
  const container = document.getElementById(containerId);
  if (!panel || !container) {
    return;
  }
  if (!Array.isArray(items) || items.length === 0) {
    panel.style.display = "none";
    return;
  }

  const focusLabel = getUiText(ui, ["fields", "focus"], "Focus");
  const runFileLabel = getUiText(ui, ["roadmap", "run_file"], "Run file");

  container.innerHTML = items
    .map((item) => {
      const runButton =
        supportsRunner && item.path && item.path.endsWith(".py")
          ? `<button class="run-example-btn" data-example-file="${escapeHtml(item.path)}">${escapeHtml(runFileLabel)}</button>`
          : "";
      return `
      <article class="service-card">
        <h3>${escapeHtml(item.title || item.name || "Example")}</h3>
        <p><strong>${escapeHtml(titlePrefix)}:</strong> <code>${escapeHtml(item.path || "")}</code></p>
        ${item.focus ? `<p><strong>${escapeHtml(focusLabel)}:</strong> ${escapeHtml(item.focus)}</p>` : ""}
        ${item.stack ? `<div class="tags">${item.stack.map((v) => `<span class="tag">${escapeHtml(v)}</span>`).join("")}</div>` : ""}
        ${runButton}
      </article>
      `;
    })
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

function renderMiniProjectsWithUi(items, ui) {
  const container = document.getElementById("miniProjects");
  if (!container) {
    return;
  }

  if (!Array.isArray(items) || items.length === 0) {
    container.innerHTML = "";
    return;
  }

  const pathLabel = getUiText(ui, ["fields", "path"], "Path");
  const focusLabel = getUiText(ui, ["fields", "focus"], "Focus");

  container.innerHTML = items
    .map(
      (item) => `
      <article class="service-card">
        <h3>${escapeHtml(item.name || "")}</h3>
        <p><strong>${escapeHtml(pathLabel)}:</strong> <code>${escapeHtml(item.path || "")}</code></p>
        <p><strong>${escapeHtml(focusLabel)}:</strong> ${escapeHtml(item.focus || "")}</p>
        <div class="tags">
          ${(item.stack || []).map((tech) => `<span class="tag">${escapeHtml(tech)}</span>`).join("")}
        </div>
      </article>
    `,
    )
    .join("");
}

function toggleRunnerPanel(supportsRunner) {
  const panel = document.getElementById("consolePanel");
  if (!panel) {
    return;
  }
  panel.style.display = supportsRunner ? "" : "none";
}

function renderPage(data, locale, supportsRunner) {
  const runtimeData = buildRuntimeData(data, locale);
  applyLanguageButtons(locale);
  applyStaticText(runtimeData, supportsRunner);
  renderStats(runtimeData);
  renderCheatSheet(runtimeData.cheat_sheets || [], runtimeData.ui || {});
  renderRoadmap(runtimeData.roadmap || [], runtimeData, supportsRunner);
  renderStackMap(runtimeData.java_python_map || [], runtimeData.ui || {});
  renderArchitectureDiagrams(runtimeData.architecture_diagrams || []);
  renderOpenSourceStacks(runtimeData.open_source_stacks || [], runtimeData.ui || {});
  renderMiniProjectsWithUi(runtimeData.mini_projects || [], runtimeData.ui || {});
  renderPathLibrary(
    "extraPanel",
    "extraExamples",
    runtimeData.extra_examples || [],
    getUiText(runtimeData.ui, ["fields", "path"], "Path"),
    runtimeData.ui || {},
    supportsRunner,
  );
  renderPathLibrary(
    "dbPanel",
    "dbPracticals",
    runtimeData.database_practicals || [],
    getUiText(runtimeData.ui, ["fields", "path"], "Path"),
    runtimeData.ui || {},
    supportsRunner,
  );
  renderCapstones(runtimeData.capstone_projects || [], runtimeData.ui || {});
  renderServices(runtimeData.recommended_services || [], runtimeData.ui || {});
  bindRoadmapActions(runtimeData.site, runtimeData);

  const generatedAt = new Date(data.generated_at).toLocaleString();
  const generatedNode = document.getElementById("generatedAt");
  if (generatedNode) {
    const prefix = getUiText(runtimeData.ui, ["footer", "generated_at"], "Track data generated at");
    generatedNode.textContent = `${prefix} ${generatedAt}`;
  }
}

async function initLearningSite() {
  const source = document.body.dataset.source;
  if (!source) {
    return;
  }

  const response = await fetch(source);
  const data = await response.json();
  const locale = getSelectedLocale(data);
  const supportsRunner = isLocalRunnerHost();

  toggleRunnerPanel(supportsRunner);
  renderPage(data, locale, supportsRunner);

  const buttons = document.querySelectorAll(".lang-btn");
  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      const nextLocale = button.dataset.lang || data.default_locale || "en";
      setSelectedLocale(nextLocale);
      renderPage(data, nextLocale, supportsRunner);
    });
  });

  window.addEventListener("python-labs-language-change", (event) => {
    const nextLocale = event.detail?.locale || data.default_locale || "en";
    renderPage(data, nextLocale, supportsRunner);
  });
}

initLearningSite().catch((error) => {
  const generatedNode = document.getElementById("generatedAt");
  if (generatedNode) {
    generatedNode.textContent = `Failed to load track data: ${error}`;
  }
});
