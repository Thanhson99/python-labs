const PYTHON_LABS_LOCALE_KEY = "python_labs_locale";
const PYTHON_LABS_SUPPORTED_LOCALES = ["en", "vi"];

function getPythonLabsLocale() {
  const saved = localStorage.getItem(PYTHON_LABS_LOCALE_KEY);
  return PYTHON_LABS_SUPPORTED_LOCALES.includes(saved) ? saved : "en";
}

function setPythonLabsLocale(locale) {
  const normalized = PYTHON_LABS_SUPPORTED_LOCALES.includes(locale) ? locale : "en";
  localStorage.setItem(PYTHON_LABS_LOCALE_KEY, normalized);
  document.documentElement.lang = normalized;
  window.dispatchEvent(new CustomEvent("python-labs-language-change", { detail: { locale: normalized } }));
}

function applyLanguageButtons(locale) {
  document.querySelectorAll(".lang-btn").forEach((button) => {
    button.classList.toggle("active", button.dataset.lang === locale);
  });
}

function bindLanguageSwitcher() {
  if (document.body.dataset.langBound === "1") {
    return;
  }

  document.body.dataset.langBound = "1";
  document.querySelectorAll(".lang-btn").forEach((button) => {
    button.addEventListener("click", () => {
      setPythonLabsLocale(button.dataset.lang || "en");
    });
  });
}

function translateLandingPage(locale) {
  if (document.body.dataset.page !== "landing") {
    return;
  }

  const copy = {
    en: {
      eyebrow: "Python Labs",
      title: "Python Learning Portal",
      subtitle:
        "Choose a site for learning, architecture, interview prep, or weekly planning. Everything is static and generated from your current repository.",
      section: "Choose a Site",
      foundationTitle: "Foundation Site",
      foundationSummary: "Massive practical cheat sheet for Python core to strong intermediate.",
      foundationButton: "Open Foundation",
      advancedTitle: "Advanced Architecture Site",
      advancedSummary: "Roadmap for production systems: queues, Kafka, microservices, reliability.",
      advancedButton: "Open Advanced",
      interviewTitle: "Interview Practice Site",
      interviewSummary: "Static interview prep portal with topic catalog, JSON question bank, answers, and explanations.",
      interviewButton: "Open Interview Prep",
      sourcesTitle: "Interview Sources Site",
      sourcesSummary: "Static curated source hub for Vietnamese and English interview learning resources.",
      sourcesButton: "Open Sources",
      plannerTitle: "Study Planner Site",
      plannerSummary: "Weekly study plans with checklists for Foundation, Advanced, and Interview prep.",
      plannerButton: "Open Planner",
    },
    vi: {
      eyebrow: "Python Labs",
      title: "Cổng Học Python",
      subtitle:
        "Chọn site để học, xem kiến trúc, luyện phỏng vấn hoặc lập kế hoạch học theo tuần. Mọi thứ đều là static và được tạo trực tiếp từ repository hiện tại.",
      section: "Chọn một Site",
      foundationTitle: "Site Foundation",
      foundationSummary: "Cheat sheet thực hành lớn cho Python từ cốt lõi đến trung cấp vững.",
      foundationButton: "Mở Site Foundation",
      advancedTitle: "Site Kiến Trúc Nâng Cao",
      advancedSummary: "Lộ trình cho hệ thống production: queue, Kafka, microservice và reliability.",
      advancedButton: "Mở Site Nâng Cao",
      interviewTitle: "Site Luyện Phỏng Vấn",
      interviewSummary: "Cổng luyện phỏng vấn tĩnh với catalog chủ đề, ngân hàng câu hỏi JSON, đáp án và giải thích.",
      interviewButton: "Mở Luyện Phỏng Vấn",
      sourcesTitle: "Site Nguồn Phỏng Vấn",
      sourcesSummary: "Kho tài liệu tĩnh tổng hợp nguồn học phỏng vấn tiếng Việt và tiếng Anh.",
      sourcesButton: "Mở Nguồn Tài Liệu",
      plannerTitle: "Site Kế Hoạch Học",
      plannerSummary: "Kế hoạch học theo tuần có checklist cho Foundation, Advanced và luyện phỏng vấn.",
      plannerButton: "Mở Kế Hoạch Học",
      note: "Các trang luyện phỏng vấn là static hoàn toàn, nên có thể deploy trực tiếp lên GitHub Pages mà không cần Python server.",
    },
  }[locale] || {};

  const setText = (id, value) => {
    const node = document.getElementById(id);
    if (node && value) {
      node.textContent = value;
    }
  };

  setText("eyebrow", copy.eyebrow);
  setText("landingTitle", copy.title);
  setText("landingSubtitle", copy.subtitle);
  setText("landingSectionTitle", copy.section);
  setText("landingFoundationTitle", copy.foundationTitle);
  setText("landingFoundationSummary", copy.foundationSummary);
  setText("landingFoundationButton", copy.foundationButton);
  setText("landingAdvancedTitle", copy.advancedTitle);
  setText("landingAdvancedSummary", copy.advancedSummary);
  setText("landingAdvancedButton", copy.advancedButton);
  setText("landingInterviewTitle", copy.interviewTitle);
  setText("landingInterviewSummary", copy.interviewSummary);
  setText("landingInterviewButton", copy.interviewButton);
  setText("landingSourcesTitle", copy.sourcesTitle);
  setText("landingSourcesSummary", copy.sourcesSummary);
  setText("landingSourcesButton", copy.sourcesButton);
  setText("landingPlannerTitle", copy.plannerTitle);
  setText("landingPlannerSummary", copy.plannerSummary);
  setText("landingPlannerButton", copy.plannerButton);
  setText("landingNote", copy.note);
}

function initPythonLabsSiteLanguage() {
  const locale = getPythonLabsLocale();
  document.documentElement.lang = locale;
  applyLanguageButtons(locale);
  bindLanguageSwitcher();
  translateLandingPage(locale);

  window.addEventListener("python-labs-language-change", (event) => {
    const nextLocale = event.detail?.locale || "en";
    applyLanguageButtons(nextLocale);
    translateLandingPage(nextLocale);
  });
}

window.PythonLabsI18n = {
  getLocale: getPythonLabsLocale,
  setLocale: setPythonLabsLocale,
  applyButtons: applyLanguageButtons,
};

initPythonLabsSiteLanguage();
