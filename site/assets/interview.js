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

function getQueryParam(name) {
  const params = new URLSearchParams(window.location.search);
  return params.get(name);
}

function slugify(value) {
  return String(value || "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

function getScoreRating(scorePercent) {
  if (scorePercent >= 90) {
    return "Excellent";
  }
  if (scorePercent >= 75) {
    return "Good";
  }
  if (scorePercent >= 60) {
    return "Fair";
  }
  if (scorePercent >= 40) {
    return "Average";
  }
  return "Needs Review";
}

function getBestScoreKey(setId) {
  return `interview_quiz_best:${setId || "default"}`;
}

function getBestScore(setId) {
  const raw = localStorage.getItem(getBestScoreKey(setId));
  return raw ? JSON.parse(raw) : null;
}

function setBestScore(setId, payload) {
  localStorage.setItem(getBestScoreKey(setId), JSON.stringify(payload));
}

function buildSearchText(item) {
  return [
    item.category,
    item.question,
    item.question_vi,
    item.question_en,
    item.correct_answer,
    item.explanation,
    ...(item.compare || []),
  ]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();
}

function buildFallbackOptions(item, index) {
  const category = String(item.category || "").toLowerCase();
  const templates = {
    "python core": [
      "Because Python treats these cases as identical in normal execution.",
      "Because this behavior only matters in frontend code, not Python itself.",
      "Because the interpreter converts everything automatically behind the scenes.",
    ],
    "http apis": [
      "Because HTTP errors are automatically retried by the browser in all cases.",
      "Because API responses never need validation if the endpoint is internal.",
      "Because status codes are only useful for debugging and not real application logic.",
    ],
    automation: [
      "Because automation scripts should avoid all configuration and always hardcode values.",
      "Because repeated reruns always improve correctness no matter what the script does.",
      "Because logging is optional once a script works locally one time.",
    ],
    databases: [
      "Because database structure rarely affects application behavior after deployment.",
      "Because SQL safety is mostly unrelated to parameter handling.",
      "Because indexes only help write speed and not reads.",
    ],
    "ai/ml": [
      "Because model evaluation is unnecessary when the training score is high.",
      "Because machine learning quality depends only on model size and not on data.",
      "Because semantic retrieval removes the need for checking grounded answers.",
    ],
  };

  const generic = [
    "Because this distinction usually has no real effect in production systems.",
    "Because Python or the framework handles the difference automatically every time.",
    "Because the main goal is visual formatting rather than program behavior.",
  ];

  let distractors = generic;
  for (const [key, values] of Object.entries(templates)) {
    if (category.includes(key)) {
      distractors = values;
      break;
    }
  }

  const options = [
    item.correct_answer,
    distractors[0],
    distractors[1],
    distractors[2],
  ].filter(Boolean);

  const insertAt = index % options.length;
  const reordered = [];
  let correctInserted = false;
  for (let i = 0; i < options.length; i += 1) {
    if (i === insertAt) {
      reordered.push(item.correct_answer);
      correctInserted = true;
    }
    const next = options[i];
    if (next !== item.correct_answer) {
      reordered.push(next);
    }
  }
  if (!correctInserted) {
    reordered.push(item.correct_answer);
  }

  return [...new Set(reordered)].slice(0, 4);
}

function ensureQuestionOptions(item, index) {
  if (Array.isArray(item.options) && item.options.length >= 2) {
    return item.options;
  }
  return buildFallbackOptions(item, index);
}

function renderStatCards(items) {
  const stats = document.getElementById("stats");
  if (!stats || !Array.isArray(items)) {
    return;
  }

  stats.innerHTML = items
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

function renderCatalogStats(data) {
  renderStatCards([
    ["Tracks", (data.ladders || []).length],
    ["Topics", (data.topic_catalog || []).length],
    ["Practice Sets", (data.practice_sets || []).length],
    ["Format", "Static JSON"],
  ]);
}

function renderSourcesStats(data) {
  renderStatCards([
    ["VI Sources", (data.vietnamese_sources || []).length],
    ["EN Sources", (data.english_sources || []).length],
    ["Study Paths", (data.study_paths || []).length],
    ["Format", "Static Links"],
  ]);
}

function renderQuestionStats(data) {
  const questions = Array.isArray(data.questions) ? data.questions : [];
  const categories = new Set(questions.map((item) => item.category).filter(Boolean));
  const best = getBestScore(data.set_id || "default");
  renderStatCards([
    ["Questions", questions.length],
    ["Categories", categories.size],
    ["Level", data.level || "basic"],
    ["Best", best ? `${best.scorePercent}%` : "No score"],
  ]);
}

function renderCards(containerId, items, renderer) {
  const container = document.getElementById(containerId);
  if (!container || !Array.isArray(items)) {
    return;
  }
  container.innerHTML = items.map(renderer).join("");
}

function renderCatalogPage(data) {
  const title = document.getElementById("title");
  const subtitle = document.getElementById("subtitle");

  if (title) {
    title.textContent = data.title || title.textContent;
  }
  if (subtitle) {
    subtitle.textContent = data.subtitle || "";
  }

  renderCatalogStats(data);

  renderCards(
    "ladders",
    data.ladders || [],
    (item) => `
      <article class="service-card interview-card">
        <p><span class="tag category">${escapeHtml(item.level || "")}</span></p>
        <h3>${escapeHtml(item.name || "")}</h3>
        <p>${escapeHtml(item.summary || "")}</p>
        <p><strong>Focus:</strong> ${escapeHtml((item.focus || []).join(", "))}</p>
      </article>
    `,
  );

  renderCards(
    "topicCatalog",
    data.topic_catalog || [],
    (item) => `
      <article class="service-card interview-card">
        <p><span class="tag">${escapeHtml(item.domain || "")}</span></p>
        <h3>${escapeHtml(item.title || "")}</h3>
        <p>${escapeHtml(item.summary || "")}</p>
        <p><strong>Examples:</strong> ${escapeHtml((item.examples || []).join(", "))}</p>
        <p><strong>Expected depth:</strong> ${escapeHtml(item.depth || "")}</p>
      </article>
    `,
  );

  renderCards(
    "practiceSets",
    data.practice_sets || [],
    (item) => `
      <article class="service-card interview-card">
        <p><span class="level ${escapeHtml(item.level_class || "basic")}">${escapeHtml(item.level || "")}</span></p>
        <h3>${escapeHtml(item.name || "")}</h3>
        <p>${escapeHtml(item.summary || "")}</p>
        <p><strong>Topics:</strong> ${escapeHtml((item.topics || []).join(", "))}</p>
        <p><strong>Output:</strong> ${escapeHtml(item.output || "")}</p>
        ${item.question_set ? `<p><a class="btn" href="${escapeHtml(item.question_page || "interview-questions.html")}?set=${encodeURIComponent(item.question_set)}">Open set</a></p>` : ""}
      </article>
    `,
  );

  renderCards(
    "projectIdeas",
    data.project_ideas || [],
    (item) => `
      <article class="service-card interview-card">
        <h3>${escapeHtml(item.name || "")}</h3>
        <p>${escapeHtml(item.summary || "")}</p>
        <p><strong>Why it matters:</strong> ${escapeHtml(item.why || "")}</p>
        <div class="tags">
          ${(item.stack || []).map((tag) => `<span class="tag">${escapeHtml(tag)}</span>`).join("")}
        </div>
      </article>
    `,
  );

  renderCards(
    "prepNotes",
    data.preparation_notes || [],
    (item) => `
      <article class="service-card interview-card">
        <h3>${escapeHtml(item.title || "")}</h3>
        <p>${escapeHtml(item.note || "")}</p>
      </article>
    `,
  );
}

function renderQuestionSetLinks(registry, activeSetId) {
  const container = document.getElementById("questionSetLinks");
  if (!container) {
    return;
  }

  const sets = Array.isArray(registry?.sets) ? registry.sets : [];
  const currentPage = window.location.pathname.split("/").pop() || "interview-questions.html";
  container.innerHTML = sets
    .map((item) => {
      const activeClass = item.id === activeSetId ? " active-set" : "";
      return `
        <article class="service-card interview-card compact-card${activeClass}">
          <p><span class="level ${escapeHtml(item.level_class || "basic")}">${escapeHtml(item.level || "")}</span></p>
          <h3>${escapeHtml(item.name || "")}</h3>
          <p>${escapeHtml(item.summary || "")}</p>
          <p><a class="btn" href="${escapeHtml(currentPage)}?set=${encodeURIComponent(item.id)}">Open set</a></p>
        </article>
      `;
    })
    .join("");
}

function renderInterviewSourcesPage(data) {
  const title = document.getElementById("title");
  const subtitle = document.getElementById("subtitle");

  if (title) {
    title.textContent = data.title || title.textContent;
  }
  if (subtitle) {
    subtitle.textContent = data.subtitle || "";
  }

  renderSourcesStats(data);

  renderCards(
    "sourceQuestionSets",
    data.question_sets || [],
    (item) => `
      <article class="service-card interview-card compact-card">
        <p><span class="level ${escapeHtml(item.level_class || "basic")}">${escapeHtml(item.level || "")}</span></p>
        <h3>${escapeHtml(item.name || "")}</h3>
        <p>${escapeHtml(item.summary || "")}</p>
        <p><a class="btn" href="${escapeHtml(item.href || "#")}">Open question set</a></p>
      </article>
    `,
  );

  renderCards(
    "sourceGuides",
    data.guides || [],
    (item) => `
      <article class="service-card interview-card">
        <h3>${escapeHtml(item.title || "")}</h3>
        <p>${escapeHtml(item.note || "")}</p>
      </article>
    `,
  );

  const sourceCard = (item) => `
    <article class="source-row">
      <h3>${escapeHtml(item.name || "")}</h3>
      <p><strong>Level:</strong> ${escapeHtml(item.level || "")}</p>
      <p><strong>Focus:</strong> ${escapeHtml(item.focus || "")}</p>
      <p><strong>Best for:</strong> ${escapeHtml(item.best_for || "")}</p>
      <p><a class="btn" href="${escapeHtml(item.url || "#")}" target="_blank" rel="noreferrer">Open reference link</a></p>
    </article>
  `;

  renderCards("vietnameseSources", data.vietnamese_sources || [], sourceCard);
  renderCards("englishSources", data.english_sources || [], sourceCard);
}

function buildFilterButtons(categories) {
  const container = document.getElementById("filters");
  if (!container) {
    return;
  }

  const allCategories = ["All", ...categories];
  container.innerHTML = allCategories
    .map(
      (category, index) => `
        <button class="filter-btn ${index === 0 ? "active" : ""}" data-category="${escapeHtml(category)}">
          ${escapeHtml(category)}
        </button>
      `,
    )
    .join("");
}

function questionCard(item, index) {
  const options = ensureQuestionOptions(item, index);
  const questionId = slugify(`${item.category || "question"}-${index + 1}`);
  const intent = item.intent ? `<p>${escapeHtml(item.intent)}</p>` : "";
  const languageMarkup =
    item.question_vi || item.question_en
      ? `
        <div class="question-language">
          ${item.question_vi ? `<div class="language-row"><span class="language-label">VI</span>${escapeHtml(item.question_vi)}</div>` : ""}
          ${item.question_en ? `<div class="language-row"><span class="language-label">EN</span>${escapeHtml(item.question_en)}</div>` : ""}
        </div>
      `
      : "";
  const optionMarkup = `
      <div class="question-options">
        ${options
          .map(
            (option, optionIndex) => `
              <div class="option-item" data-option-index="${optionIndex}">
                <label>
                  <input type="radio" name="${escapeHtml(questionId)}" value="${escapeHtml(option)}" />
                  <span>${escapeHtml(option)}</span>
                </label>
              </div>
            `,
          )
          .join("")}
      </div>
    `;

  const comparison = Array.isArray(item.compare)
    ? `
      <div class="compare-box">
        <strong>Compare:</strong>
        <ul>
          ${item.compare.map((entry) => `<li>${escapeHtml(entry)}</li>`).join("")}
        </ul>
      </div>
    `
    : "";

  const snippet = item.code_snippet
    ? `<pre><code>${escapeHtml(normalizeSnippet(item.code_snippet))}</code></pre>`
    : "";

  return `
    <article class="question-card" data-category="${escapeHtml(item.category || "")}" data-correct-answer="${escapeHtml(item.correct_answer || "")}">
      <div class="question-meta">
        <span class="tag category">${escapeHtml(item.category || "General")}</span>
        <span class="level ${escapeHtml(item.level_class || "basic")}">${escapeHtml(item.level || "basic")}</span>
        <span class="question-index">Q${index + 1}</span>
      </div>
      <h3>${escapeHtml(item.question || "")}</h3>
      ${languageMarkup}
      ${intent}
      ${optionMarkup}
      <div class="question-actions">
        <button class="btn reveal-btn" type="button">Check Answer</button>
        <span class="result-badge pending">Not checked</span>
      </div>
      <div class="answer-panel" hidden>
        <p><strong>Correct answer:</strong> ${escapeHtml(item.correct_answer || "")}</p>
        <p><strong>Explanation:</strong> ${escapeHtml(item.explanation || "")}</p>
        ${snippet}
        ${comparison}
      </div>
    </article>
  `;
}

function applyQuestionFilters() {
  const activeButton = document.querySelector(".filter-btn.active");
  const selectedCategory = activeButton?.dataset.category || "All";
  const searchValue = String(document.getElementById("questionSearch")?.value || "").trim().toLowerCase();
  const cards = document.querySelectorAll(".question-card");
  let visibleCount = 0;

  cards.forEach((card) => {
    const category = card.getAttribute("data-category") || "";
    const searchText = card.getAttribute("data-search-text") || "";
    const categoryMatch = selectedCategory === "All" || category === selectedCategory;
    const searchMatch = !searchValue || searchText.includes(searchValue);
    const visible = categoryMatch && searchMatch;
    card.toggleAttribute("hidden", !visible);
    if (visible) {
      visibleCount += 1;
    }
  });

  const searchMeta = document.getElementById("searchMeta");
  if (searchMeta) {
    searchMeta.textContent = searchValue
      ? `Showing ${visibleCount} matching questions`
      : `Showing ${visibleCount} questions`;
  }
}

function evaluateQuestionCard(card) {
  const selected = card.querySelector("input[type='radio']:checked");
  const answerPanel = card.querySelector(".answer-panel");
  const badge = card.querySelector(".result-badge");
  const correctAnswer = card.dataset.correctAnswer || "";
  const options = card.querySelectorAll(".option-item");

  options.forEach((node) => {
    node.classList.remove("correct-option", "wrong-option");
    const input = node.querySelector("input");
    if (input && input.value === correctAnswer) {
      node.classList.add("correct-option");
    }
  });

  if (!selected) {
    if (badge) {
      badge.textContent = "Unanswered";
      badge.className = "result-badge wrong";
    }
    if (answerPanel) {
      answerPanel.removeAttribute("hidden");
    }
    return { answered: false, correct: false };
  }

  const isCorrect = selected.value === correctAnswer;
  const selectedOption = selected.closest(".option-item");
  if (selectedOption && !isCorrect) {
    selectedOption.classList.add("wrong-option");
  }

  if (badge) {
    badge.textContent = isCorrect ? "Correct" : "Wrong";
    badge.className = `result-badge ${isCorrect ? "correct" : "wrong"}`;
  }
  if (answerPanel) {
    answerPanel.removeAttribute("hidden");
  }

  return { answered: true, correct: isCorrect };
}

function updateQuizSummary(activeSetId) {
  const cards = document.querySelectorAll(".question-card");
  let answered = 0;
  let correct = 0;

  cards.forEach((card) => {
    const checked = card.querySelector("input[type='radio']:checked");
    const badge = card.querySelector(".result-badge");
    if (checked) {
      answered += 1;
    }
    if (badge && badge.classList.contains("correct")) {
      correct += 1;
    }
  });

  const total = cards.length || 1;
  const scorePercent = Math.round((correct / total) * 100);
  const rating = getScoreRating(scorePercent);

  const answeredNode = document.getElementById("answeredCount");
  const correctNode = document.getElementById("correctCount");
  const scoreNode = document.getElementById("scorePercent");
  const ratingNode = document.getElementById("scoreRating");

  if (answeredNode) {
    answeredNode.textContent = `${answered}/${cards.length}`;
  }
  if (correctNode) {
    correctNode.textContent = `${correct}`;
  }
  if (scoreNode) {
    scoreNode.textContent = `${scorePercent}%`;
  }
  if (ratingNode) {
    ratingNode.textContent = answered === cards.length ? rating : "In progress";
  }

  if (answered === cards.length) {
    const best = getBestScore(activeSetId);
    if (!best || scorePercent > best.scorePercent) {
      setBestScore(activeSetId, {
        answered,
        correct,
        total: cards.length,
        scorePercent,
        rating,
      });
    }
  }
}

function bindQuestionInteractions(activeSetId, data) {
  const revealButtons = document.querySelectorAll(".reveal-btn");
  revealButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const card = button.closest(".question-card");
      if (!card) {
        return;
      }
      evaluateQuestionCard(card);
      updateQuizSummary(activeSetId);
    });
  });

  const radioInputs = document.querySelectorAll(".question-card input[type='radio']");
  radioInputs.forEach((input) => {
    input.addEventListener("change", () => {
      updateQuizSummary(activeSetId);
    });
  });

  const filterButtons = document.querySelectorAll(".filter-btn");
  const cards = document.querySelectorAll(".question-card");
  filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
      filterButtons.forEach((node) => node.classList.remove("active"));
      button.classList.add("active");
      applyQuestionFilters();
    });
  });

  const searchInput = document.getElementById("questionSearch");
  if (searchInput) {
    searchInput.addEventListener("input", () => {
      applyQuestionFilters();
    });
  }

  const finishButton = document.getElementById("finishQuizBtn");
  if (finishButton) {
    finishButton.addEventListener("click", () => {
      let correct = 0;
      let answered = 0;
      cards.forEach((card) => {
        const result = evaluateQuestionCard(card);
        if (result.answered) {
          answered += 1;
        }
        if (result.correct) {
          correct += 1;
        }
      });

      const total = cards.length || 1;
      const scorePercent = Math.round((correct / total) * 100);
      const rating = getScoreRating(scorePercent);
      updateQuizSummary(activeSetId);
      renderQuestionStats(data);
      window.alert(
        `Quiz completed.\nSet: ${data.title}\nAnswered: ${answered}/${cards.length}\nCorrect: ${correct}/${cards.length}\nScore: ${scorePercent}%\nRating: ${rating}`,
      );
    });
  }

  const resetButton = document.getElementById("resetQuizBtn");
  if (resetButton) {
    resetButton.addEventListener("click", () => {
      cards.forEach((card) => {
        card.querySelectorAll("input[type='radio']").forEach((input) => {
          input.checked = false;
        });
        card.querySelectorAll(".option-item").forEach((node) => {
          node.classList.remove("correct-option", "wrong-option");
        });
        const badge = card.querySelector(".result-badge");
        if (badge) {
          badge.textContent = "Not checked";
          badge.className = "result-badge pending";
        }
        const panel = card.querySelector(".answer-panel");
        if (panel) {
          panel.setAttribute("hidden", "");
        }
      });
      updateQuizSummary(activeSetId);
    });
  }
}

function renderQuestionsPage(data, registry, activeSetId) {
  const title = document.getElementById("title");
  const subtitle = document.getElementById("subtitle");
  const questions = Array.isArray(data.questions) ? data.questions : [];
  data.set_id = activeSetId || data.set_id || "default";

  if (title) {
    title.textContent = data.title || title.textContent;
  }
  if (subtitle) {
    subtitle.textContent = data.subtitle || "";
  }

  renderQuestionStats(data);
  renderQuestionSetLinks(registry, activeSetId);

  const questionList = document.getElementById("questionList");
  if (questionList) {
    questionList.innerHTML = questions.map((item, index) => questionCard(item, index)).join("");
    const cards = questionList.querySelectorAll(".question-card");
    cards.forEach((card, index) => {
      card.setAttribute("data-search-text", buildSearchText(questions[index]));
    });
  }

  const categories = [...new Set(questions.map((item) => item.category).filter(Boolean))];
  buildFilterButtons(categories);
  bindQuestionInteractions(activeSetId, data);
  updateQuizSummary(activeSetId);
  applyQuestionFilters();
}

async function loadQuestionSet(source, registrySource) {
  const selectedSet = getQueryParam("set") || "basic";

  if (!registrySource) {
    const response = await fetch(source);
    const data = await response.json();
    return { data, registry: null, activeSetId: selectedSet };
  }

  const registryResponse = await fetch(registrySource);
  const registry = await registryResponse.json();
  const sets = Array.isArray(registry.sets) ? registry.sets : [];
  const matched = sets.find((item) => item.id === selectedSet) || sets[0];
  const resolvedSource = matched?.file || source;
  const dataResponse = await fetch(resolvedSource);
  const data = await dataResponse.json();
  return { data, registry, activeSetId: matched?.id || selectedSet };
}

async function initInterviewSite() {
  const source = document.body.dataset.source;
  const page = document.body.dataset.page;
  const registrySource = document.body.dataset.registry;
  if (!source || !page) {
    return;
  }

  let data;
  let registry = null;
  let activeSetId = null;

  if (page === "interview-questions") {
    const payload = await loadQuestionSet(source, registrySource);
    data = payload.data;
    registry = payload.registry;
    activeSetId = payload.activeSetId;
  } else {
    const response = await fetch(source);
    data = await response.json();
  }

  if (page === "interview-catalog") {
    renderCatalogPage(data);
  }
  if (page === "interview-questions") {
    renderQuestionsPage(data, registry, activeSetId);
  }
  if (page === "interview-sources") {
    renderInterviewSourcesPage(data);
  }

  const generatedNode = document.getElementById("generatedAt");
  if (generatedNode) {
    const generatedAt = data.generated_at ? new Date(data.generated_at).toLocaleString() : "static data";
    generatedNode.textContent = `Interview data generated at ${generatedAt}`;
  }
}

initInterviewSite().catch((error) => {
  const generatedNode = document.getElementById("generatedAt");
  if (generatedNode) {
    generatedNode.textContent = `Failed to load interview data: ${error}`;
  }
});
