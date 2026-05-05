function plannerLocale() {
  return window.PythonLabsI18n?.getLocale?.() || "en";
}

function plannerStateKey(planId, weekId, taskIndex) {
  return `planner_task:${planId}:${weekId}:${taskIndex}`;
}

function isPlannerTaskDone(planId, weekId, taskIndex) {
  return localStorage.getItem(plannerStateKey(planId, weekId, taskIndex)) === "1";
}

function setPlannerTaskDone(planId, weekId, taskIndex, done) {
  localStorage.setItem(plannerStateKey(planId, weekId, taskIndex), done ? "1" : "0");
}

function resetPlannerPlan(planId) {
  Object.keys(localStorage).forEach((key) => {
    if (key.startsWith(`planner_task:${planId}:`)) {
      localStorage.removeItem(key);
    }
  });
}

function plannerText(payload, locale) {
  return payload?.locales?.[locale] || payload?.locales?.en || {};
}

function plannerUi(payload, locale) {
  return plannerText(payload, locale).ui || {};
}

function plannerPlans(payload, locale) {
  return plannerText(payload, locale).plans || [];
}

function plannerList(payload, locale, key) {
  return plannerText(payload, locale)[key] || [];
}

function plannerLevelClass(value) {
  const normalized = String(value || "").toLowerCase();
  if (normalized.includes("advanced") || normalized.includes("nâng")) {
    return "advanced";
  }
  if (normalized.includes("interview") || normalized.includes("phỏng")) {
    return "intermediate";
  }
  return "basic";
}

function plannerTotals(plans) {
  let weeks = 0;
  let tasks = 0;
  let completed = 0;

  plans.forEach((plan) => {
    (plan.weeks || []).forEach((week) => {
      weeks += 1;
      (week.tasks || []).forEach((_task, taskIndex) => {
        tasks += 1;
        if (isPlannerTaskDone(plan.id, week.id, taskIndex)) {
          completed += 1;
        }
      });
    });
  });

  return { weeks, tasks, completed };
}

function plannerStatCards(items) {
  const stats = document.getElementById("stats");
  if (!stats) {
    return;
  }

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

function renderPlannerHighlights(ui) {
  const node = document.getElementById("highlights");
  if (!node) {
    return;
  }

  const items = [
    [ui.highlight1Title, ui.highlight1Body],
    [ui.highlight2Title, ui.highlight2Body],
    [ui.highlight3Title, ui.highlight3Body],
  ];

  node.innerHTML = items
    .map(
      ([title, body]) => `
        <article class="service-card planner-card">
          <h3>${title || ""}</h3>
          <p>${body || ""}</p>
        </article>
      `,
    )
    .join("");
}

function renderPlannerSimpleCards(containerId, items, bodyKey) {
  const node = document.getElementById(containerId);
  if (!node) {
    return;
  }

  node.innerHTML = items
    .map(
      (item) => `
        <article class="service-card planner-card">
          <h3>${item.title || ""}</h3>
          <p>${item[bodyKey] || ""}</p>
        </article>
      `,
    )
    .join("");
}

function renderPlannerPlans(payload, locale) {
  const ui = plannerUi(payload, locale);
  const plans = plannerPlans(payload, locale);
  const totals = plannerTotals(plans);
  const plansNode = document.getElementById("plans");

  document.documentElement.lang = locale;
  const title = document.getElementById("title");
  const subtitle = document.getElementById("subtitle");
  const backButton = document.getElementById("backButton");
  const sectionHighlights = document.getElementById("sectionHighlights");
  const sectionQuickStart = document.getElementById("sectionQuickStart");
  const sectionHabits = document.getElementById("sectionHabits");
  const sectionPlans = document.getElementById("sectionPlans");
  const sectionReview = document.getElementById("sectionReview");
  const generatedAt = document.getElementById("generatedAt");

  if (title) {
    title.textContent = plannerText(payload, locale).title || "Study Planner";
  }
  if (subtitle) {
    subtitle.textContent = plannerText(payload, locale).subtitle || "";
  }
  if (backButton) {
    backButton.textContent = ui.backButton || "Back to track selection";
  }
  if (sectionHighlights) {
    sectionHighlights.textContent = ui.sectionHighlights || "How To Use This Planner";
  }
  if (sectionQuickStart) {
    sectionQuickStart.textContent = ui.sectionQuickStart || "Quick Start";
  }
  if (sectionHabits) {
    sectionHabits.textContent = ui.sectionHabits || "Daily Habits";
  }
  if (sectionPlans) {
    sectionPlans.textContent = ui.sectionPlans || "Study Plans";
  }
  if (sectionReview) {
    sectionReview.textContent = ui.sectionReview || "Weekly Review Questions";
  }
  if (generatedAt) {
    const timestamp = payload.generated_at ? new Date(payload.generated_at).toLocaleString() : "static data";
    generatedAt.textContent = `${ui.statsMode || "Mode"}: ${ui.modeValue || "Saved locally"} | ${timestamp}`;
  }

  plannerStatCards([
    [ui.statsPlans || "Plans", plans.length],
    [ui.statsWeeks || "Weeks", totals.weeks],
    [ui.statsCompleted || "Completed Tasks", `${totals.completed}/${totals.tasks}`],
    [ui.statsMode || "Mode", ui.modeValue || "Saved locally"],
  ]);

  renderPlannerHighlights(ui);
  renderPlannerSimpleCards("quickStart", plannerList(payload, locale, "quick_start"), "body");
  renderPlannerSimpleCards("habits", plannerList(payload, locale, "daily_habits"), "body");
  renderPlannerSimpleCards("reviewQuestions", plannerList(payload, locale, "weekly_review"), "body");

  if (!plansNode) {
    return;
  }

  plansNode.innerHTML = plans
    .map((plan) => {
      const planCompleted = (plan.weeks || []).reduce((count, week) => {
        return (
          count +
          (week.tasks || []).filter((_task, taskIndex) => isPlannerTaskDone(plan.id, week.id, taskIndex)).length
        );
      }, 0);
      const planTotal = (plan.weeks || []).reduce((count, week) => count + (week.tasks || []).length, 0);

      return `
        <article class="timeline-item planner-plan" data-plan-id="${plan.id}">
          <div class="planner-plan-header">
            <div>
              <p><span class="level ${plannerLevelClass(plan.level)}">${plan.level || ""}</span></p>
              <h3>${plan.name || ""}</h3>
              <p>${plan.summary || ""}</p>
            </div>
            <div class="planner-progress-chip">${planCompleted}/${planTotal}</div>
          </div>
          <div class="planner-grid">
            <p><strong>${ui.durationLabel || "Duration"}:</strong> ${plan.duration || ""}</p>
            <p><strong>${ui.outcomeLabel || "Target outcome"}:</strong> ${plan.outcome || ""}</p>
          </div>
          <p><strong>${ui.focusLabel || "Focus"}:</strong> ${(plan.focus || []).join(", ")}</p>
          <div class="planner-subsection">
            <p><strong>${ui.deliverablesLabel || "Deliverables"}:</strong></p>
            <ul>
              ${(plan.deliverables || []).map((item) => `<li>${item}</li>`).join("")}
            </ul>
          </div>
          <div class="planner-subsection">
            <p><strong>${ui.milestonesLabel || "Milestones"}:</strong></p>
            <ul>
              ${(plan.milestones || []).map((item) => `<li>${item}</li>`).join("")}
            </ul>
          </div>
          <div class="planner-subsection">
            <p><strong>${ui.resourcesLabel || "Use these site sections"}:</strong></p>
            <div class="tags">
              ${(plan.resources || []).map((item) => `<span class="tag">${item}</span>`).join("")}
            </div>
          </div>
          <div class="planner-weeks">
            ${(plan.weeks || [])
              .map(
                (week, weekIndex) => `
                  <section class="planner-week">
                    <div class="planner-week-head">
                      <h4>${ui.weekLabel || "Week"} ${weekIndex + 1}: ${week.title || ""}</h4>
                    </div>
                    <p><strong>${ui.goalLabel || "Outcome"}:</strong> ${week.goal || ""}</p>
                    <p><strong>${ui.taskLabel || "Checklist"}:</strong></p>
                    <div class="planner-task-list">
                      ${(week.tasks || [])
                        .map(
                          (task, taskIndex) => `
                            <label class="planner-task">
                              <input
                                type="checkbox"
                                data-plan-id="${plan.id}"
                                data-week-id="${week.id}"
                                data-task-index="${taskIndex}"
                                ${isPlannerTaskDone(plan.id, week.id, taskIndex) ? "checked" : ""}
                              />
                              <span>${task}</span>
                            </label>
                          `,
                        )
                        .join("")}
                    </div>
                  </section>
                `,
              )
              .join("")}
          </div>
          <p class="planner-actions">
            <button type="button" class="btn secondary-btn planner-reset-btn" data-plan-id="${plan.id}">${ui.resetPlan || "Reset plan progress"}</button>
          </p>
        </article>
      `;
    })
    .join("");

  plansNode.querySelectorAll(".planner-task input").forEach((input) => {
    input.addEventListener("change", (event) => {
      const target = event.currentTarget;
      setPlannerTaskDone(target.dataset.planId, target.dataset.weekId, Number(target.dataset.taskIndex), target.checked);
      renderPlannerPlans(payload, plannerLocale());
    });
  });

  plansNode.querySelectorAll(".planner-reset-btn").forEach((button) => {
    button.addEventListener("click", () => {
      resetPlannerPlan(button.dataset.planId);
      renderPlannerPlans(payload, plannerLocale());
    });
  });
}

async function initPlannerSite() {
  const source = document.body.dataset.source;
  if (!source) {
    return;
  }

  const response = await fetch(source);
  const payload = await response.json();

  const render = () => renderPlannerPlans(payload, plannerLocale());
  render();
  window.addEventListener("python-labs-language-change", render);
}

initPlannerSite().catch((error) => {
  const generatedAt = document.getElementById("generatedAt");
  if (generatedAt) {
    generatedAt.textContent = String(error);
  }
});
