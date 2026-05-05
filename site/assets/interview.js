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

function getLocale() {
  return window.PythonLabsI18n?.getLocale?.() || "en";
}

function getLocaleSource(source, locale) {
  if (locale !== "vi") {
    return source;
  }
  return source.replace(/\.json$/i, "-vi.json");
}

async function fetchJsonWithLocale(source, locale) {
  const localizedSource = getLocaleSource(source, locale);
  if (localizedSource !== source) {
    try {
      const localizedResponse = await fetch(localizedSource);
      if (localizedResponse.ok) {
        return await localizedResponse.json();
      }
    } catch (_error) {
      // Fall back to the default source below.
    }
  }

  const response = await fetch(source);
  return await response.json();
}

const INTERVIEW_I18N = {
  en: {
    common: {
      eyebrow: "Python Labs",
      backToTracks: "Back to track selection",
      general: "General",
      all: "All",
      formatStaticJson: "Static JSON",
      formatStaticLinks: "Static Links",
      generatedAt: "Interview data generated at",
      failedLoad: "Failed to load interview data",
      level: "Level",
      focus: "Focus",
      bestFor: "Best for",
      examples: "Examples",
      expectedDepth: "Expected depth",
      topics: "Topics",
      output: "Output",
      whyItMatters: "Why it matters",
      openSet: "Open set",
      openQuestionSet: "Open question set",
      openReferenceLink: "Open reference link",
      noScore: "No score",
      inProgress: "In progress",
      notGraded: "Not graded",
      notChecked: "Not checked",
      unanswered: "Unanswered",
      correct: "Correct",
      wrong: "Wrong",
      compare: "Compare",
      correctAnswer: "Correct answer",
      explanation: "Explanation",
      checkAnswer: "Check Answer",
      finishQuiz: "Finish Quiz",
      resetQuiz: "Reset Quiz",
      searchAll: "Showing all questions",
      searchShowing: "Showing",
      searchMatching: "matching questions",
      searchQuestions: "questions",
      languageVi: "VI",
      languageEn: "EN",
      statsTracks: "Tracks",
      statsTopics: "Topics",
      statsPracticeSets: "Practice Sets",
      statsViSources: "VI Sources",
      statsEnSources: "EN Sources",
      statsStudyPaths: "Study Paths",
      statsQuestions: "Questions",
      statsCategories: "Categories",
      statsLevel: "Level",
      statsBest: "Best",
    },
    ratings: {
      excellent: "Excellent",
      good: "Good",
      fair: "Fair",
      average: "Average",
      needsReview: "Needs Review",
    },
    levels: {
      basic: "Basic",
      intermediate: "Intermediate",
      advanced: "Advanced",
      general: "General",
      "basic to advanced": "Basic to advanced",
      "basic to intermediate": "Basic to intermediate",
      "intermediate to advanced": "Intermediate to advanced",
    },
    categories: {},
    pages: {
      "interview.html": {
        title: "Code Interview Practice",
        heroPrimaryButton: "Open Code Questions",
        heroSecondaryButton: "Open Interview Sources",
        backButton: "Back to track selection",
        sectionLadders: "Code Ladders",
        sectionTopicCatalog: "Code Topic Catalog",
        sectionPracticeSets: "Code Practice Sets",
        sectionProjectIdeas: "Portfolio Project Ideas",
        sectionPrepNotes: "Preparation Notes",
      },
      "interview-questions.html": {
        title: "Basic Interview Questions",
        heroPrimaryButton: "Back to interview catalog",
        backButton: "Back to track selection",
        sectionQuestionBank: "Question Bank",
        questionBankNote:
          "Choose an answer for each question, check per-question results, then finish the quiz to get a final rating.",
        summaryAnsweredLabel: "Answered",
        summaryCorrectLabel: "Correct",
        summaryScoreLabel: "Score",
        summaryRatingLabel: "Rating",
        searchPlaceholder: "Search questions, answers, Vietnamese, English, category...",
      },
      "code-questions.html": {
        title: "Code Question Bank",
        heroPrimaryButton: "Back to code practice",
        backButton: "Back to track selection",
        sectionQuestionBank: "Code Question Bank",
        questionBankNote:
          "This page only shows code-related practice sets. Choose answers, check results, and finish the quiz for a final score.",
        summaryAnsweredLabel: "Answered",
        summaryCorrectLabel: "Correct",
        summaryScoreLabel: "Score",
        summaryRatingLabel: "Rating",
        searchPlaceholder: "Search code questions, answers, category...",
      },
      "interview-role-questions.html": {
        title: "Interview Role Question Bank",
        heroPrimaryButton: "Back to interview questions",
        backButton: "Back to track selection",
        sectionQuestionBank: "Interview Role Question Bank",
        questionBankNote:
          "This page only shows interview-style sets such as fresher, intermediate, senior, and bilingual prompts.",
        summaryAnsweredLabel: "Answered",
        summaryCorrectLabel: "Correct",
        summaryScoreLabel: "Score",
        summaryRatingLabel: "Rating",
        searchPlaceholder: "Search interview questions, Vietnamese, English, answers...",
      },
      "interview-sources.html": {
        title: "Interview Questions and Sources",
        heroPrimaryButton: "Open Fresher Questions",
        heroSecondaryButton: "Open Code Practice",
        backButton: "Back to track selection",
        sectionQuestionSets: "Interview Question Sets",
        sourcesNote:
          "This site is for interview-style question sets such as `fresher`, `intermediate`, and `senior`. Reference links are listed below for extra reading.",
        sectionVietnameseSources: "Vietnamese Reference Links",
        sectionEnglishSources: "English Reference Links",
        sectionUsageNotes: "Usage Notes",
      },
    },
  },
  vi: {
    common: {
      eyebrow: "Python Labs",
      backToTracks: "Quay lại trang chọn lộ trình",
      general: "Tổng quát",
      all: "Tất cả",
      formatStaticJson: "JSON tĩnh",
      formatStaticLinks: "Liên kết tĩnh",
      generatedAt: "Dữ liệu interview được tạo lúc",
      failedLoad: "Tải dữ liệu interview thất bại",
      level: "Cấp độ",
      focus: "Trọng tâm",
      bestFor: "Phù hợp nhất",
      examples: "Ví dụ",
      expectedDepth: "Độ sâu kỳ vọng",
      topics: "Chủ đề",
      output: "Đầu ra",
      whyItMatters: "Vì sao quan trọng",
      openSet: "Mở bộ câu hỏi",
      openQuestionSet: "Mở bộ phỏng vấn",
      openReferenceLink: "Mở liên kết tham khảo",
      noScore: "Chưa có điểm",
      inProgress: "Đang làm",
      notGraded: "Chưa chấm",
      notChecked: "Chưa kiểm tra",
      unanswered: "Chưa trả lời",
      correct: "Đúng",
      wrong: "Sai",
      compare: "So sánh",
      correctAnswer: "Đáp án đúng",
      explanation: "Giải thích",
      checkAnswer: "Kiểm tra đáp án",
      finishQuiz: "Hoàn thành bài quiz",
      resetQuiz: "Làm lại",
      searchAll: "Đang hiển thị toàn bộ câu hỏi",
      searchShowing: "Đang hiển thị",
      searchMatching: "câu hỏi khớp",
      searchQuestions: "câu hỏi",
      languageVi: "VI",
      languageEn: "EN",
      statsTracks: "Bậc luyện tập",
      statsTopics: "Chủ đề",
      statsPracticeSets: "Bộ câu hỏi",
      statsViSources: "Nguồn VI",
      statsEnSources: "Nguồn EN",
      statsStudyPaths: "Lộ trình học",
      statsQuestions: "Câu hỏi",
      statsCategories: "Danh mục",
      statsLevel: "Cấp độ",
      statsBest: "Điểm tốt nhất",
    },
    ratings: {
      excellent: "Xuất sắc",
      good: "Tốt",
      fair: "Ổn",
      average: "Trung bình",
      needsReview: "Cần ôn lại",
    },
    levels: {
      basic: "Cơ bản",
      intermediate: "Trung cấp",
      advanced: "Nâng cao",
      general: "Tổng quát",
      "basic to advanced": "Cơ bản đến nâng cao",
      "basic to intermediate": "Cơ bản đến trung cấp",
      "intermediate to advanced": "Trung cấp đến nâng cao",
    },
    categories: {
      "Python Core": "Python Cốt lõi",
      "Files and JSON": "File và JSON",
      Testing: "Kiểm thử",
      Logging: "Logging",
      CLI: "CLI",
      "HTTP APIs": "HTTP API",
      Databases: "Database",
      Automation: "Tự động hóa",
      Performance: "Hiệu năng",
      "AI/ML": "AI/ML",
      Python: "Python",
      Backend: "Backend",
      Systems: "Hệ thống",
      Architecture: "Kiến trúc",
      Messaging: "Messaging",
      Security: "Bảo mật",
      Resilience: "Độ bền",
      Deployment: "Triển khai",
      Domain: "Domain",
      Observability: "Quan sát hệ thống",
      Caching: "Caching",
      API: "API",
      Data: "Dữ liệu",
    },
    pages: {
      "interview.html": {
        title: "Luyện Phỏng Vấn Code",
        heroPrimaryButton: "Mở câu hỏi code",
        heroSecondaryButton: "Mở nguồn phỏng vấn",
        backButton: "Quay lại trang chọn lộ trình",
        sectionLadders: "Bậc luyện code",
        sectionTopicCatalog: "Danh mục chủ đề code",
        sectionPracticeSets: "Bộ câu hỏi code",
        sectionProjectIdeas: "Ý tưởng project portfolio",
        sectionPrepNotes: "Ghi chú chuẩn bị",
      },
      "interview-questions.html": {
        title: "Ngân Hàng Câu Hỏi Phỏng Vấn Cơ Bản",
        heroPrimaryButton: "Quay lại catalog phỏng vấn",
        backButton: "Quay lại trang chọn lộ trình",
        sectionQuestionBank: "Ngân hàng câu hỏi",
        questionBankNote:
          "Chọn đáp án cho từng câu, kiểm tra kết quả từng câu, rồi hoàn thành bài quiz để nhận đánh giá cuối cùng.",
        summaryAnsweredLabel: "Đã trả lời",
        summaryCorrectLabel: "Đúng",
        summaryScoreLabel: "Điểm",
        summaryRatingLabel: "Đánh giá",
        searchPlaceholder: "Tìm câu hỏi, đáp án, tiếng Việt, tiếng Anh, danh mục...",
      },
      "code-questions.html": {
        title: "Ngân Hàng Câu Hỏi Code",
        heroPrimaryButton: "Quay lại luyện code",
        backButton: "Quay lại trang chọn lộ trình",
        sectionQuestionBank: "Ngân hàng câu hỏi code",
        questionBankNote:
          "Trang này chỉ hiển thị các bộ câu hỏi liên quan đến code. Hãy chọn đáp án, xem kết quả và hoàn thành quiz để lấy điểm.",
        summaryAnsweredLabel: "Đã trả lời",
        summaryCorrectLabel: "Đúng",
        summaryScoreLabel: "Điểm",
        summaryRatingLabel: "Đánh giá",
        searchPlaceholder: "Tìm câu hỏi code, đáp án, danh mục...",
      },
      "interview-role-questions.html": {
        title: "Ngân Hàng Câu Hỏi Theo Vai Trò",
        heroPrimaryButton: "Quay lại câu hỏi phỏng vấn",
        backButton: "Quay lại trang chọn lộ trình",
        sectionQuestionBank: "Ngân hàng câu hỏi theo vai trò",
        questionBankNote:
          "Trang này hiển thị các bộ câu hỏi kiểu phỏng vấn như fresher, intermediate, senior và bộ song ngữ.",
        summaryAnsweredLabel: "Đã trả lời",
        summaryCorrectLabel: "Đúng",
        summaryScoreLabel: "Điểm",
        summaryRatingLabel: "Đánh giá",
        searchPlaceholder: "Tìm câu hỏi phỏng vấn, tiếng Việt, tiếng Anh, đáp án...",
      },
      "interview-sources.html": {
        title: "Câu Hỏi Và Nguồn Phỏng Vấn",
        heroPrimaryButton: "Mở câu hỏi fresher",
        heroSecondaryButton: "Mở luyện code",
        backButton: "Quay lại trang chọn lộ trình",
        sectionQuestionSets: "Bộ câu hỏi phỏng vấn",
        sourcesNote:
          "Trang này dành cho các bộ câu hỏi phỏng vấn như `fresher`, `intermediate` và `senior`. Các liên kết tham khảo được liệt kê bên dưới để đọc thêm.",
        sectionVietnameseSources: "Liên kết tham khảo tiếng Việt",
        sectionEnglishSources: "Liên kết tham khảo tiếng Anh",
        sectionUsageNotes: "Ghi chú sử dụng",
      },
    },
  },
};

const INTERVIEW_CONTENT_I18N = {
  vi: {
    "Code Interview Practice Site":
      "Site Luyện Phỏng Vấn Code",
    "Static code-focused interview practice from Python basics to advanced backend, automation, AI/ML, and system design implementation questions.":
      "Site luyện phỏng vấn code tĩnh, tập trung từ Python cơ bản đến các câu hỏi triển khai backend nâng cao, automation, AI/ML và system design.",
    "Code Foundations": "Nền Tảng Code",
    "Python syntax, collections, files, JSON, testing, and basic automation coding habits.":
      "Cú pháp Python, collection, file, JSON, testing và các thói quen code automation cơ bản.",
    "Implementation and APIs": "Triển Khai Và API",
    "APIs, retries, async, databases, ORM tradeoffs, automation pipelines, and debugging.":
      "API, retry, async, database, trade-off của ORM, pipeline automation và debug.",
    "Architecture and AI Systems": "Kiến Trúc Và Hệ Thống AI",
    "Scaling, observability, distributed systems, AI pipelines, retrieval, and production tradeoffs.":
      "Scaling, observability, hệ thống phân tán, pipeline AI, retrieval và các trade-off trong production.",
    "Language and Data Structures": "Ngôn Ngữ Và Cấu Trúc Dữ Liệu",
    "Questions about Python core behavior, traps, identity vs equality, mutability, and efficient use of collections.":
      "Câu hỏi về hành vi cốt lõi của Python, các bẫy thường gặp, identity so với equality, mutability và cách dùng collection hiệu quả.",
    "Scripts and File Pipelines": "Script Và Pipeline File",
    "Practical code questions around dry-run, file I/O, batch processing, idempotency, and scheduling safety.":
      "Các câu hỏi code thực tế về dry-run, file I/O, xử lý theo lô, idempotency và độ an toàn của lịch chạy.",
    "HTTP, Databases, and ORM": "HTTP, Database Và ORM",
    "Code-focused backend questions around timeouts, retries, transactions, query shaping, and caching.":
      "Các câu hỏi backend thiên về code xoay quanh timeout, retry, transaction, tối ưu query và caching.",
    "AI and Machine Learning Code Paths": "Luồng Code AI Và Machine Learning",
    "Applied questions about evaluation, leakage, embeddings, prompt templates, RAG, and model-serving tradeoffs.":
      "Các câu hỏi ứng dụng về evaluation, leakage, embedding, prompt template, RAG và trade-off khi phục vụ model.",
    "Distributed and Production Patterns": "Mẫu Phân Tán Và Production",
    "Implementation-heavy questions on queues, idempotency, retries, observability, and delivery safety.":
      "Các câu hỏi nặng về triển khai liên quan đến queue, idempotency, retry, observability và độ an toàn khi phát hành.",
    "Basic Master Set": "Bộ Master Cơ Bản",
    "Large all-in-one foundation bank with more than 100 questions.":
      "Ngân hàng nền tảng tổng hợp với hơn 100 câu hỏi trong một bộ duy nhất.",
    "Code-focused beginner practice": "Bài luyện code cho người mới bắt đầu",
    "Intermediate Master Set": "Bộ Master Trung Cấp",
    "Large implementation bank for APIs, async, databases, optimization, and data flow.":
      "Ngân hàng câu hỏi triển khai lớn về API, async, database, tối ưu và luồng dữ liệu.",
    "Mid-level code interview practice": "Bài luyện phỏng vấn code mức trung cấp",
    "Advanced Master Set": "Bộ Master Nâng Cao",
    "Large advanced bank for distributed systems, AI systems, resilience, and operations.":
      "Ngân hàng câu hỏi nâng cao lớn về hệ thống phân tán, hệ thống AI, resilience và vận hành.",
    "Hard code and architecture practice": "Bài luyện code và kiến trúc khó",
    "Automation Set": "Bộ Automation",
    "Code questions about scripting, scheduling, file pipelines, retries, and safety.":
      "Các câu hỏi code về scripting, scheduling, pipeline file, retry và an toàn vận hành.",
    "Automation-oriented code quiz": "Quiz code thiên về automation",
    "Backend and Data Set": "Bộ Backend Và Dữ Liệu",
    "Code questions for APIs, persistence, ORM behavior, caching, and query design.":
      "Các câu hỏi code về API, persistence, hành vi ORM, caching và thiết kế query.",
    "Backend implementation quiz": "Quiz triển khai backend",
    "AI and Machine Learning Set": "Bộ AI Và Machine Learning",
    "Applied AI/ML code and reasoning questions for evaluation, retrieval, prompts, and serving tradeoffs.":
      "Các câu hỏi code và suy luận AI/ML ứng dụng về evaluation, retrieval, prompt và trade-off khi serving.",
    "AI/ML technical quiz": "Quiz kỹ thuật AI/ML",
    "System Design Set": "Bộ System Design",
    "Production code and architecture questions around queues, scaling, reliability, and delivery behavior.":
      "Các câu hỏi code production và kiến trúc xoay quanh queue, scaling, reliability và hành vi phát hành.",
    "Advanced systems quiz": "Quiz hệ thống nâng cao",
    "Static Code Quiz Engine": "Bộ Máy Quiz Code Tĩnh",
    "A JSON-driven static site that turns code questions into a scored quiz without a backend.":
      "Một site tĩnh chạy bằng JSON, biến câu hỏi code thành quiz có chấm điểm mà không cần backend.",
    "Shows how to model content, scoring, and search entirely on GitHub Pages.":
      "Thể hiện cách mô hình hóa nội dung, chấm điểm và tìm kiếm hoàn toàn trên GitHub Pages.",
    "Automation Drill Lab": "Lab Luyện Automation",
    "A collection of tiny scripts and question sets around files, APIs, retries, and schedules.":
      "Một bộ script nhỏ và các bộ câu hỏi xoay quanh file, API, retry và lịch chạy.",
    "Useful for practical coding interviews that ask for scripts and operational reasoning.":
      "Hữu ích cho các buổi phỏng vấn code thực tế yêu cầu viết script và suy luận vận hành.",
    "Practice by writing and comparing code": "Luyện bằng cách viết và so sánh code",
    "Code interviews improve faster when you compare multiple implementations and explain which one is safer or faster.":
      "Phỏng vấn code tiến bộ nhanh hơn khi bạn so sánh nhiều cách triển khai và giải thích cách nào an toàn hơn hoặc nhanh hơn.",
    "Focus on bottlenecks, not only syntax": "Tập trung vào bottleneck, không chỉ cú pháp",
    "A strong answer identifies whether the real cost is in loops, I/O, queries, network calls, or external dependencies.":
      "Một câu trả lời tốt phải chỉ ra chi phí thực sự nằm ở vòng lặp, I/O, query, network call hay dependency bên ngoài.",
    "Treat failure paths as first-class": "Xem nhánh lỗi là phần hạng nhất",
    "Real code quality is often revealed by retries, validation, cleanup, and edge cases rather than the happy path.":
      "Chất lượng code thực sự thường lộ ra ở retry, validation, cleanup và edge case hơn là happy path.",
    "Fresher Interview Set": "Bộ Phỏng Vấn Fresher",
    "Interview-style fresher questions synthesized into one static quiz set with right/wrong checking.":
      "Bộ câu hỏi kiểu phỏng vấn cho fresher, được tổng hợp thành một quiz tĩnh có kiểm tra đúng/sai.",
    "Intermediate Interview Set": "Bộ Phỏng Vấn Trung Cấp",
    "Interview-style mid-level set focused on implementation choices, API design, testing, and optimization.":
      "Bộ câu hỏi kiểu phỏng vấn mức trung cấp, tập trung vào lựa chọn triển khai, thiết kế API, testing và tối ưu.",
    "Senior Interview Set": "Bộ Phỏng Vấn Senior",
    "Hard interview set for senior-level design, tradeoffs, reliability, performance, and AI/system thinking.":
      "Bộ câu hỏi khó cho senior về thiết kế, trade-off, reliability, hiệu năng và tư duy AI/hệ thống.",
    "Automation": "Automation",
    "Scripting pipelines, CLI design, scheduling, idempotency, retries, and file workflows.":
      "Pipeline scripting, thiết kế CLI, scheduling, idempotency, retry và workflow với file.",
    "Backend and Data": "Backend Và Dữ Liệu",
    "APIs, validation, SQL, transactions, ORM usage, caching, and service design basics.":
      "API, validation, SQL, transaction, cách dùng ORM, caching và nền tảng thiết kế service.",
    "AI and Machine Learning": "AI Và Machine Learning",
    "Model evaluation, embeddings, inference patterns, data leakage, RAG, and prompt reliability.":
      "Đánh giá model, embedding, mẫu inference, rò rỉ dữ liệu, RAG và độ tin cậy của prompt.",
    "System Design": "System Design",
    "Queues, idempotency, observability, failure isolation, scaling, and delivery tradeoffs.":
      "Queue, idempotency, observability, cô lập lỗi, scaling và trade-off khi phát hành.",
    "Bilingual VI/EN": "Song Ngữ VI/EN",
    "Vietnamese and English interview prompts for searching and learning in both languages.":
      "Các prompt phỏng vấn tiếng Việt và tiếng Anh để tìm kiếm và học bằng cả hai ngôn ngữ.",
    "Interview Questions and Sources Site": "Site Câu Hỏi Và Nguồn Phỏng Vấn",
    "Static interview question hub for fresher, intermediate, and senior preparation, with Vietnamese and English reference links underneath.":
      "Trung tâm câu hỏi phỏng vấn tĩnh cho lộ trình fresher, intermediate và senior, kèm các liên kết tham khảo tiếng Việt và tiếng Anh ở bên dưới.",
    "Entry-level interview quiz for Python basics, files, JSON, testing, and simple debugging.":
      "Quiz phỏng vấn đầu vào về Python cơ bản, file, JSON, testing và debug đơn giản.",
    "Mid-level interview quiz for APIs, database work, async, retries, and implementation tradeoffs.":
      "Quiz phỏng vấn mức trung cấp về API, làm việc với database, async, retry và trade-off triển khai.",
    "Hard interview quiz for scaling, reliability, architecture, operations, and AI/system tradeoffs.":
      "Quiz phỏng vấn khó về scaling, reliability, kiến trúc, vận hành và trade-off AI/hệ thống.",
    "Bilingual VI/EN Interview Set": "Bộ Phỏng Vấn Song Ngữ VI/EN",
    "Vietnamese and English interview prompts for learning terminology and answer phrasing.":
      "Các prompt phỏng vấn tiếng Việt và tiếng Anh để học thuật ngữ và cách diễn đạt câu trả lời.",
    "Interview question sets live here": "Các bộ câu hỏi phỏng vấn nằm ở đây",
    "Use this site for interview-style sets such as fresher, intermediate, senior, and bilingual interview prompts.":
      "Hãy dùng site này cho các bộ câu hỏi kiểu phỏng vấn như fresher, intermediate, senior và bộ prompt song ngữ.",
    "Reference links stay secondary": "Liên kết tham khảo chỉ là phụ",
    "External links are supporting reading only. The core practice experience should stay in the local JSON quiz sets.":
      "Các liên kết bên ngoài chỉ dùng để đọc bổ trợ. Trải nghiệm luyện tập cốt lõi nên nằm trong các bộ quiz JSON local.",
    "Read in both Vietnamese and English": "Đọc bằng cả tiếng Việt và tiếng Anh",
    "Vietnamese helps fast understanding. English helps with global terminology and real interview phrasing.":
      "Tiếng Việt giúp hiểu nhanh. Tiếng Anh giúp nắm thuật ngữ toàn cầu và cách diễn đạt thực tế khi phỏng vấn.",
  },
};

function currentFileName() {
  return window.location.pathname.split("/").pop() || "interview.html";
}

function tCommon(locale, key) {
  return INTERVIEW_I18N[locale]?.common?.[key] ?? INTERVIEW_I18N.en.common[key] ?? key;
}

function tPage(locale, key) {
  const file = currentFileName();
  return INTERVIEW_I18N[locale]?.pages?.[file]?.[key] ?? INTERVIEW_I18N.en.pages?.[file]?.[key] ?? "";
}

function translateLevel(value, locale) {
  const normalized = String(value || "").toLowerCase();
  return INTERVIEW_I18N[locale]?.levels?.[normalized] ?? value ?? "";
}

function translateCategory(value, locale) {
  return INTERVIEW_I18N[locale]?.categories?.[value] ?? value ?? tCommon(locale, "general");
}

function translateContent(value, locale) {
  if (locale !== "vi") {
    return value ?? "";
  }
  return INTERVIEW_CONTENT_I18N.vi?.[value] ?? value ?? "";
}

function translateList(values, locale) {
  if (!Array.isArray(values)) {
    return [];
  }
  return values.map((value) => translateContent(value, locale));
}

function getScoreRating(scorePercent, locale) {
  if (scorePercent >= 90) {
    return INTERVIEW_I18N[locale].ratings.excellent;
  }
  if (scorePercent >= 75) {
    return INTERVIEW_I18N[locale].ratings.good;
  }
  if (scorePercent >= 60) {
    return INTERVIEW_I18N[locale].ratings.fair;
  }
  if (scorePercent >= 40) {
    return INTERVIEW_I18N[locale].ratings.average;
  }
  return INTERVIEW_I18N[locale].ratings.needsReview;
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

function buildFallbackOptions(item, index, locale) {
  const category = String(item.category || "").toLowerCase();
  const templates =
    locale === "vi"
      ? {
          "python core": [
            "Vì Python xem các trường hợp này là tương đương trong quá trình chạy thông thường.",
            "Vì hành vi này chỉ quan trọng trong frontend chứ không phải trong chính Python.",
            "Vì interpreter luôn tự động chuyển đổi mọi thứ ở phía sau.",
          ],
          "http apis": [
            "Vì lỗi HTTP luôn được trình duyệt tự retry trong mọi trường hợp.",
            "Vì response API nội bộ thì không bao giờ cần validate.",
            "Vì status code chỉ hữu ích cho debug chứ không ảnh hưởng logic thật.",
          ],
          automation: [
            "Vì script automation nên tránh mọi cấu hình và luôn hardcode giá trị.",
            "Vì chạy lại nhiều lần luôn làm kết quả đúng hơn bất kể script làm gì.",
            "Vì logging không còn cần thiết sau khi script chạy được một lần ở máy local.",
          ],
          databases: [
            "Vì cấu trúc database hiếm khi ảnh hưởng đến hành vi ứng dụng sau khi deploy.",
            "Vì an toàn SQL hầu như không liên quan đến việc truyền tham số.",
            "Vì index chỉ giúp tăng tốc ghi chứ không giúp đọc.",
          ],
          "ai/ml": [
            "Vì không cần đánh giá model nếu điểm huấn luyện đã cao.",
            "Vì chất lượng machine learning chỉ phụ thuộc vào kích thước model chứ không phụ thuộc dữ liệu.",
            "Vì semantic retrieval loại bỏ hoàn toàn nhu cầu kiểm tra grounded answers.",
          ],
        }
      : {
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

  const generic =
    locale === "vi"
      ? [
          "Vì khác biệt này thường không tạo ra tác động thật trong hệ thống production.",
          "Vì Python hoặc framework luôn tự xử lý sự khác biệt đó trong mọi trường hợp.",
          "Vì mục tiêu chính chỉ là định dạng hiển thị chứ không phải hành vi chương trình.",
        ]
      : [
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

  const options = [item.correct_answer, distractors[0], distractors[1], distractors[2]].filter(Boolean);
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

function ensureQuestionOptions(item, index, locale) {
  if (locale === "vi" && Array.isArray(item.options_vi) && item.options_vi.length >= 2) {
    return item.options_vi;
  }
  if (Array.isArray(item.options) && item.options.length >= 2) {
    return item.options;
  }
  return buildFallbackOptions(item, index, locale);
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

function applyPageShell(locale) {
  const setText = (id, value) => {
    const node = document.getElementById(id);
    if (node && value) {
      node.textContent = value;
    }
  };

  document.documentElement.lang = locale;
  setText("eyebrow", tCommon(locale, "eyebrow"));
  setText("heroPrimaryButton", tPage(locale, "heroPrimaryButton"));
  setText("heroSecondaryButton", tPage(locale, "heroSecondaryButton"));
  setText("backButton", tPage(locale, "backButton") || tCommon(locale, "backToTracks"));
  setText("sectionLadders", tPage(locale, "sectionLadders"));
  setText("sectionTopicCatalog", tPage(locale, "sectionTopicCatalog"));
  setText("sectionPracticeSets", tPage(locale, "sectionPracticeSets"));
  setText("sectionProjectIdeas", tPage(locale, "sectionProjectIdeas"));
  setText("sectionPrepNotes", tPage(locale, "sectionPrepNotes"));
  setText("sectionQuestionBank", tPage(locale, "sectionQuestionBank"));
  setText("questionBankNote", tPage(locale, "questionBankNote"));
  setText("summaryAnsweredLabel", tPage(locale, "summaryAnsweredLabel"));
  setText("summaryCorrectLabel", tPage(locale, "summaryCorrectLabel"));
  setText("summaryScoreLabel", tPage(locale, "summaryScoreLabel"));
  setText("summaryRatingLabel", tPage(locale, "summaryRatingLabel"));
  setText("finishQuizBtn", tCommon(locale, "finishQuiz"));
  setText("resetQuizBtn", tCommon(locale, "resetQuiz"));
  setText("sectionQuestionSets", tPage(locale, "sectionQuestionSets"));
  setText("sourcesNote", tPage(locale, "sourcesNote"));
  setText("sectionVietnameseSources", tPage(locale, "sectionVietnameseSources"));
  setText("sectionEnglishSources", tPage(locale, "sectionEnglishSources"));
  setText("sectionUsageNotes", tPage(locale, "sectionUsageNotes"));

  const search = document.getElementById("questionSearch");
  if (search) {
    search.placeholder = tPage(locale, "searchPlaceholder");
  }
}

function renderCatalogStats(data, locale) {
  renderStatCards([
    [tCommon(locale, "statsTracks"), (data.ladders || []).length],
    [tCommon(locale, "statsTopics"), (data.topic_catalog || []).length],
    [tCommon(locale, "statsPracticeSets"), (data.practice_sets || []).length],
    [tCommon(locale, "output"), tCommon(locale, "formatStaticJson")],
  ]);
}

function renderSourcesStats(data, locale) {
  renderStatCards([
    [tCommon(locale, "statsViSources"), (data.vietnamese_sources || []).length],
    [tCommon(locale, "statsEnSources"), (data.english_sources || []).length],
    [tCommon(locale, "statsStudyPaths"), (data.study_paths || []).length],
    [tCommon(locale, "output"), tCommon(locale, "formatStaticLinks")],
  ]);
}

function renderQuestionStats(data, locale) {
  const questions = Array.isArray(data.questions) ? data.questions : [];
  const categories = new Set(questions.map((item) => item.category).filter(Boolean));
  const best = getBestScore(data.set_id || "default");
  renderStatCards([
    [tCommon(locale, "statsQuestions"), questions.length],
    [tCommon(locale, "statsCategories"), categories.size],
    [tCommon(locale, "statsLevel"), translateLevel(data.level || "basic", locale)],
    [tCommon(locale, "statsBest"), best ? `${best.scorePercent}%` : tCommon(locale, "noScore")],
  ]);
}

function renderCards(containerId, items, renderer) {
  const container = document.getElementById(containerId);
  if (!container || !Array.isArray(items)) {
    return;
  }
  container.innerHTML = items.map(renderer).join("");
}

function getQuestionPrompt(item, locale) {
  if (locale === "vi") {
    return item.question_vi || item.question || item.question_en || "";
  }
  return item.question_en || item.question || item.question_vi || "";
}

function renderCatalogPage(data, locale) {
  const title = document.getElementById("title");
  const subtitle = document.getElementById("subtitle");

  if (title) {
    title.textContent = tPage(locale, "title") || data.title || title.textContent;
  }
  if (subtitle) {
    subtitle.textContent = translateContent(data.subtitle || "", locale);
  }

  renderCatalogStats(data, locale);

  renderCards(
    "ladders",
    data.ladders || [],
    (item) => `
      <article class="service-card interview-card">
        <p><span class="tag category">${escapeHtml(translateLevel(item.level || "", locale))}</span></p>
        <h3>${escapeHtml(translateContent(item.name || "", locale))}</h3>
        <p>${escapeHtml(translateContent(item.summary || "", locale))}</p>
        <p><strong>${escapeHtml(tCommon(locale, "focus"))}:</strong> ${escapeHtml(translateList(item.focus || [], locale).join(", "))}</p>
      </article>
    `,
  );

  renderCards(
    "topicCatalog",
    data.topic_catalog || [],
    (item) => `
        <article class="service-card interview-card">
        <p><span class="tag">${escapeHtml(translateCategory(item.domain || "", locale))}</span></p>
        <h3>${escapeHtml(translateContent(item.title || "", locale))}</h3>
        <p>${escapeHtml(translateContent(item.summary || "", locale))}</p>
        <p><strong>${escapeHtml(tCommon(locale, "examples"))}:</strong> ${escapeHtml(translateList(item.examples || [], locale).join(", "))}</p>
        <p><strong>${escapeHtml(tCommon(locale, "expectedDepth"))}:</strong> ${escapeHtml(translateLevel(item.depth || "", locale))}</p>
      </article>
    `,
  );

  renderCards(
    "practiceSets",
    data.practice_sets || [],
    (item) => `
      <article class="service-card interview-card">
        <p><span class="level ${escapeHtml(item.level_class || "basic")}">${escapeHtml(translateLevel(item.level || "", locale))}</span></p>
        <h3>${escapeHtml(translateContent(item.name || "", locale))}</h3>
        <p>${escapeHtml(translateContent(item.summary || "", locale))}</p>
        <p><strong>${escapeHtml(tCommon(locale, "topics"))}:</strong> ${escapeHtml(translateList(item.topics || [], locale).join(", "))}</p>
        <p><strong>${escapeHtml(tCommon(locale, "output"))}:</strong> ${escapeHtml(translateContent(item.output || "", locale))}</p>
        ${item.question_set ? `<p><a class="btn" href="${escapeHtml(item.question_page || "interview-questions.html")}?set=${encodeURIComponent(item.question_set)}">${escapeHtml(tCommon(locale, "openSet"))}</a></p>` : ""}
      </article>
    `,
  );

  renderCards(
    "projectIdeas",
    data.project_ideas || [],
    (item) => `
      <article class="service-card interview-card">
        <h3>${escapeHtml(translateContent(item.name || "", locale))}</h3>
        <p>${escapeHtml(translateContent(item.summary || "", locale))}</p>
        <p><strong>${escapeHtml(tCommon(locale, "whyItMatters"))}:</strong> ${escapeHtml(translateContent(item.why || "", locale))}</p>
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
        <h3>${escapeHtml(translateContent(item.title || "", locale))}</h3>
        <p>${escapeHtml(translateContent(item.note || "", locale))}</p>
      </article>
    `,
  );
}

function renderQuestionSetLinks(registry, activeSetId, locale) {
  const container = document.getElementById("questionSetLinks");
  if (!container) {
    return;
  }

  const sets = Array.isArray(registry?.sets) ? registry.sets : [];
  const currentPage = currentFileName() || "interview-questions.html";

  container.innerHTML = sets
    .map((item) => {
      const activeClass = item.id === activeSetId ? " active-set" : "";
      return `
        <article class="service-card interview-card compact-card${activeClass}">
          <p><span class="level ${escapeHtml(item.level_class || "basic")}">${escapeHtml(translateLevel(item.level || "", locale))}</span></p>
          <h3>${escapeHtml(translateContent(item.name || "", locale))}</h3>
          <p>${escapeHtml(translateContent(item.summary || "", locale))}</p>
          <p><a class="btn" href="${escapeHtml(currentPage)}?set=${encodeURIComponent(item.id)}">${escapeHtml(tCommon(locale, "openSet"))}</a></p>
        </article>
      `;
    })
    .join("");
}

function renderInterviewSourcesPage(data, locale) {
  const title = document.getElementById("title");
  const subtitle = document.getElementById("subtitle");

  if (title) {
    title.textContent = tPage(locale, "title") || data.title || title.textContent;
  }
  if (subtitle) {
    subtitle.textContent = translateContent(data.subtitle || "", locale);
  }

  renderSourcesStats(data, locale);

  renderCards(
    "sourceQuestionSets",
    data.question_sets || [],
    (item) => `
      <article class="service-card interview-card compact-card">
        <p><span class="level ${escapeHtml(item.level_class || "basic")}">${escapeHtml(translateLevel(item.level || "", locale))}</span></p>
        <h3>${escapeHtml(translateContent(item.name || "", locale))}</h3>
        <p>${escapeHtml(translateContent(item.summary || "", locale))}</p>
        <p><a class="btn" href="${escapeHtml(item.href || "#")}">${escapeHtml(tCommon(locale, "openQuestionSet"))}</a></p>
      </article>
    `,
  );

  renderCards(
    "sourceGuides",
    data.guides || [],
    (item) => `
      <article class="service-card interview-card">
        <h3>${escapeHtml(translateContent(item.title || "", locale))}</h3>
        <p>${escapeHtml(translateContent(item.note || "", locale))}</p>
      </article>
    `,
  );

  const sourceCard = (item) => `
    <article class="source-row">
      <h3>${escapeHtml(item.name || "")}</h3>
      <p><strong>${escapeHtml(tCommon(locale, "level"))}:</strong> ${escapeHtml(translateLevel(item.level || "", locale))}</p>
      <p><strong>${escapeHtml(tCommon(locale, "focus"))}:</strong> ${escapeHtml(translateContent(item.focus || "", locale))}</p>
      <p><strong>${escapeHtml(tCommon(locale, "bestFor"))}:</strong> ${escapeHtml(translateContent(item.best_for || "", locale))}</p>
      <p><a class="btn" href="${escapeHtml(item.url || "#")}" target="_blank" rel="noreferrer">${escapeHtml(tCommon(locale, "openReferenceLink"))}</a></p>
    </article>
  `;

  renderCards("vietnameseSources", data.vietnamese_sources || [], sourceCard);
  renderCards("englishSources", data.english_sources || [], sourceCard);
}

function buildFilterButtons(categories, locale) {
  const container = document.getElementById("filters");
  if (!container) {
    return;
  }

  const allCategories = ["All", ...categories];
  container.innerHTML = allCategories
    .map(
      (category, index) => `
        <button class="filter-btn ${index === 0 ? "active" : ""}" data-category="${escapeHtml(category)}">
          ${escapeHtml(category === "All" ? tCommon(locale, "all") : translateCategory(category, locale))}
        </button>
      `,
    )
    .join("");
}

function questionCard(item, index, locale) {
  const options = ensureQuestionOptions(item, index, locale);
  const questionId = slugify(`${item.category || "question"}-${index + 1}`);
  const intent = item.intent ? `<p>${escapeHtml(item.intent)}</p>` : "";
  const categoryLabel = locale === "vi" ? item.category_vi || translateCategory(item.category || "", locale) : translateCategory(item.category || "", locale);
  const levelLabel = translateLevel(item.level || "basic", locale);
  const prompt = getQuestionPrompt(item, locale);
  const correctAnswer = locale === "vi" ? item.correct_answer_vi || item.correct_answer || "" : item.correct_answer || "";
  const explanation = locale === "vi" ? item.explanation_vi || item.explanation || "" : item.explanation || "";
  const correctAnswerEn = item.correct_answer_en || "";
  const explanationEn = item.explanation_en || "";
  const languageMarkup = "";
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
        <strong>${escapeHtml(tCommon(locale, "compare"))}:</strong>
        <ul>
          ${item.compare.map((entry) => `<li>${escapeHtml(entry)}</li>`).join("")}
        </ul>
      </div>
    `
    : "";

  const snippet = item.code_snippet ? `<pre><code>${escapeHtml(normalizeSnippet(item.code_snippet))}</code></pre>` : "";

  return `
    <article class="question-card" data-category="${escapeHtml(item.category || "")}" data-correct-answer="${escapeHtml(correctAnswer)}">
      <div class="question-meta">
        <span class="tag category">${escapeHtml(categoryLabel || tCommon(locale, "general"))}</span>
        <span class="level ${escapeHtml(item.level_class || "basic")}">${escapeHtml(levelLabel)}</span>
        <span class="question-index">Q${index + 1}</span>
      </div>
      <h3>${escapeHtml(prompt)}</h3>
      ${languageMarkup}
      ${intent}
      ${optionMarkup}
      <div class="question-actions">
        <button class="btn reveal-btn" type="button">${escapeHtml(tCommon(locale, "checkAnswer"))}</button>
        <span class="result-badge pending">${escapeHtml(tCommon(locale, "notChecked"))}</span>
      </div>
      <div class="answer-panel" hidden>
        <p><strong>${escapeHtml(tCommon(locale, "correctAnswer"))}:</strong> ${escapeHtml(correctAnswer)}</p>
        <p><strong>${escapeHtml(tCommon(locale, "explanation"))}:</strong> ${escapeHtml(explanation)}</p>
        ${snippet}
        ${comparison}
      </div>
    </article>
  `;
}

function applyQuestionFilters(locale) {
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
      ? `${tCommon(locale, "searchShowing")} ${visibleCount} ${tCommon(locale, "searchMatching")}`
      : `${tCommon(locale, "searchShowing")} ${visibleCount} ${tCommon(locale, "searchQuestions")}`;
  }
}

function evaluateQuestionCard(card, locale) {
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
      badge.textContent = tCommon(locale, "unanswered");
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
    badge.textContent = isCorrect ? tCommon(locale, "correct") : tCommon(locale, "wrong");
    badge.className = `result-badge ${isCorrect ? "correct" : "wrong"}`;
  }
  if (answerPanel) {
    answerPanel.removeAttribute("hidden");
  }

  return { answered: true, correct: isCorrect };
}

function updateQuizSummary(activeSetId, locale) {
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
  const rating = getScoreRating(scorePercent, locale);

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
    ratingNode.textContent = answered === cards.length ? rating : tCommon(locale, "inProgress");
  }

  if (answered === cards.length) {
    const best = getBestScore(activeSetId);
    if (!best || scorePercent > best.scorePercent) {
      setBestScore(activeSetId, { answered, correct, total: cards.length, scorePercent, rating });
    }
  }
}

function bindQuestionInteractions(activeSetId, data, locale) {
  const revealButtons = document.querySelectorAll(".reveal-btn");
  revealButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const card = button.closest(".question-card");
      if (!card) {
        return;
      }
      evaluateQuestionCard(card, locale);
      updateQuizSummary(activeSetId, locale);
    });
  });

  const radioInputs = document.querySelectorAll(".question-card input[type='radio']");
  radioInputs.forEach((input) => {
    input.addEventListener("change", () => {
      updateQuizSummary(activeSetId, locale);
    });
  });

  const filterButtons = document.querySelectorAll(".filter-btn");
  const cards = document.querySelectorAll(".question-card");
  filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
      filterButtons.forEach((node) => node.classList.remove("active"));
      button.classList.add("active");
      applyQuestionFilters(locale);
    });
  });

  const searchInput = document.getElementById("questionSearch");
  if (searchInput) {
    searchInput.addEventListener("input", () => {
      applyQuestionFilters(locale);
    });
  }

  const finishButton = document.getElementById("finishQuizBtn");
  if (finishButton) {
    finishButton.addEventListener("click", () => {
      let correct = 0;
      let answered = 0;
      cards.forEach((card) => {
        const result = evaluateQuestionCard(card, locale);
        if (result.answered) {
          answered += 1;
        }
        if (result.correct) {
          correct += 1;
        }
      });

      const total = cards.length || 1;
      const scorePercent = Math.round((correct / total) * 100);
      const rating = getScoreRating(scorePercent, locale);
      updateQuizSummary(activeSetId, locale);
      renderQuestionStats(data, locale);

      const setLabel = data.title || tPage(locale, "title");
      const answeredLabel = tPage(locale, "summaryAnsweredLabel") || tCommon(locale, "statsQuestions");
      const correctLabel = tPage(locale, "summaryCorrectLabel") || tCommon(locale, "correct");
      const scoreLabel = tPage(locale, "summaryScoreLabel") || tCommon(locale, "score");
      const ratingLabel = tPage(locale, "summaryRatingLabel") || "Rating";
      const completedLine = locale === "vi" ? "Hoàn thành bài quiz." : "Quiz completed.";
      const setLine = locale === "vi" ? "Bộ" : "Set";

      window.alert(
        `${completedLine}\n${setLine}: ${setLabel}\n${answeredLabel}: ${answered}/${cards.length}\n${correctLabel}: ${correct}/${cards.length}\n${scoreLabel}: ${scorePercent}%\n${ratingLabel}: ${rating}`,
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
          badge.textContent = tCommon(locale, "notChecked");
          badge.className = "result-badge pending";
        }
        const panel = card.querySelector(".answer-panel");
        if (panel) {
          panel.setAttribute("hidden", "");
        }
      });
      updateQuizSummary(activeSetId, locale);
    });
  }
}

function renderQuestionsPage(data, registry, activeSetId, locale) {
  const title = document.getElementById("title");
  const subtitle = document.getElementById("subtitle");
  const questions = Array.isArray(data.questions) ? data.questions : [];
  data.set_id = activeSetId || data.set_id || "default";

  if (title) {
    title.textContent = tPage(locale, "title") || data.title || title.textContent;
  }
  if (subtitle) {
    subtitle.textContent = translateContent(data.subtitle || "", locale);
  }

  renderQuestionStats(data, locale);
  renderQuestionSetLinks(registry, activeSetId, locale);

  const questionList = document.getElementById("questionList");
  if (questionList) {
    questionList.innerHTML = questions.map((item, index) => questionCard(item, index, locale)).join("");
    const cards = questionList.querySelectorAll(".question-card");
    cards.forEach((card, index) => {
      card.setAttribute("data-search-text", buildSearchText(questions[index]));
    });
  }

  const categories = [...new Set(questions.map((item) => item.category).filter(Boolean))];
  buildFilterButtons(categories, locale);
  bindQuestionInteractions(activeSetId, data, locale);
  updateQuizSummary(activeSetId, locale);
  applyQuestionFilters(locale);
}

async function loadQuestionSet(source, registrySource, locale) {
  const selectedSet = getQueryParam("set") || "basic";

  if (!registrySource) {
    const data = await fetchJsonWithLocale(source, locale);
    return { data, registry: null, activeSetId: selectedSet };
  }

  const registryResponse = await fetch(registrySource);
  const registry = await registryResponse.json();
  const sets = Array.isArray(registry.sets) ? registry.sets : [];
  const matched = sets.find((item) => item.id === selectedSet) || sets[0];
  const resolvedSource = matched?.file || source;
  const data = await fetchJsonWithLocale(resolvedSource, locale);
  return { data, registry, activeSetId: matched?.id || selectedSet };
}

function renderInterviewPage(page, data, registry, activeSetId, locale) {
  applyPageShell(locale);

  if (page === "interview-catalog") {
    renderCatalogPage(data, locale);
  }
  if (page === "interview-questions") {
    renderQuestionsPage(data, registry, activeSetId, locale);
  }
  if (page === "interview-sources") {
    renderInterviewSourcesPage(data, locale);
  }

  const generatedNode = document.getElementById("generatedAt");
  if (generatedNode) {
    const generatedAt = data.generated_at ? new Date(data.generated_at).toLocaleString() : "static data";
    generatedNode.textContent = `${tCommon(locale, "generatedAt")} ${generatedAt}`;
  }
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
    const payload = await loadQuestionSet(source, registrySource, getLocale());
    data = payload.data;
    registry = payload.registry;
    activeSetId = payload.activeSetId;
  } else {
    data = await fetchJsonWithLocale(source, getLocale());
  }

  const render = async () => {
    const locale = getLocale();
    if (page === "interview-questions") {
      const payload = await loadQuestionSet(source, registrySource, locale);
      data = payload.data;
      registry = payload.registry;
      activeSetId = payload.activeSetId;
    } else {
      data = await fetchJsonWithLocale(source, locale);
    }
    renderInterviewPage(page, data, registry, activeSetId, locale);
  };
  render();

  window.addEventListener("python-labs-language-change", () => {
    render();
  });
}

initInterviewSite().catch((error) => {
  const generatedNode = document.getElementById("generatedAt");
  if (generatedNode) {
    generatedNode.textContent = `${tCommon(getLocale(), "failedLoad")}: ${error}`;
  }
});
