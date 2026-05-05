#!/usr/bin/env python3
"""Build metadata and learning tracks for the Python Labs portal."""

from __future__ import annotations

import ast
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SERVICES_DIR = ROOT_DIR / "services"
SITE_DATA_DIR = ROOT_DIR / "site" / "data"

CATALOG_FILE = SITE_DATA_DIR / "catalog.json"
FOUNDATION_FILE = SITE_DATA_DIR / "foundation.json"
ADVANCED_FILE = SITE_DATA_DIR / "advanced.json"

ENTRYPOINT_PRIORITY = ["main.py", "app.py", "index.py", "run.py", "server.py", "test.py"]
IGNORE_PARTS = {"__pycache__", ".venv", "venv", ".git", "node_modules"}

TOPIC_MAP = {
    "ai-search-engine": ["web scraping", "search workflow", "performance measurement"],
    "basic-bot": ["OpenAI API basics", "prompting", "script automation"],
    "box-browser": ["GUI automation", "desktop integration"],
    "calculator-gradient-image": ["image processing", "numerical operations"],
    "composio": ["API orchestration", "automation workflows", "template rendering"],
    "crypto-bot": ["telegram bot", "schedulers", "external APIs", "testing"],
    "download-video": ["HTTP download", "CLI scripts"],
    "dropshipping-bot": ["service architecture", "configuration management"],
    "get-data": ["data collection", "HTTP requests"],
    "nft-ai-bot": ["AI image generation", "environment variables", "HTTP APIs"],
    "smart-contract": ["web3", "blockchain transactions", "contract deployment"],
}

STDLIB_MODULES = {
    "ast",
    "collections",
    "datetime",
    "json",
    "logging",
    "os",
    "pathlib",
    "sys",
    "time",
    "timeit",
    "typing",
}


FOUNDATION_CHEATSHEET = [
    {
        "category": "Syntax",
        "title": "Variables and Naming",
        "summary": "Use snake_case and keep names semantic.",
        "snippet": "user_name = 'ThanhSon99'\\nmax_retries = 3\\nis_ready = False",
        "application": "Readable scripts and maintainable configs.",
        "tags": ["variables", "style"],
    },
    {
        "category": "Syntax",
        "title": "Core Data Types",
        "summary": "Know list, tuple, dict, set tradeoffs.",
        "snippet": "skills = ['python', 'sql']\\nprofile = {'name': 'A', 'exp': 2}\\nunique_ids = {1, 2, 3}",
        "application": "Modeling incoming API payloads.",
        "tags": ["types", "collections"],
    },
    {
        "category": "Syntax",
        "title": "Conditionals",
        "summary": "Guard invalid states early.",
        "snippet": "if not token:\\n    raise ValueError('missing token')\\nelif token == 'dev':\\n    mode = 'sandbox'",
        "application": "Input validation before requests.",
        "tags": ["if", "validation"],
    },
    {
        "category": "Syntax",
        "title": "Loops",
        "summary": "Prefer enumerate for index + item.",
        "snippet": "for idx, item in enumerate(items, start=1):\\n    print(idx, item)",
        "application": "Batch processing + progress logs.",
        "tags": ["for", "iteration"],
    },
    {
        "category": "Functions",
        "title": "Function Design",
        "summary": "One purpose per function, explicit return.",
        "snippet": "def build_url(host, path):\\n    return f'{host.rstrip('/')}/{path.lstrip('/')}'",
        "application": "Reusable helper utilities.",
        "tags": ["functions", "clean-code"],
    },
    {
        "category": "Functions",
        "title": "Default Arguments",
        "summary": "Avoid mutable defaults.",
        "snippet": "def add_tag(tag, tags=None):\\n    tags = [] if tags is None else tags\\n    tags.append(tag)\\n    return tags",
        "application": "Prevent shared-state bugs.",
        "tags": ["functions", "pitfalls"],
    },
    {
        "category": "Functions",
        "title": "Lambda and sorted",
        "summary": "Keep lambdas short and obvious.",
        "snippet": "users = sorted(users, key=lambda x: x['score'], reverse=True)",
        "application": "Ranking and quick transforms.",
        "tags": ["lambda", "sorting"],
    },
    {
        "category": "Docs",
        "title": "Docstring Convention",
        "summary": "Document args, returns, and raises.",
        "snippet": "def fetch(url):\\n    \"\"\"Fetch JSON data.\\n\\n    Args:\\n        url: endpoint URL\\n    Returns:\\n        dict payload\\n    \"\"\"",
        "application": "Faster onboarding and IDE hints.",
        "tags": ["docstring", "documentation"],
    },
    {
        "category": "Docs",
        "title": "Useful Comments",
        "summary": "Explain why, not what.",
        "snippet": "# Keep 2 retries only to avoid duplicate external charges",
        "application": "Capture domain decision context.",
        "tags": ["comments", "code-review"],
    },
    {
        "category": "Imports",
        "title": "Import Ordering",
        "summary": "stdlib, third-party, local modules.",
        "snippet": "import json\\nfrom pathlib import Path\\n\\nimport requests\\n\\nfrom .client import ApiClient",
        "application": "Consistent project hygiene.",
        "tags": ["imports", "structure"],
    },
    {
        "category": "Error Handling",
        "title": "try/except/finally",
        "summary": "Catch specific exceptions.",
        "snippet": "try:\\n    payload = response.json()\\nexcept ValueError as exc:\\n    logger.error('invalid json: %s', exc)\\nfinally:\\n    response.close()",
        "application": "Safe API and file handling.",
        "tags": ["exceptions", "reliability"],
    },
    {
        "category": "Error Handling",
        "title": "Custom Exceptions",
        "summary": "Model domain-level failures.",
        "snippet": "class PaymentDeclinedError(Exception):\\n    pass",
        "application": "Clear service contracts.",
        "tags": ["exceptions", "domain"],
    },
    {
        "category": "Data",
        "title": "List Comprehension",
        "summary": "Compact mapping + filtering.",
        "snippet": "valid_ids = [u['id'] for u in users if u.get('active')]",
        "application": "Transform API lists quickly.",
        "tags": ["list", "comprehension"],
    },
    {
        "category": "Data",
        "title": "Dict Get and Defaults",
        "summary": "Avoid KeyError in partial payloads.",
        "snippet": "country = profile.get('address', {}).get('country', 'unknown')",
        "application": "Resilient JSON parsing.",
        "tags": ["dict", "json"],
    },
    {
        "category": "Data",
        "title": "Dataclasses",
        "summary": "Typed lightweight data models.",
        "snippet": "from dataclasses import dataclass\\n\\n@dataclass\\nclass User:\\n    id: int\\n    email: str",
        "application": "Internal DTO for service layers.",
        "tags": ["dataclass", "typing"],
    },
    {
        "category": "Files",
        "title": "Pathlib",
        "summary": "Use Path instead of raw strings.",
        "snippet": "from pathlib import Path\\nreport = Path('data') / 'report.json'\\nreport.parent.mkdir(exist_ok=True)",
        "application": "Cross-platform file paths.",
        "tags": ["pathlib", "filesystem"],
    },
    {
        "category": "Files",
        "title": "JSON IO",
        "summary": "Always set encoding and pretty indent for debug files.",
        "snippet": "with open('out.json', 'w', encoding='utf-8') as f:\\n    json.dump(payload, f, ensure_ascii=False, indent=2)",
        "application": "Audit logs and debug snapshots.",
        "tags": ["json", "io"],
    },
    {
        "category": "Database",
        "title": "SQLite Connection",
        "summary": "Simple local database for scripts and prototypes.",
        "snippet": "import sqlite3\\nconn = sqlite3.connect('app.db')\\ncur = conn.cursor()\\ncur.execute('SELECT 1')\\nconn.close()",
        "application": "Quick local persistence without external services.",
        "tags": ["sqlite", "database"],
    },
    {
        "category": "Database",
        "title": "PostgreSQL via SQLAlchemy",
        "summary": "Use engine + session factory for clean data access.",
        "snippet": "from sqlalchemy import create_engine\\nfrom sqlalchemy.orm import sessionmaker\\nengine = create_engine('postgresql+psycopg://user:pass@localhost:5432/app')\\nSession = sessionmaker(bind=engine)\\nsession = Session()",
        "application": "Production-ready relational database integration.",
        "tags": ["postgresql", "sqlalchemy"],
    },
    {
        "category": "Database",
        "title": "Connection URL from Environment",
        "summary": "Never hardcode credentials in source files.",
        "snippet": "db_url = os.getenv('DATABASE_URL')\\nif not db_url:\\n    raise RuntimeError('DATABASE_URL is required')",
        "application": "Secure and portable environment-specific configuration.",
        "tags": ["database", "env", "security"],
    },
    {
        "category": "HTTP",
        "title": "Requests with Timeout",
        "summary": "Never call API without timeout.",
        "snippet": "response = requests.get(url, timeout=15)\\nresponse.raise_for_status()",
        "application": "Avoid hanging worker processes.",
        "tags": ["requests", "api"],
    },
    {
        "category": "HTTP",
        "title": "Retry Pattern",
        "summary": "Retry only idempotent operations.",
        "snippet": "for _ in range(3):\\n    try:\\n        return client.get()\\n    except TimeoutError:\\n        time.sleep(1)",
        "application": "Handle unstable providers.",
        "tags": ["retry", "resilience"],
    },
    {
        "category": "CLI",
        "title": "argparse",
        "summary": "Build scripts with clear flags.",
        "snippet": "parser.add_argument('--limit', type=int, default=50)\\nargs = parser.parse_args()",
        "application": "Reusable local automations.",
        "tags": ["cli", "argparse"],
    },
    {
        "category": "Environment",
        "title": "Environment Variables",
        "summary": "Load secrets from env, not code.",
        "snippet": "api_key = os.getenv('OPENAI_API_KEY')\\nif not api_key:\\n    raise RuntimeError('missing OPENAI_API_KEY')",
        "application": "Secure config handling.",
        "tags": ["env", "security"],
    },
    {
        "category": "Logging",
        "title": "Structured Logging",
        "summary": "Log context-rich messages.",
        "snippet": "logger.info('sync completed', extra={'service': 'crypto', 'count': 42})",
        "application": "Easier incident debugging.",
        "tags": ["logging", "observability"],
    },
    {
        "category": "Testing",
        "title": "pytest Basics",
        "summary": "Arrange, Act, Assert pattern.",
        "snippet": "def test_add():\\n    assert add(2, 3) == 5",
        "application": "Prevent regression in helpers.",
        "tags": ["pytest", "qa"],
    },
    {
        "category": "Testing",
        "title": "Mock External Calls",
        "summary": "Patch network clients in tests.",
        "snippet": "@patch('module.requests.get')\\ndef test_fetch(mock_get):\\n    ...",
        "application": "Fast stable CI without network.",
        "tags": ["mock", "testing"],
    },
    {
        "category": "Packaging",
        "title": "requirements Discipline",
        "summary": "Pin critical versions for stability.",
        "snippet": "requests==2.32.3\\npython-dotenv==1.0.1",
        "application": "Reproducible environments.",
        "tags": ["dependencies", "packaging"],
    },
    {
        "category": "Performance",
        "title": "Generator",
        "summary": "Use generators for large streams.",
        "snippet": "def read_lines(path):\\n    with open(path) as f:\\n        for line in f:\\n            yield line.strip()",
        "application": "Memory-efficient pipelines.",
        "tags": ["performance", "generator"],
    },
    {
        "category": "Concurrency",
        "title": "ThreadPoolExecutor",
        "summary": "Parallelize IO-bound workloads.",
        "snippet": "with ThreadPoolExecutor(max_workers=8) as ex:\\n    results = list(ex.map(fetch, urls))",
        "application": "Bulk HTTP fetching.",
        "tags": ["concurrency", "io"],
    },
    {
        "category": "Typing",
        "title": "Type Hints",
        "summary": "Annotate public interfaces.",
        "snippet": "def normalize(amount: float, currency: str) -> float:\\n    return round(amount, 2)",
        "application": "Static analysis and safer refactor.",
        "tags": ["typing", "quality"],
    },
    {
        "category": "Project",
        "title": "Module Layout",
        "summary": "Separate config, core logic, adapters.",
        "snippet": "service/\\n  config.py\\n  adapters/\\n  core/\\n  app.py",
        "application": "Microservice-ready structure.",
        "tags": ["architecture", "layout"],
    },
    {
        "category": "Security",
        "title": "Input Sanitization",
        "summary": "Validate and normalize user data early.",
        "snippet": "email = email.strip().lower()\\nif '@' not in email:\\n    raise ValueError('invalid email')",
        "application": "Avoid bad records and injection paths.",
        "tags": ["security", "validation"],
    },
    {
        "category": "Workflow",
        "title": "Pre-Commit Checks",
        "summary": "Run format, lint, test before commit.",
        "snippet": "python -m py_compile scripts/build_site.py\\npytest -q",
        "application": "Higher merge confidence.",
        "tags": ["workflow", "quality"],
    },
]

ADVANCED_CHEATSHEET = [
    {
        "category": "Architecture",
        "title": "Layered Service",
        "summary": "Transport -> application -> domain -> infrastructure.",
        "snippet": "api -> use_case -> domain_model -> repository",
        "application": "Keep business logic framework-agnostic.",
        "tags": ["architecture", "clean"],
    },
    {
        "category": "Architecture",
        "title": "Hexagonal Ports/Adapters",
        "summary": "Define ports as interfaces; adapters integrate vendors.",
        "snippet": "class PriceFeedPort(Protocol):\\n    def latest(self, symbol: str) -> float: ...",
        "application": "Swap API providers without core rewrite.",
        "tags": ["ports", "adapters"],
    },
    {
        "category": "Messaging",
        "title": "RabbitMQ",
        "summary": "Queue-based work distribution for tasks.",
        "snippet": "aio-pika / pika + dead-letter queue + retry headers",
        "application": "Email, image generation, asynchronous jobs.",
        "tags": ["rabbitmq", "queue"],
    },
    {
        "category": "Messaging",
        "title": "Kafka",
        "summary": "Event streaming and durable logs.",
        "snippet": "aiokafka producer/consumer + partitioned topics",
        "application": "Audit streams, analytics, CDC pipelines.",
        "tags": ["kafka", "stream"],
    },
    {
        "category": "Messaging",
        "title": "Redis Streams",
        "summary": "Lightweight stream + consumer groups.",
        "snippet": "XADD / XREADGROUP for event fan-out",
        "application": "Smaller event-driven systems.",
        "tags": ["redis", "stream"],
    },
    {
        "category": "Task Processing",
        "title": "Celery",
        "summary": "Distributed task queue with retries and scheduling.",
        "snippet": "@celery.task(bind=True, autoretry_for=(Exception,), retry_backoff=True)",
        "application": "Long-running async jobs in production.",
        "tags": ["celery", "workers"],
    },
    {
        "category": "Task Processing",
        "title": "Dramatiq / RQ",
        "summary": "Simpler alternatives for background workers.",
        "snippet": "@dramatiq.actor(max_retries=5)",
        "application": "Small and medium queue workloads.",
        "tags": ["dramatiq", "rq"],
    },
    {
        "category": "API",
        "title": "FastAPI",
        "summary": "Typed REST APIs with OpenAPI generation.",
        "snippet": "@app.get('/health')\\ndef health() -> dict[str, str]:\\n    return {'status': 'ok'}",
        "application": "Service endpoints + docs first workflow.",
        "tags": ["fastapi", "api"],
    },
    {
        "category": "API",
        "title": "gRPC",
        "summary": "Binary RPC for internal service-to-service traffic.",
        "snippet": "protobuf contracts + generated Python stubs",
        "application": "Low latency internal microservice calls.",
        "tags": ["grpc", "protobuf"],
    },
    {
        "category": "Data",
        "title": "SQLAlchemy 2",
        "summary": "Unit-of-work and repository patterns.",
        "snippet": "session.execute(select(User).where(User.id == uid)).scalar_one_or_none()",
        "application": "Reliable relational data layer.",
        "tags": ["sqlalchemy", "postgres"],
    },
    {
        "category": "Data",
        "title": "Alembic Migrations",
        "summary": "Version schema changes safely.",
        "snippet": "alembic revision --autogenerate -m 'add event table'",
        "application": "Zero-surprise database deployment.",
        "tags": ["alembic", "migration"],
    },
    {
        "category": "Data",
        "title": "Async DB Access",
        "summary": "Use async driver for high-concurrency APIs.",
        "snippet": "asyncpg / sqlalchemy.ext.asyncio",
        "application": "I/O heavy API services.",
        "tags": ["async", "database"],
    },
    {
        "category": "Caching",
        "title": "Redis Cache Aside",
        "summary": "Read-through with TTL and invalidation rules.",
        "snippet": "value = redis.get(key) or load_from_db()",
        "application": "Reduce DB load and response latency.",
        "tags": ["redis", "cache"],
    },
    {
        "category": "Observability",
        "title": "Metrics",
        "summary": "Expose Prometheus counters and histograms.",
        "snippet": "REQUEST_LATENCY.labels(route='/verify').observe(seconds)",
        "application": "SLO tracking and alerting.",
        "tags": ["prometheus", "metrics"],
    },
    {
        "category": "Observability",
        "title": "Tracing",
        "summary": "Propagate trace-id across services.",
        "snippet": "OpenTelemetry instrumentation + OTLP exporter",
        "application": "Debug distributed latency spikes.",
        "tags": ["otel", "tracing"],
    },
    {
        "category": "Observability",
        "title": "Structured Logs",
        "summary": "JSON logs with correlation id.",
        "snippet": "{'trace_id': tid, 'event': 'order_confirmed', 'service': 'billing'}",
        "application": "Centralized log analysis (ELK/Loki).",
        "tags": ["logs", "json"],
    },
    {
        "category": "Security",
        "title": "JWT and Key Rotation",
        "summary": "Use short token expiry and rotate signing keys.",
        "snippet": "kid-based key set + refresh token revocation list",
        "application": "Auth in microservice gateways.",
        "tags": ["jwt", "auth"],
    },
    {
        "category": "Security",
        "title": "Secrets Management",
        "summary": "Keep secrets outside image and repo.",
        "snippet": "Vault / AWS Secrets Manager / Doppler",
        "application": "Secure production config.",
        "tags": ["secrets", "ops"],
    },
    {
        "category": "Security",
        "title": "Rate Limit",
        "summary": "Protect endpoints from abuse.",
        "snippet": "token bucket by IP/API key",
        "application": "Public API hardening.",
        "tags": ["rate-limit", "api"],
    },
    {
        "category": "Resilience",
        "title": "Circuit Breaker",
        "summary": "Trip on repeated downstream failures.",
        "snippet": "closed -> open -> half-open states",
        "application": "Prevent cascading outages.",
        "tags": ["circuit-breaker", "reliability"],
    },
    {
        "category": "Resilience",
        "title": "Idempotency Key",
        "summary": "Handle duplicate retry requests safely.",
        "snippet": "X-Idempotency-Key persisted with response hash",
        "application": "Payments and order APIs.",
        "tags": ["idempotency", "api"],
    },
    {
        "category": "Resilience",
        "title": "Outbox Pattern",
        "summary": "Publish events reliably with DB transaction.",
        "snippet": "write business row + outbox row in same tx",
        "application": "Avoid lost events after commit.",
        "tags": ["outbox", "event-driven"],
    },
    {
        "category": "Deployment",
        "title": "Docker Multi-stage",
        "summary": "Slim production image with pinned base.",
        "snippet": "builder stage installs deps, runtime stage runs app",
        "application": "Fast CI and smaller attack surface.",
        "tags": ["docker", "deployment"],
    },
    {
        "category": "Deployment",
        "title": "Kubernetes Basics",
        "summary": "Use Deployment, Service, ConfigMap, Secret, HPA.",
        "snippet": "readinessProbe + livenessProbe + resource limits",
        "application": "Scalable service orchestration.",
        "tags": ["k8s", "cloud"],
    },
    {
        "category": "Deployment",
        "title": "Blue/Green + Canary",
        "summary": "Gradual rollout strategy reduces blast radius.",
        "snippet": "10% traffic canary then full promotion",
        "application": "Safer releases for critical APIs.",
        "tags": ["release", "sre"],
    },
    {
        "category": "Testing",
        "title": "Contract Testing",
        "summary": "Verify API compatibility between services.",
        "snippet": "consumer-driven contracts (Pact) in CI",
        "application": "Microservice integration stability.",
        "tags": ["contract", "testing"],
    },
    {
        "category": "Testing",
        "title": "Load Testing",
        "summary": "Measure throughput and latency budget.",
        "snippet": "k6 scenarios with p95 and p99 thresholds",
        "application": "Capacity planning before launch.",
        "tags": ["performance", "load-test"],
    },
    {
        "category": "CI/CD",
        "title": "Pipeline Gates",
        "summary": "lint -> unit -> integration -> security scan -> deploy",
        "snippet": "fail fast on quality gates",
        "application": "Reliable automated release process.",
        "tags": ["cicd", "devops"],
    },
    {
        "category": "Domain",
        "title": "Event Modeling",
        "summary": "Name events in business language.",
        "snippet": "user_registered, payment_authorized, order_shipped",
        "application": "Clear event-driven design.",
        "tags": ["ddd", "events"],
    },
    {
        "category": "Domain",
        "title": "Saga Pattern",
        "summary": "Coordinate distributed transactions.",
        "snippet": "reserve -> charge -> confirm / compensate",
        "application": "Order + payment orchestration.",
        "tags": ["saga", "distributed"],
    },
]


def _iter_python_files(service_dir: Path) -> list[Path]:
    files: list[Path] = []
    for path in service_dir.rglob("*.py"):
        if any(part in IGNORE_PARTS for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def _detect_entrypoint(python_files: list[Path]) -> str | None:
    by_name = {path.name: path for path in python_files}
    for name in ENTRYPOINT_PRIORITY:
        if name in by_name:
            return str(by_name[name].relative_to(ROOT_DIR))
    for path in python_files:
        if path.name != "__init__.py":
            return str(path.relative_to(ROOT_DIR))
    if python_files:
        return str(python_files[0].relative_to(ROOT_DIR))
    return None


def _parse_imports(path: Path) -> list[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
    except SyntaxError:
        return []

    modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.append(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.append(node.module.split(".")[0])
    return modules


def _read_requirements(service_dir: Path) -> list[str]:
    req_file = service_dir / "requirements.txt"
    if not req_file.exists():
        return []

    deps: list[str] = []
    for line in req_file.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.lower().startswith("pip install "):
            line = line[12:].strip()
            for part in line.split():
                if part and not part.startswith("-"):
                    deps.append(part)
            continue
        base = line.split("==")[0].split(">=")[0].split("<=")[0].strip()
        if base:
            deps.append(base)
    return deps


def _guess_level(service_name: str, file_count: int, dep_count: int) -> str:
    advanced_names = {"crypto-bot", "smart-contract", "dropshipping-bot", "composio"}
    intermediate_names = {"ai-search-engine", "nft-ai-bot", "calculator-gradient-image"}

    if service_name.lower() in advanced_names or dep_count >= 8 or file_count >= 15:
        return "advanced"
    if service_name.lower() in intermediate_names or dep_count >= 4 or file_count >= 6:
        return "intermediate"
    return "basic"


def _load_services() -> list[dict]:
    services: list[dict] = []
    for service_dir in sorted(SERVICES_DIR.iterdir()):
        if not service_dir.is_dir() or service_dir.name.startswith("."):
            continue

        python_files = _iter_python_files(service_dir)
        imports = Counter()
        for py in python_files:
            imports.update(_parse_imports(py))

        requirements = _read_requirements(service_dir)
        local_modules = {p.stem for p in python_files if p.name != "__init__.py"}
        top_imports = [
            module
            for module, _ in imports.most_common(30)
            if module not in STDLIB_MODULES and module not in local_modules and module != service_dir.name
        ]

        services.append(
            {
                "name": service_dir.name,
                "path": str(service_dir.relative_to(ROOT_DIR)),
                "entrypoint": _detect_entrypoint(python_files),
                "python_files": len(python_files),
                "requirements": requirements,
                "tech_stack": sorted(set(requirements + top_imports))[:18],
                "topics": TOPIC_MAP.get(service_dir.name.lower(), ["python scripting", "module structure"]),
                "level": _guess_level(service_dir.name, len(python_files), len(requirements)),
            }
        )

    return services


def _build_catalog(services: list[dict], generated_at: str) -> dict:
    level_counts = Counter(service["level"] for service in services)
    return {
        "generated_at": generated_at,
        "overview": {
            "service_count": len(services),
            "basic_count": level_counts.get("basic", 0),
            "intermediate_count": level_counts.get("intermediate", 0),
            "advanced_count": level_counts.get("advanced", 0),
        },
        "services": services,
    }


def _build_foundation_track(services: list[dict], generated_at: str) -> dict:
    beginner_services = [s for s in services if s["level"] in {"basic", "intermediate"}]
    roadmap = [
        {
            "stage": "Stage 1: Python Core",
            "goals": [
                "variables, data types, operators",
                "if/else, loops, functions",
                "comments and docstrings",
                "imports and module basics",
            ],
            "build": ["CLI calculator", "json parser", "file reader tool"],
            "tools": ["python", "venv", "pip", "argparse"],
            "example_path": "learning-path/foundation/stage-01-python-core",
            "example_file": "learning-path/foundation/stage-01-python-core/main.py",
        },
        {
            "stage": "Stage 2: Data and Files",
            "goals": [
                "dict/list/set patterns",
                "json and csv processing",
                "pathlib and filesystem safety",
                "basic performance with comprehensions",
            ],
            "build": ["daily report generator", "data cleaner", "batch rename script"],
            "tools": ["json", "csv", "pathlib", "collections"],
            "example_path": "learning-path/foundation/stage-02-data-and-files",
            "example_file": "learning-path/foundation/stage-02-data-and-files/transform_data.py",
        },
        {
            "stage": "Stage 3: API Integrations",
            "goals": [
                "requests + timeouts",
                "error handling and retries",
                "environment variable config",
                "simple logging strategy",
            ],
            "build": ["weather cli", "currency monitor", "rss news collector"],
            "tools": ["requests", "python-dotenv", "logging"],
            "example_path": "learning-path/foundation/stage-03-api-integrations",
            "example_file": "learning-path/foundation/stage-03-api-integrations/api_client.py",
        },
        {
            "stage": "Stage 4: Project Structure",
            "goals": [
                "split config/core/adapters",
                "remove duplicated utilities",
                "create reusable modules",
                "manage requirements per service",
            ],
            "build": ["mini service template", "shared utils package"],
            "tools": ["pip", "pytest", "ruff", "black"],
            "example_path": "learning-path/foundation/stage-04-project-structure",
            "example_file": "learning-path/foundation/stage-04-project-structure/app/main.py",
        },
        {
            "stage": "Stage 5: Intermediate Automation",
            "goals": [
                "schedule scripts",
                "consume third-party APIs",
                "produce markdown/html reports",
                "use lightweight tests",
            ],
            "build": ["market tracker", "auto summary bot", "alert scheduler"],
            "tools": ["apscheduler", "jinja2", "pytest"],
            "example_path": "learning-path/foundation/stage-05-intermediate-automation",
            "example_file": "learning-path/foundation/stage-05-intermediate-automation/scheduler_demo.py",
        },
        {
            "stage": "Stage 6: API Service Basics",
            "goals": [
                "build CRUD API",
                "use pydantic validation",
                "add health and readiness endpoints",
                "introduce simple middleware",
            ],
            "build": ["task api", "auth prototype", "service status board"],
            "tools": ["fastapi", "uvicorn", "pydantic"],
            "example_path": "learning-path/foundation/stage-06-api-service-basics",
            "example_file": "learning-path/foundation/stage-06-api-service-basics/mini_api.py",
        },
        {
            "stage": "Stage 7: Storage",
            "goals": [
                "sql fundamentals",
                "orm usage",
                "migrations",
                "indexes and query tuning basics",
                "connection pooling and transaction safety",
            ],
            "build": ["inventory service", "blog backend"],
            "tools": ["postgresql", "sqlalchemy", "alembic"],
            "example_path": "learning-path/foundation/stage-07-storage",
            "example_file": "learning-path/foundation/stage-07-storage/sqlite_example.py",
        },
        {
            "stage": "Stage 8: Async and Concurrency",
            "goals": [
                "threadpool vs async",
                "I/O bound tuning",
                "background worker basics",
                "graceful shutdown",
            ],
            "build": ["bulk fetcher", "parallel scraper", "async notifier"],
            "tools": ["asyncio", "httpx", "concurrent.futures"],
            "example_path": "learning-path/foundation/stage-08-async-and-concurrency",
            "example_file": "learning-path/foundation/stage-08-async-and-concurrency/async_demo.py",
        },
        {
            "stage": "Stage 9: Testing and Quality",
            "goals": [
                "unit + integration tests",
                "test doubles/mocks",
                "code coverage",
                "pre-commit automation",
            ],
            "build": ["test harness for one service"],
            "tools": ["pytest", "coverage", "pre-commit"],
            "example_path": "learning-path/foundation/stage-09-testing-and-quality",
            "example_file": "learning-path/foundation/stage-09-testing-and-quality/math_utils.py",
        },
        {
            "stage": "Stage 10: Delivery",
            "goals": [
                "dockerize one service",
                "config by environment",
                "basic CI pipeline",
                "release notes and changelog",
            ],
            "build": ["dockerized api + ci"],
            "tools": ["docker", "github actions", "makefile"],
            "example_path": "learning-path/foundation/stage-10-delivery",
            "example_file": "",
        },
    ]

    open_source_stacks = [
        {
            "name": "FastAPI Starter",
            "use_case": "Typed REST APIs with automatic docs.",
            "packages": ["fastapi", "uvicorn", "pydantic"],
        },
        {
            "name": "Data Layer Starter",
            "use_case": "Relational persistence and migrations.",
            "packages": ["sqlalchemy", "alembic", "psycopg"],
        },
        {
            "name": "Caching Starter",
            "use_case": "Low-latency reads and temporary state.",
            "packages": ["redis", "hiredis"],
        },
        {
            "name": "Background Jobs Starter",
            "use_case": "Async tasks and periodic workers.",
            "packages": ["celery", "redis", "apscheduler"],
        },
        {
            "name": "Quality Starter",
            "use_case": "Linting, formatting, and tests.",
            "packages": ["pytest", "ruff", "black", "mypy"],
        },
    ]

    mini_projects = [
        {
            "name": "Foundation Milestone 1: CLI Data Toolkit",
            "path": "learning-path/projects/foundation-cli-data-toolkit",
            "focus": "Core syntax + data transformations + file outputs",
            "stack": ["python", "argparse", "json", "pathlib"],
        },
        {
            "name": "Foundation Milestone 2: API + Storage Service",
            "path": "learning-path/projects/foundation-api-storage-service",
            "focus": "HTTP endpoint + persistence + tests",
            "stack": ["http.server", "sqlite3", "pytest"],
        },
    ]

    extra_examples = [
        {"title": "Decorators", "path": "learning-path/foundation/extras/decorators/example.py"},
        {"title": "Context Managers", "path": "learning-path/foundation/extras/context-managers/example.py"},
        {"title": "itertools + regex", "path": "learning-path/foundation/extras/itertools-regex/example.py"},
        {"title": "argparse subcommands", "path": "learning-path/foundation/extras/argparse-subcommands/example.py"},
        {"title": "logging config", "path": "learning-path/foundation/extras/logging-config/example.py"},
        {"title": "CSV advanced", "path": "learning-path/foundation/extras/csv-advanced/example.py"},
        {"title": "pathlib advanced", "path": "learning-path/foundation/extras/pathlib-advanced/example.py"},
        {"title": "typing generics", "path": "learning-path/foundation/extras/typing-generics/example.py"},
        {"title": "dataclass validation", "path": "learning-path/foundation/extras/dataclass-validation/example.py"},
        {"title": "error patterns", "path": "learning-path/foundation/extras/error-patterns/example.py"},
    ]

    database_practicals = [
        {"title": "PostgreSQL local (Docker)", "path": "learning-path/database/postgres-local/docker-compose.yml"},
        {"title": "PostgreSQL connection check", "path": "learning-path/database/postgres-local/check_connection.py"},
        {"title": "Alembic demo", "path": "learning-path/database/alembic-demo/README.md"},
        {"title": "Indexing and query plan", "path": "learning-path/database/indexing-query-plan/example.sql"},
        {"title": "Isolation notes", "path": "learning-path/database/isolation-demo/example.py"},
        {"title": "Connection pool demo", "path": "learning-path/database/pool-demo/example.py"},
    ]

    foundation_ui_en = {
        "hero": {
            "eyebrow": "Python Labs",
            "back_to_tracks": "Back to track selection",
            "example_root": "Example root",
            "static_note": "Static hosting mode: GitHub Pages can browse the roadmap and examples without the Python runner API.",
            "local_runner_enabled": "Local runner is available on localhost.",
        },
        "sections": {
            "cheat_sheets": "Cheat Sheet Library",
            "roadmap": "Roadmap",
            "mini_projects": "Mini Projects",
            "database_practicals": "Database Practicals",
            "extra_examples": "Extra Example Library",
            "open_source_stacks": "Open-Source Integration Stacks",
            "recommended_services": "Recommended Services",
        },
        "stats": {
            "cheat_items": "Cheat Items",
            "roadmap_stages": "Roadmap Stages",
            "completed": "Completed",
            "track": "Track",
        },
        "fields": {
            "application": "Application",
            "goals": "Goals",
            "build": "Build",
            "tools": "Tools",
            "example_code": "Example code",
            "path": "Path",
            "focus": "Focus",
            "entrypoint": "Entrypoint",
            "topics": "Topics",
            "use_case": "Use case",
            "java": "Java",
            "python": "Python",
            "when": "Use when",
            "scope": "Scope",
        },
        "roadmap": {
            "mark_completed": "Mark completed",
            "run_example": "Run example",
            "run_file": "Run file",
        },
        "runner": {
            "heading": "Example Runner Output",
            "placeholder": 'Select a roadmap item and click "Run example".',
            "disabled": "Static hosting mode detected. Run examples locally from the repository for live execution.",
            "running": "Running",
            "request_failed": "Runner request failed",
        },
        "footer": {"generated_at": "Track data generated at"},
        "common": {"general": "General", "none": "(none)"},
    }

    foundation_ui_vi = {
        "hero": {
            "eyebrow": "Python Labs",
            "back_to_tracks": "Quay lại trang chọn lộ trình",
            "example_root": "Thư mục ví dụ",
            "static_note": "Chế độ static: GitHub Pages có thể duyệt lộ trình và ví dụ mà không cần API chạy Python.",
            "local_runner_enabled": "Có thể chạy ví dụ trực tiếp khi mở site bằng localhost.",
        },
        "sections": {
            "cheat_sheets": "Thư viện Cheat Sheet",
            "roadmap": "Lộ trình học",
            "mini_projects": "Mini Project",
            "database_practicals": "Thực hành Database",
            "extra_examples": "Thư viện Ví dụ Mở rộng",
            "open_source_stacks": "Stack Tích hợp Mã nguồn mở",
            "recommended_services": "Service Nên Tham Khảo",
        },
        "stats": {
            "cheat_items": "Mục Cheat Sheet",
            "roadmap_stages": "Chặng học",
            "completed": "Hoàn thành",
            "track": "Lộ trình",
        },
        "fields": {
            "application": "Ứng dụng",
            "goals": "Mục tiêu",
            "build": "Nên làm",
            "tools": "Công cụ",
            "example_code": "Mã ví dụ",
            "path": "Đường dẫn",
            "focus": "Trọng tâm",
            "entrypoint": "Điểm vào",
            "topics": "Chủ đề",
            "use_case": "Tình huống dùng",
            "java": "Java",
            "python": "Python",
            "when": "Dùng khi",
            "scope": "Phạm vi",
        },
        "roadmap": {
            "mark_completed": "Đánh dấu hoàn thành",
            "run_example": "Chạy ví dụ",
            "run_file": "Chạy file",
        },
        "runner": {
            "heading": "Kết quả chạy ví dụ",
            "placeholder": 'Chọn một mục trong lộ trình rồi bấm "Chạy ví dụ".',
            "disabled": "Đang ở chế độ static. Hãy chạy ví dụ cục bộ từ repository nếu cần thực thi trực tiếp.",
            "running": "Đang chạy",
            "request_failed": "Gọi runner thất bại",
        },
        "footer": {"generated_at": "Dữ liệu lộ trình được tạo lúc"},
        "common": {"general": "Tổng quát", "none": "(không có)"},
    }

    cheat_sheets_vi = [
        {
            "category": "Cú pháp",
            "title": "Biến và cách đặt tên",
            "summary": "Dùng `snake_case` và đặt tên mang ý nghĩa rõ ràng.",
            "snippet": "user_name = 'ThanhSon99'\\nmax_retries = 3\\nis_ready = False",
            "application": "Giúp script dễ đọc và cấu hình dễ bảo trì.",
            "tags": ["variables", "style"],
        },
        {
            "category": "Cú pháp",
            "title": "Kiểu dữ liệu cốt lõi",
            "summary": "Nắm rõ điểm mạnh yếu của `list`, `tuple`, `dict`, `set`.",
            "snippet": "skills = ['python', 'sql']\\nprofile = {'name': 'A', 'exp': 2}\\nunique_ids = {1, 2, 3}",
            "application": "Mô hình hóa payload API đầu vào.",
            "tags": ["types", "collections"],
        },
        {
            "category": "Cú pháp",
            "title": "Rẽ nhánh điều kiện",
            "summary": "Chặn sớm các trạng thái không hợp lệ.",
            "snippet": "if not token:\\n    raise ValueError('missing token')\\nelif token == 'dev':\\n    mode = 'sandbox'",
            "application": "Kiểm tra dữ liệu trước khi gửi request.",
            "tags": ["if", "validation"],
        },
        {
            "category": "Cú pháp",
            "title": "Vòng lặp",
            "summary": "Ưu tiên `enumerate` khi cần cả chỉ số lẫn phần tử.",
            "snippet": "for idx, item in enumerate(items, start=1):\\n    print(idx, item)",
            "application": "Xử lý batch và in log tiến độ.",
            "tags": ["for", "iteration"],
        },
        {
            "category": "Hàm",
            "title": "Thiết kế hàm",
            "summary": "Mỗi hàm chỉ nên có một trách nhiệm và trả về rõ ràng.",
            "snippet": "def build_url(host, path):\\n    return f'{host.rstrip('/')}/{path.lstrip('/')}'",
            "application": "Tạo helper tái sử dụng trong nhiều module.",
            "tags": ["functions", "clean-code"],
        },
        {
            "category": "Hàm",
            "title": "Tham số mặc định",
            "summary": "Tránh dùng giá trị mặc định có thể bị mutate.",
            "snippet": "def add_tag(tag, tags=None):\\n    tags = [] if tags is None else tags\\n    tags.append(tag)\\n    return tags",
            "application": "Ngăn bug do chia sẻ state ngoài ý muốn.",
            "tags": ["functions", "pitfalls"],
        },
        {
            "category": "Hàm",
            "title": "Lambda và sorted",
            "summary": "Giữ lambda ngắn gọn và dễ hiểu.",
            "snippet": "users = sorted(users, key=lambda x: x['score'], reverse=True)",
            "application": "Xếp hạng và biến đổi dữ liệu nhanh.",
            "tags": ["lambda", "sorting"],
        },
        {
            "category": "Tài liệu",
            "title": "Quy ước Docstring",
            "summary": "Mô tả tham số, giá trị trả về và lỗi có thể phát sinh.",
            "snippet": "def fetch(url):\\n    \"\"\"Fetch JSON data.\\n\\n    Args:\\n        url: endpoint URL\\n    Returns:\\n        dict payload\\n    \"\"\"",
            "application": "Onboard nhanh hơn và IDE gợi ý tốt hơn.",
            "tags": ["docstring", "documentation"],
        },
        {
            "category": "Tài liệu",
            "title": "Comment hữu ích",
            "summary": "Giải thích vì sao, không chỉ giải thích code đang làm gì.",
            "snippet": "# Keep 2 retries only to avoid duplicate external charges",
            "application": "Lưu lại bối cảnh quyết định nghiệp vụ.",
            "tags": ["comments", "code-review"],
        },
        {
            "category": "Import",
            "title": "Thứ tự import",
            "summary": "Sắp theo `stdlib`, thư viện ngoài, rồi module nội bộ.",
            "snippet": "import json\\nfrom pathlib import Path\\n\\nimport requests\\n\\nfrom .client import ApiClient",
            "application": "Giữ dự án gọn và nhất quán.",
            "tags": ["imports", "structure"],
        },
        {
            "category": "Xử lý lỗi",
            "title": "try/except/finally",
            "summary": "Chỉ bắt đúng loại exception cần xử lý.",
            "snippet": "try:\\n    payload = response.json()\\nexcept ValueError as exc:\\n    logger.error('invalid json: %s', exc)\\nfinally:\\n    response.close()",
            "application": "Xử lý API và file an toàn hơn.",
            "tags": ["exceptions", "reliability"],
        },
        {
            "category": "Xử lý lỗi",
            "title": "Custom Exception",
            "summary": "Biểu diễn lỗi ở mức domain bằng class riêng.",
            "snippet": "class PaymentDeclinedError(Exception):\\n    pass",
            "application": "Làm rõ contract giữa các tầng service.",
            "tags": ["exceptions", "domain"],
        },
        {
            "category": "Dữ liệu",
            "title": "List Comprehension",
            "summary": "Viết gọn thao tác map và filter.",
            "snippet": "valid_ids = [u['id'] for u in users if u.get('active')]",
            "application": "Biến đổi danh sách API nhanh chóng.",
            "tags": ["list", "comprehension"],
        },
        {
            "category": "Dữ liệu",
            "title": "dict.get và giá trị mặc định",
            "summary": "Tránh `KeyError` với payload không đầy đủ.",
            "snippet": "country = profile.get('address', {}).get('country', 'unknown')",
            "application": "Parse JSON bền hơn trước dữ liệu thiếu.",
            "tags": ["dict", "json"],
        },
        {
            "category": "Dữ liệu",
            "title": "Dataclass",
            "summary": "Model dữ liệu nhẹ, có kiểu rõ ràng.",
            "snippet": "from dataclasses import dataclass\\n\\n@dataclass\\nclass User:\\n    id: int\\n    email: str",
            "application": "Dùng làm DTO nội bộ cho tầng service.",
            "tags": ["dataclass", "typing"],
        },
        {
            "category": "File",
            "title": "Pathlib",
            "summary": "Ưu tiên `Path` thay vì nối chuỗi thủ công.",
            "snippet": "from pathlib import Path\\nreport = Path('data') / 'report.json'\\nreport.parent.mkdir(exist_ok=True)",
            "application": "Xử lý đường dẫn đa nền tảng.",
            "tags": ["pathlib", "filesystem"],
        },
        {
            "category": "File",
            "title": "Đọc ghi JSON",
            "summary": "Luôn khai báo encoding và indent khi cần debug.",
            "snippet": "with open('out.json', 'w', encoding='utf-8') as f:\\n    json.dump(payload, f, ensure_ascii=False, indent=2)",
            "application": "Hữu ích cho log kiểm tra và snapshot debug.",
            "tags": ["json", "io"],
        },
        {
            "category": "Database",
            "title": "Kết nối SQLite",
            "summary": "Database cục bộ đơn giản cho script và prototype.",
            "snippet": "import sqlite3\\nconn = sqlite3.connect('app.db')\\ncur = conn.cursor()\\ncur.execute('SELECT 1')\\nconn.close()",
            "application": "Lưu trữ nhanh mà không cần service ngoài.",
            "tags": ["sqlite", "database"],
        },
        {
            "category": "Database",
            "title": "PostgreSQL với SQLAlchemy",
            "summary": "Dùng `engine` và `session factory` để truy cập dữ liệu sạch hơn.",
            "snippet": "from sqlalchemy import create_engine\\nfrom sqlalchemy.orm import sessionmaker\\nengine = create_engine('postgresql+psycopg://user:pass@localhost:5432/app')\\nSession = sessionmaker(bind=engine)\\nsession = Session()",
            "application": "Tích hợp relational database theo hướng production.",
            "tags": ["postgresql", "sqlalchemy"],
        },
        {
            "category": "Database",
            "title": "Connection URL từ environment",
            "summary": "Không hardcode thông tin đăng nhập trong source code.",
            "snippet": "db_url = os.getenv('DATABASE_URL')\\nif not db_url:\\n    raise RuntimeError('DATABASE_URL is required')",
            "application": "Cấu hình an toàn và linh hoạt theo môi trường.",
            "tags": ["database", "env", "security"],
        },
        {
            "category": "HTTP",
            "title": "Requests có timeout",
            "summary": "Không gọi API mà thiếu timeout.",
            "snippet": "response = requests.get(url, timeout=15)\\nresponse.raise_for_status()",
            "application": "Tránh treo worker hoặc script lâu không cần thiết.",
            "tags": ["requests", "api"],
        },
        {
            "category": "HTTP",
            "title": "Mẫu retry",
            "summary": "Chỉ retry các thao tác idempotent.",
            "snippet": "for _ in range(3):\\n    try:\\n        return client.get()\\n    except TimeoutError:\\n        time.sleep(1)",
            "application": "Giảm lỗi khi làm việc với provider không ổn định.",
            "tags": ["retry", "resilience"],
        },
        {
            "category": "CLI",
            "title": "argparse",
            "summary": "Tạo script có tham số rõ ràng, dễ tái sử dụng.",
            "snippet": "parser.add_argument('--limit', type=int, default=50)\\nargs = parser.parse_args()",
            "application": "Hữu ích cho automation nội bộ.",
            "tags": ["cli", "argparse"],
        },
        {
            "category": "Môi trường",
            "title": "Biến môi trường",
            "summary": "Nạp secret từ env thay vì nhét vào code.",
            "snippet": "api_key = os.getenv('OPENAI_API_KEY')\\nif not api_key:\\n    raise RuntimeError('missing OPENAI_API_KEY')",
            "application": "Quản lý cấu hình an toàn hơn.",
            "tags": ["env", "security"],
        },
        {
            "category": "Logging",
            "title": "Structured Logging",
            "summary": "Log nên mang thêm context để dễ truy vết.",
            "snippet": "logger.info('sync completed', extra={'service': 'crypto', 'count': 42})",
            "application": "Hỗ trợ debug sự cố hiệu quả hơn.",
            "tags": ["logging", "observability"],
        },
        {
            "category": "Testing",
            "title": "pytest cơ bản",
            "summary": "Theo mẫu Arrange, Act, Assert.",
            "snippet": "def test_add():\\n    assert add(2, 3) == 5",
            "application": "Ngăn regression ở các helper quan trọng.",
            "tags": ["pytest", "qa"],
        },
        {
            "category": "Clean Code",
            "title": "Tách hàm nhỏ",
            "summary": "Tách logic dài thành các bước đặt tên rõ ràng.",
            "snippet": "def handle_order(order):\\n    validate_order(order)\\n    persist_order(order)\\n    publish_event(order)",
            "application": "Đọc code nhanh hơn và test từng phần dễ hơn.",
            "tags": ["refactor", "maintainability"],
        },
        {
            "category": "Packaging",
            "title": "requirements.txt tối thiểu",
            "summary": "Chỉ giữ dependency thực sự cần thiết.",
            "snippet": "requests==2.32.3\\npython-dotenv==1.0.1",
            "application": "Giảm độ phức tạp khi build và deploy.",
            "tags": ["deps", "packaging"],
        },
    ]

    roadmap_vi = [
        {
            "stage": "Chặng 1: Python Cốt lõi",
            "goals": [
                "biến, kiểu dữ liệu, toán tử",
                "if/else, vòng lặp, hàm",
                "comment và docstring",
                "import và khái niệm module cơ bản",
            ],
            "build": ["máy tính CLI", "trình đọc json", "công cụ đọc file"],
            "tools": ["python", "venv", "pip", "argparse"],
            "example_path": "learning-path/foundation/stage-01-python-core",
            "example_file": "learning-path/foundation/stage-01-python-core/main.py",
        },
        {
            "stage": "Chặng 2: Dữ liệu và File",
            "goals": [
                "mẫu dùng dict/list/set",
                "xử lý json và csv",
                "pathlib và an toàn filesystem",
                "tối ưu cơ bản bằng comprehension",
            ],
            "build": ["trình tạo báo cáo hằng ngày", "script làm sạch dữ liệu", "script đổi tên hàng loạt"],
            "tools": ["json", "csv", "pathlib", "collections"],
            "example_path": "learning-path/foundation/stage-02-data-and-files",
            "example_file": "learning-path/foundation/stage-02-data-and-files/transform_data.py",
        },
        {
            "stage": "Chặng 3: Tích hợp API",
            "goals": [
                "requests và timeout",
                "xử lý lỗi và retry",
                "cấu hình bằng biến môi trường",
                "chiến lược logging đơn giản",
            ],
            "build": ["weather cli", "trình theo dõi tỷ giá", "bộ gom tin RSS"],
            "tools": ["requests", "python-dotenv", "logging"],
            "example_path": "learning-path/foundation/stage-03-api-integrations",
            "example_file": "learning-path/foundation/stage-03-api-integrations/api_client.py",
        },
        {
            "stage": "Chặng 4: Cấu trúc Dự án",
            "goals": [
                "tách config/core/adapters",
                "loại bỏ utility trùng lặp",
                "tạo module tái sử dụng",
                "quản lý requirements theo từng service",
            ],
            "build": ["template service mini", "gói shared utils"],
            "tools": ["pip", "pytest", "ruff", "black"],
            "example_path": "learning-path/foundation/stage-04-project-structure",
            "example_file": "learning-path/foundation/stage-04-project-structure/app/main.py",
        },
        {
            "stage": "Chặng 5: Automation Trung cấp",
            "goals": [
                "lên lịch cho script",
                "tiêu thụ API bên thứ ba",
                "tạo báo cáo markdown/html",
                "dùng test gọn nhẹ",
            ],
            "build": ["market tracker", "bot tóm tắt tự động", "bộ lên lịch cảnh báo"],
            "tools": ["apscheduler", "jinja2", "pytest"],
            "example_path": "learning-path/foundation/stage-05-intermediate-automation",
            "example_file": "learning-path/foundation/stage-05-intermediate-automation/scheduler_demo.py",
        },
        {
            "stage": "Chặng 6: Nền tảng API Service",
            "goals": [
                "xây CRUD API",
                "dùng validation với pydantic",
                "thêm endpoint health và readiness",
                "giới thiệu middleware đơn giản",
            ],
            "build": ["task api", "prototype auth", "bảng trạng thái service"],
            "tools": ["fastapi", "uvicorn", "pydantic"],
            "example_path": "learning-path/foundation/stage-06-api-service-basics",
            "example_file": "learning-path/foundation/stage-06-api-service-basics/mini_api.py",
        },
        {
            "stage": "Chặng 7: Storage",
            "goals": [
                "nền tảng SQL",
                "sử dụng ORM",
                "migration",
                "index và tối ưu query cơ bản",
                "connection pool và an toàn transaction",
            ],
            "build": ["inventory service", "blog backend"],
            "tools": ["postgresql", "sqlalchemy", "alembic"],
            "example_path": "learning-path/foundation/stage-07-storage",
            "example_file": "learning-path/foundation/stage-07-storage/sqlite_example.py",
        },
        {
            "stage": "Chặng 8: Async và Concurrency",
            "goals": [
                "so sánh threadpool và async",
                "tối ưu tác vụ I/O bound",
                "nền tảng background worker",
                "graceful shutdown",
            ],
            "build": ["bulk fetcher", "parallel scraper", "async notifier"],
            "tools": ["asyncio", "httpx", "concurrent.futures"],
            "example_path": "learning-path/foundation/stage-08-async-and-concurrency",
            "example_file": "learning-path/foundation/stage-08-async-and-concurrency/async_demo.py",
        },
        {
            "stage": "Chặng 9: Testing và Chất lượng",
            "goals": [
                "unit test và integration test",
                "test double và mock",
                "độ phủ code",
                "pre-commit automation",
            ],
            "build": ["bộ test cho một service"],
            "tools": ["pytest", "coverage", "pre-commit"],
            "example_path": "learning-path/foundation/stage-09-testing-and-quality",
            "example_file": "learning-path/foundation/stage-09-testing-and-quality/math_utils.py",
        },
        {
            "stage": "Chặng 10: Delivery",
            "goals": [
                "docker hóa một service",
                "cấu hình theo môi trường",
                "pipeline CI cơ bản",
                "ghi release notes và changelog",
            ],
            "build": ["api docker hóa + ci"],
            "tools": ["docker", "github actions", "makefile"],
            "example_path": "learning-path/foundation/stage-10-delivery",
            "example_file": "",
        },
    ]

    open_source_stacks_vi = [
        {
            "name": "FastAPI Starter",
            "use_case": "REST API có kiểu rõ ràng và tài liệu tự sinh.",
            "packages": ["fastapi", "uvicorn", "pydantic"],
        },
        {
            "name": "Data Layer Starter",
            "use_case": "Làm việc với database quan hệ và migration.",
            "packages": ["sqlalchemy", "alembic", "psycopg"],
        },
        {
            "name": "Caching Starter",
            "use_case": "Đọc nhanh và lưu trạng thái tạm thời độ trễ thấp.",
            "packages": ["redis", "hiredis"],
        },
        {
            "name": "Background Jobs Starter",
            "use_case": "Tác vụ async và worker chạy định kỳ.",
            "packages": ["celery", "redis", "apscheduler"],
        },
        {
            "name": "Quality Starter",
            "use_case": "Lint, format và test cho chất lượng code.",
            "packages": ["pytest", "ruff", "black", "mypy"],
        },
    ]

    mini_projects_vi = [
        {
            "name": "Cột mốc Foundation 1: Bộ công cụ CLI xử lý dữ liệu",
            "path": "learning-path/projects/foundation-cli-data-toolkit",
            "focus": "Cú pháp cốt lõi + biến đổi dữ liệu + xuất file",
            "stack": ["python", "argparse", "json", "pathlib"],
        },
        {
            "name": "Cột mốc Foundation 2: Service API + lưu trữ",
            "path": "learning-path/projects/foundation-api-storage-service",
            "focus": "HTTP endpoint + persistence + test",
            "stack": ["http.server", "sqlite3", "pytest"],
        },
    ]

    extra_examples_vi = [
        {"title": "Decorator", "path": "learning-path/foundation/extras/decorators/example.py"},
        {"title": "Context Manager", "path": "learning-path/foundation/extras/context-managers/example.py"},
        {"title": "itertools + regex", "path": "learning-path/foundation/extras/itertools-regex/example.py"},
        {"title": "argparse subcommands", "path": "learning-path/foundation/extras/argparse-subcommands/example.py"},
        {"title": "cấu hình logging", "path": "learning-path/foundation/extras/logging-config/example.py"},
        {"title": "CSV nâng cao", "path": "learning-path/foundation/extras/csv-advanced/example.py"},
        {"title": "pathlib nâng cao", "path": "learning-path/foundation/extras/pathlib-advanced/example.py"},
        {"title": "typing generics", "path": "learning-path/foundation/extras/typing-generics/example.py"},
        {"title": "kiểm tra dataclass", "path": "learning-path/foundation/extras/dataclass-validation/example.py"},
        {"title": "mẫu lỗi thường gặp", "path": "learning-path/foundation/extras/error-patterns/example.py"},
    ]

    database_practicals_vi = [
        {"title": "PostgreSQL local (Docker)", "path": "learning-path/database/postgres-local/docker-compose.yml"},
        {"title": "kiểm tra kết nối PostgreSQL", "path": "learning-path/database/postgres-local/check_connection.py"},
        {"title": "demo Alembic", "path": "learning-path/database/alembic-demo/README.md"},
        {"title": "index và query plan", "path": "learning-path/database/indexing-query-plan/example.sql"},
        {"title": "ghi chú isolation", "path": "learning-path/database/isolation-demo/example.py"},
        {"title": "demo connection pool", "path": "learning-path/database/pool-demo/example.py"},
    ]

    foundation_locales = {
        "en": {
            "title": "Python Foundation Track",
            "subtitle": "Large practical cheatsheet + stepwise roadmap from beginner to strong intermediate.",
            "ui": foundation_ui_en,
            "cheat_sheets": FOUNDATION_CHEATSHEET,
            "roadmap": roadmap,
            "open_source_stacks": open_source_stacks,
            "mini_projects": mini_projects,
            "extra_examples": extra_examples,
            "database_practicals": database_practicals,
            "recommended_services": beginner_services,
        },
        "vi": {
            "title": "Lộ trình Python Foundation",
            "subtitle": "Cheat sheet thực chiến kèm lộ trình từng bước từ mới bắt đầu lên trung cấp vững.",
            "ui": foundation_ui_vi,
            "cheat_sheets": cheat_sheets_vi,
            "roadmap": roadmap_vi,
            "open_source_stacks": open_source_stacks_vi,
            "mini_projects": mini_projects_vi,
            "extra_examples": extra_examples_vi,
            "database_practicals": database_practicals_vi,
            "recommended_services": beginner_services,
        },
    }

    return {
        "generated_at": generated_at,
        "site": "foundation",
        "default_locale": "en",
        "supported_locales": ["en", "vi"],
        "title": "Python Foundation Track",
        "subtitle": "Large practical cheatsheet + stepwise roadmap from beginner to strong intermediate.",
        "example_root": "learning-path/foundation",
        "cheat_sheets": FOUNDATION_CHEATSHEET,
        "roadmap": roadmap,
        "open_source_stacks": open_source_stacks,
        "mini_projects": mini_projects,
        "extra_examples": extra_examples,
        "database_practicals": database_practicals,
        "recommended_services": beginner_services,
        "locales": foundation_locales,
    }


def _build_advanced_track(services: list[dict], generated_at: str) -> dict:
    advanced_services = [s for s in services if s["level"] == "advanced"]
    java_python_map = [
        {
            "domain": "Message Queue",
            "java_stack": "RabbitMQ + Spring AMQP",
            "python_stack": "RabbitMQ + aio-pika / pika + Celery",
            "when": "Asynchronous job processing, delayed tasks",
        },
        {
            "domain": "Event Streaming",
            "java_stack": "Kafka + Spring Kafka",
            "python_stack": "Kafka + aiokafka / confluent-kafka",
            "when": "Event-driven architecture, audit logs, analytics",
        },
        {
            "domain": "REST API",
            "java_stack": "Spring Boot",
            "python_stack": "FastAPI / Flask",
            "when": "Public/internal HTTP services",
        },
        {
            "domain": "ORM",
            "java_stack": "JPA / Hibernate",
            "python_stack": "SQLAlchemy",
            "when": "Relational persistence with repository patterns",
        },
        {
            "domain": "Batch Jobs",
            "java_stack": "Spring Batch",
            "python_stack": "Celery beat / Airflow",
            "when": "Scheduled ETL or periodic processing",
        },
        {
            "domain": "Service Discovery",
            "java_stack": "Eureka",
            "python_stack": "Consul / Kubernetes DNS",
            "when": "Dynamic service-to-service resolution",
        },
        {
            "domain": "Config Server",
            "java_stack": "Spring Cloud Config",
            "python_stack": "env + Vault + config service",
            "when": "Centralized config management",
        },
        {
            "domain": "Gateway",
            "java_stack": "Spring Cloud Gateway",
            "python_stack": "Kong / Traefik / Nginx + FastAPI",
            "when": "Auth, routing, throttling, request policy",
        },
        {
            "domain": "Observability",
            "java_stack": "Micrometer + Zipkin",
            "python_stack": "Prometheus + OpenTelemetry + Grafana",
            "when": "Metrics and tracing at scale",
        },
    ]

    roadmap = [
        {
            "stage": "Phase A: Service Contracts",
            "goals": [
                "define API schemas (OpenAPI/protobuf)",
                "enforce versioning strategy",
                "set backward compatibility rules",
            ],
            "build": ["contract-first user service", "api lint pipeline"],
            "tools": ["FastAPI", "Pydantic", "protobuf", "spectral"],
            "example_path": "learning-path/advanced/phase-a-service-contracts",
            "example_file": "learning-path/advanced/phase-a-service-contracts/pydantic_models.py",
        },
        {
            "stage": "Phase B: Event-Driven Core",
            "goals": [
                "choose queue vs stream",
                "implement producer/consumer",
                "add dead letter and retry policies",
            ],
            "build": ["order event pipeline", "notification worker"],
            "tools": ["RabbitMQ", "Kafka", "Redis Streams"],
            "example_path": "learning-path/advanced/phase-b-event-driven-core",
            "example_file": "learning-path/advanced/phase-b-event-driven-core/rabbitmq_worker_example.py",
        },
        {
            "stage": "Phase C: Consistency Patterns",
            "goals": [
                "outbox/inbox",
                "idempotency keys",
                "saga orchestration and compensation",
            ],
            "build": ["payment + order saga"],
            "tools": ["PostgreSQL", "Celery", "Kafka"],
            "example_path": "learning-path/advanced/phase-c-consistency-patterns",
            "example_file": "learning-path/advanced/phase-c-consistency-patterns/outbox_pattern_example.py",
        },
        {
            "stage": "Phase D: Data Platform",
            "goals": [
                "transactional database design",
                "read model/cache strategy",
                "migration governance",
            ],
            "build": ["billing ledger", "query side read API"],
            "tools": ["SQLAlchemy", "Alembic", "Redis"],
            "example_path": "learning-path/advanced/phase-d-data-platform",
            "example_file": "learning-path/advanced/phase-d-data-platform/repository_pattern.py",
        },
        {
            "stage": "Phase E: Reliability Engineering",
            "goals": [
                "timeout budgets and retries",
                "circuit breaker and fallback",
                "bulkhead isolation",
            ],
            "build": ["resilient API adapter layer"],
            "tools": ["httpx", "tenacity", "rate limiting"],
            "example_path": "learning-path/advanced/phase-e-reliability-engineering",
            "example_file": "learning-path/advanced/phase-e-reliability-engineering/resilient_http_client.py",
        },
        {
            "stage": "Phase F: Security",
            "goals": [
                "OIDC/JWT architecture",
                "key rotation",
                "secrets and policy management",
            ],
            "build": ["auth gateway", "token introspection service"],
            "tools": ["Auth0/Keycloak", "Vault", "OPA"],
            "example_path": "learning-path/advanced/phase-f-security",
            "example_file": "learning-path/advanced/phase-f-security/jwt_service_example.py",
        },
        {
            "stage": "Phase G: Observability",
            "goals": [
                "golden signals dashboards",
                "distributed tracing",
                "alert routing and runbooks",
            ],
            "build": ["full telemetry stack for 3 services"],
            "tools": ["Prometheus", "Grafana", "OpenTelemetry", "Loki"],
            "example_path": "learning-path/advanced/phase-g-observability",
            "example_file": "learning-path/advanced/phase-g-observability/structured_logging_example.py",
        },
        {
            "stage": "Phase H: Platform and Delivery",
            "goals": [
                "container hardening",
                "kubernetes deployment templates",
                "canary/blue-green release",
            ],
            "build": ["production deployment blueprint"],
            "tools": ["Docker", "Kubernetes", "Argo Rollouts"],
            "example_path": "learning-path/advanced/phase-h-platform-delivery",
            "example_file": "",
        },
        {
            "stage": "Phase I: Governance and Cost",
            "goals": [
                "service ownership model",
                "slo and error budgets",
                "cost/performance optimization",
            ],
            "build": ["team service catalog + operational playbook"],
            "tools": ["Backstage", "FinOps dashboards"],
            "example_path": "learning-path/advanced/phase-i-governance-and-cost",
            "example_file": "",
        },
    ]

    capstone = [
        {
            "name": "Realtime Market Intelligence Platform",
            "scope": "ingestion -> processing -> alerting -> dashboard",
            "stack": ["FastAPI", "Kafka", "Redis", "PostgreSQL", "Grafana"],
        },
        {
            "name": "E-commerce Event Microservices",
            "scope": "catalog, cart, payment, shipment, notification",
            "stack": ["FastAPI", "RabbitMQ", "Celery", "OpenTelemetry", "Kubernetes"],
        },
        {
            "name": "AI Workflow Orchestrator",
            "scope": "job queue, model adapters, usage metering, billing",
            "stack": ["FastAPI", "Dramatiq", "Redis", "PostgreSQL", "Prometheus"],
        },
    ]

    open_source_stacks = [
        {
            "name": "Event-Driven Core",
            "use_case": "Domain events and asynchronous service communication.",
            "packages": ["aiokafka", "pydantic", "tenacity"],
        },
        {
            "name": "Queue Worker Core",
            "use_case": "Reliable background processing with retries.",
            "packages": ["celery", "rabbitmq", "redis"],
        },
        {
            "name": "Service Platform Core",
            "use_case": "HTTP API + DB + migration + cache baseline.",
            "packages": ["fastapi", "sqlalchemy", "alembic", "redis", "httpx"],
        },
        {
            "name": "Observability Core",
            "use_case": "Metrics, tracing, and log correlation.",
            "packages": ["prometheus-client", "opentelemetry-sdk", "structlog"],
        },
        {
            "name": "Security Core",
            "use_case": "AuthN/AuthZ and secret management.",
            "packages": ["pyjwt", "passlib", "authlib", "hvac"],
        },
    ]

    mini_projects = [
        {
            "name": "Advanced Milestone 1: Event Pipeline Starter",
            "path": "learning-path/projects/advanced-event-pipeline-starter",
            "focus": "Producer-consumer flow + retry + outbox pattern",
            "stack": ["Kafka", "RabbitMQ", "SQLite", "Python workers"],
        },
        {
            "name": "Advanced Milestone 2: Observable Service Platform",
            "path": "learning-path/projects/advanced-observable-service-platform",
            "focus": "API + DB + metrics + structured logging + deploy templates",
            "stack": ["FastAPI", "PostgreSQL", "Prometheus", "OpenTelemetry", "Docker"],
        },
        {
            "name": "Advanced Milestone 3: Capstone E2E Platform",
            "path": "learning-path/projects/capstone-e2e-platform",
            "focus": "API + queue + DB + metrics + dashboard + deploy templates + tests",
            "stack": ["http.server", "sqlite3", "pytest", "docker-compose", "k8s manifest"],
        },
    ]

    architecture_diagrams = [
        {"title": "RabbitMQ Worker Flow", "file": "assets/diagrams/rabbitmq-flow.svg"},
        {"title": "Kafka Stream Processing Flow", "file": "assets/diagrams/kafka-flow.svg"},
        {"title": "Outbox Pattern Transaction Flow", "file": "assets/diagrams/outbox-pattern.svg"},
        {"title": "Saga Orchestration Flow", "file": "assets/diagrams/saga-flow.svg"},
    ]

    extra_examples = [
        {"title": "Retry backoff", "path": "learning-path/advanced/extras/retry-backoff/example.py"},
        {"title": "Circuit breaker", "path": "learning-path/advanced/extras/circuit-breaker/example.py"},
        {"title": "Idempotency middleware", "path": "learning-path/advanced/extras/idempotency-middleware/example.py"},
        {"title": "Saga compensation", "path": "learning-path/advanced/extras/saga-compensation/example.py"},
        {"title": "Outbox relay", "path": "learning-path/advanced/extras/outbox-relay/example.py"},
        {"title": "Contract testing", "path": "learning-path/advanced/extras/contract-testing/example.py"},
        {"title": "Pattern tests", "path": "learning-path/advanced/extras/tests/test_patterns.py"},
    ]

    advanced_ui_en = {
        "hero": {
            "eyebrow": "Python Labs",
            "back_to_tracks": "Back to track selection",
            "example_root": "Example root",
            "static_note": "Static hosting mode: GitHub Pages can browse the roadmap and examples without the Python runner API.",
            "local_runner_enabled": "Local runner is available on localhost.",
        },
        "sections": {
            "cheat_sheets": "Advanced Cheat Sheet Library",
            "roadmap": "Architecture Roadmap",
            "java_python_map": "Java to Python Stack Mapping",
            "architecture_diagrams": "Architecture Diagrams",
            "mini_projects": "Mini Projects",
            "extra_examples": "Extra Pattern Library",
            "open_source_stacks": "Open-Source Integration Stacks",
            "capstone_projects": "Capstone Applications",
            "recommended_services": "Recommended Services",
        },
        "stats": {
            "cheat_items": "Cheat Items",
            "roadmap_stages": "Roadmap Stages",
            "completed": "Completed",
            "track": "Track",
        },
        "fields": {
            "application": "Application",
            "goals": "Goals",
            "build": "Build",
            "tools": "Tools",
            "example_code": "Example code",
            "path": "Path",
            "focus": "Focus",
            "entrypoint": "Entrypoint",
            "topics": "Topics",
            "use_case": "Use case",
            "java": "Java",
            "python": "Python",
            "when": "Use when",
            "scope": "Scope",
        },
        "roadmap": {
            "mark_completed": "Mark completed",
            "run_example": "Run example",
            "run_file": "Run file",
        },
        "runner": {
            "heading": "Example Runner Output",
            "placeholder": 'Select a roadmap item and click "Run example".',
            "disabled": "Static hosting mode detected. Run examples locally from the repository for live execution.",
            "running": "Running",
            "request_failed": "Runner request failed",
        },
        "footer": {"generated_at": "Track data generated at"},
        "common": {"general": "General", "none": "(none)"},
    }

    advanced_ui_vi = {
        "hero": {
            "eyebrow": "Python Labs",
            "back_to_tracks": "Quay lại trang chọn lộ trình",
            "example_root": "Thư mục ví dụ",
            "static_note": "Chế độ static: GitHub Pages có thể duyệt lộ trình và ví dụ mà không cần API chạy Python.",
            "local_runner_enabled": "Có thể chạy ví dụ trực tiếp khi mở site bằng localhost.",
        },
        "sections": {
            "cheat_sheets": "Thư viện Cheat Sheet Nâng Cao",
            "roadmap": "Lộ trình Kiến Trúc",
            "java_python_map": "Bản đồ Stack Java sang Python",
            "architecture_diagrams": "Sơ đồ Kiến Trúc",
            "mini_projects": "Mini Project",
            "extra_examples": "Thư viện Pattern Mở rộng",
            "open_source_stacks": "Stack Tích hợp Mã nguồn mở",
            "capstone_projects": "Ứng dụng Capstone",
            "recommended_services": "Service Nên Tham Khảo",
        },
        "stats": {
            "cheat_items": "Mục Cheat Sheet",
            "roadmap_stages": "Chặng học",
            "completed": "Hoàn thành",
            "track": "Lộ trình",
        },
        "fields": {
            "application": "Ứng dụng",
            "goals": "Mục tiêu",
            "build": "Nên làm",
            "tools": "Công cụ",
            "example_code": "Mã ví dụ",
            "path": "Đường dẫn",
            "focus": "Trọng tâm",
            "entrypoint": "Điểm vào",
            "topics": "Chủ đề",
            "use_case": "Tình huống dùng",
            "java": "Java",
            "python": "Python",
            "when": "Dùng khi",
            "scope": "Phạm vi",
        },
        "roadmap": {
            "mark_completed": "Đánh dấu hoàn thành",
            "run_example": "Chạy ví dụ",
            "run_file": "Chạy file",
        },
        "runner": {
            "heading": "Kết quả chạy ví dụ",
            "placeholder": 'Chọn một mục trong lộ trình rồi bấm "Chạy ví dụ".',
            "disabled": "Đang ở chế độ static. Hãy chạy ví dụ cục bộ từ repository nếu cần thực thi trực tiếp.",
            "running": "Đang chạy",
            "request_failed": "Gọi runner thất bại",
        },
        "footer": {"generated_at": "Dữ liệu lộ trình được tạo lúc"},
        "common": {"general": "Tổng quát", "none": "(không có)"},
    }

    advanced_cheatsheet_vi = [
        {"category": "Kiến trúc", "title": "Service phân lớp", "summary": "Transport -> application -> domain -> infrastructure.", "snippet": "api -> use_case -> domain_model -> repository", "application": "Giữ business logic độc lập với framework.", "tags": ["architecture", "clean"]},
        {"category": "Kiến trúc", "title": "Hexagonal Ports/Adapters", "summary": "Định nghĩa port như interface; adapter dùng để tích hợp vendor.", "snippet": "class PriceFeedPort(Protocol):\\n    def latest(self, symbol: str) -> float: ...", "application": "Đổi nhà cung cấp API mà không phải viết lại core.", "tags": ["ports", "adapters"]},
        {"category": "Messaging", "title": "RabbitMQ", "summary": "Phân phối công việc theo mô hình queue.", "snippet": "aio-pika / pika + dead-letter queue + retry headers", "application": "Email, tạo ảnh, job bất đồng bộ.", "tags": ["rabbitmq", "queue"]},
        {"category": "Messaging", "title": "Kafka", "summary": "Event streaming và log bền vững.", "snippet": "aiokafka producer/consumer + partitioned topics", "application": "Luồng audit, analytics, CDC pipeline.", "tags": ["kafka", "stream"]},
        {"category": "Messaging", "title": "Redis Streams", "summary": "Stream nhẹ với consumer group.", "snippet": "XADD / XREADGROUP for event fan-out", "application": "Hệ thống event-driven quy mô nhỏ hơn.", "tags": ["redis", "stream"]},
        {"category": "Xử lý tác vụ", "title": "Celery", "summary": "Task queue phân tán có retry và scheduling.", "snippet": "@celery.task(bind=True, autoretry_for=(Exception,), retry_backoff=True)", "application": "Job async chạy lâu trong production.", "tags": ["celery", "workers"]},
        {"category": "Xử lý tác vụ", "title": "Dramatiq / RQ", "summary": "Giải pháp nền đơn giản hơn cho background worker.", "snippet": "@dramatiq.actor(max_retries=5)", "application": "Queue workload quy mô nhỏ và vừa.", "tags": ["dramatiq", "rq"]},
        {"category": "API", "title": "FastAPI", "summary": "REST API có type rõ ràng và sinh OpenAPI.", "snippet": "@app.get('/health')\\ndef health() -> dict[str, str]:\\n    return {'status': 'ok'}", "application": "Endpoint service và tài liệu theo hướng docs-first.", "tags": ["fastapi", "api"]},
        {"category": "API", "title": "gRPC", "summary": "Binary RPC cho giao tiếp service nội bộ.", "snippet": "protobuf contracts + generated Python stubs", "application": "Gọi nội bộ microservice độ trễ thấp.", "tags": ["grpc", "protobuf"]},
        {"category": "Dữ liệu", "title": "SQLAlchemy 2", "summary": "Mẫu unit-of-work và repository.", "snippet": "session.execute(select(User).where(User.id == uid)).scalar_one_or_none()", "application": "Tầng dữ liệu quan hệ đáng tin cậy.", "tags": ["sqlalchemy", "postgres"]},
        {"category": "Dữ liệu", "title": "Alembic Migrations", "summary": "Version hóa thay đổi schema an toàn.", "snippet": "alembic revision --autogenerate -m 'add event table'", "application": "Triển khai database ít bất ngờ hơn.", "tags": ["alembic", "migration"]},
        {"category": "Dữ liệu", "title": "Async DB Access", "summary": "Dùng async driver cho API có concurrency cao.", "snippet": "asyncpg / sqlalchemy.ext.asyncio", "application": "Phù hợp cho API nặng về I/O.", "tags": ["async", "database"]},
        {"category": "Caching", "title": "Redis Cache Aside", "summary": "Read-through với TTL và quy tắc invalidation.", "snippet": "value = redis.get(key) or load_from_db()", "application": "Giảm tải DB và giảm độ trễ phản hồi.", "tags": ["redis", "cache"]},
        {"category": "Quan sát hệ thống", "title": "Metrics", "summary": "Expose counter và histogram Prometheus.", "snippet": "REQUEST_LATENCY.labels(route='/verify').observe(seconds)", "application": "Theo dõi SLO và gắn cảnh báo.", "tags": ["prometheus", "metrics"]},
        {"category": "Quan sát hệ thống", "title": "Tracing", "summary": "Lan truyền trace-id qua nhiều service.", "snippet": "OpenTelemetry instrumentation + OTLP exporter", "application": "Debug spike độ trễ phân tán.", "tags": ["otel", "tracing"]},
        {"category": "Quan sát hệ thống", "title": "Structured Logs", "summary": "Log JSON có correlation id.", "snippet": "{'trace_id': tid, 'event': 'order_confirmed', 'service': 'billing'}", "application": "Phân tích log tập trung qua ELK/Loki.", "tags": ["logs", "json"]},
        {"category": "Bảo mật", "title": "JWT và xoay khóa", "summary": "Dùng thời hạn token ngắn và xoay khóa ký.", "snippet": "kid-based key set + refresh token revocation list", "application": "Auth trong gateway microservice.", "tags": ["jwt", "auth"]},
        {"category": "Bảo mật", "title": "Quản lý secrets", "summary": "Giữ secret ở ngoài image và repo.", "snippet": "Vault / AWS Secrets Manager / Doppler", "application": "Bảo vệ cấu hình production.", "tags": ["secrets", "ops"]},
        {"category": "Bảo mật", "title": "Rate Limit", "summary": "Bảo vệ endpoint khỏi lạm dụng.", "snippet": "token bucket by IP/API key", "application": "Gia cố public API.", "tags": ["rate-limit", "api"]},
        {"category": "Độ bền", "title": "Circuit Breaker", "summary": "Ngắt mạch khi downstream lỗi lặp lại.", "snippet": "closed -> open -> half-open states", "application": "Ngăn sự cố dây chuyền.", "tags": ["circuit-breaker", "reliability"]},
        {"category": "Độ bền", "title": "Idempotency Key", "summary": "Xử lý an toàn request retry bị trùng.", "snippet": "X-Idempotency-Key persisted with response hash", "application": "Payment API và order API.", "tags": ["idempotency", "api"]},
        {"category": "Độ bền", "title": "Outbox Pattern", "summary": "Phát event đáng tin cậy cùng transaction DB.", "snippet": "write business row + outbox row in same tx", "application": "Tránh mất event sau commit.", "tags": ["outbox", "event-driven"]},
        {"category": "Triển khai", "title": "Docker Multi-stage", "summary": "Image production gọn với base image đã pin phiên bản.", "snippet": "builder stage installs deps, runtime stage runs app", "application": "CI nhanh hơn và giảm attack surface.", "tags": ["docker", "deployment"]},
        {"category": "Triển khai", "title": "Kubernetes Basics", "summary": "Dùng Deployment, Service, ConfigMap, Secret, HPA.", "snippet": "readinessProbe + livenessProbe + resource limits", "application": "Điều phối service có thể mở rộng.", "tags": ["k8s", "cloud"]},
        {"category": "Triển khai", "title": "Blue/Green + Canary", "summary": "Triển khai dần để giảm blast radius.", "snippet": "10% traffic canary then full promotion", "application": "Release an toàn hơn cho API quan trọng.", "tags": ["release", "sre"]},
        {"category": "Testing", "title": "Contract Testing", "summary": "Xác minh tương thích API giữa các service.", "snippet": "consumer-driven contracts (Pact) in CI", "application": "Ổn định tích hợp microservice.", "tags": ["contract", "testing"]},
        {"category": "Testing", "title": "Load Testing", "summary": "Đo throughput và ngưỡng latency.", "snippet": "k6 scenarios with p95 and p99 thresholds", "application": "Lập kế hoạch capacity trước khi launch.", "tags": ["performance", "load-test"]},
        {"category": "CI/CD", "title": "Pipeline Gates", "summary": "lint -> unit -> integration -> security scan -> deploy", "snippet": "fail fast on quality gates", "application": "Quy trình release tự động đáng tin cậy.", "tags": ["cicd", "devops"]},
        {"category": "Domain", "title": "Event Modeling", "summary": "Đặt tên event bằng ngôn ngữ nghiệp vụ.", "snippet": "user_registered, payment_authorized, order_shipped", "application": "Thiết kế event-driven rõ ràng hơn.", "tags": ["ddd", "events"]},
        {"category": "Domain", "title": "Saga Pattern", "summary": "Điều phối transaction phân tán.", "snippet": "reserve -> charge -> confirm / compensate", "application": "Điều phối order và payment.", "tags": ["saga", "distributed"]},
    ]

    java_python_map_vi = [
        {"domain": "Message Queue", "java_stack": "RabbitMQ + Spring AMQP", "python_stack": "RabbitMQ + aio-pika / pika + Celery", "when": "Xử lý job bất đồng bộ, delayed task"},
        {"domain": "Event Streaming", "java_stack": "Kafka + Spring Kafka", "python_stack": "Kafka + aiokafka / confluent-kafka", "when": "Kiến trúc event-driven, audit log, analytics"},
        {"domain": "REST API", "java_stack": "Spring Boot", "python_stack": "FastAPI / Flask", "when": "HTTP service public hoặc nội bộ"},
        {"domain": "ORM", "java_stack": "JPA / Hibernate", "python_stack": "SQLAlchemy", "when": "Lưu trữ quan hệ theo repository pattern"},
        {"domain": "Batch Jobs", "java_stack": "Spring Batch", "python_stack": "Celery beat / Airflow", "when": "ETL theo lịch hoặc xử lý định kỳ"},
        {"domain": "Service Discovery", "java_stack": "Eureka", "python_stack": "Consul / Kubernetes DNS", "when": "Phân giải service động giữa các service"},
        {"domain": "Config Server", "java_stack": "Spring Cloud Config", "python_stack": "env + Vault + config service", "when": "Quản lý cấu hình tập trung"},
        {"domain": "Gateway", "java_stack": "Spring Cloud Gateway", "python_stack": "Kong / Traefik / Nginx + FastAPI", "when": "Auth, routing, throttling, request policy"},
        {"domain": "Observability", "java_stack": "Micrometer + Zipkin", "python_stack": "Prometheus + OpenTelemetry + Grafana", "when": "Metrics và tracing ở quy mô lớn"},
    ]

    roadmap_vi = [
        {"stage": "Pha A: Hợp đồng Service", "goals": ["định nghĩa schema API (OpenAPI/protobuf)", "áp dụng chiến lược versioning", "đặt quy tắc tương thích ngược"], "build": ["user service theo contract-first", "pipeline lint API"], "tools": ["FastAPI", "Pydantic", "protobuf", "spectral"], "example_path": "learning-path/advanced/phase-a-service-contracts", "example_file": "learning-path/advanced/phase-a-service-contracts/pydantic_models.py"},
        {"stage": "Pha B: Event-Driven Core", "goals": ["chọn queue hay stream", "triển khai producer/consumer", "thêm dead letter và retry policy"], "build": ["pipeline event đơn hàng", "notification worker"], "tools": ["RabbitMQ", "Kafka", "Redis Streams"], "example_path": "learning-path/advanced/phase-b-event-driven-core", "example_file": "learning-path/advanced/phase-b-event-driven-core/rabbitmq_worker_example.py"},
        {"stage": "Pha C: Consistency Patterns", "goals": ["outbox/inbox", "idempotency key", "saga orchestration và compensation"], "build": ["saga thanh toán + đơn hàng"], "tools": ["PostgreSQL", "Celery", "Kafka"], "example_path": "learning-path/advanced/phase-c-consistency-patterns", "example_file": "learning-path/advanced/phase-c-consistency-patterns/outbox_pattern_example.py"},
        {"stage": "Pha D: Nền tảng Dữ liệu", "goals": ["thiết kế database giao dịch", "chiến lược read model/cache", "governance cho migration"], "build": ["billing ledger", "read API cho query side"], "tools": ["SQLAlchemy", "Alembic", "Redis"], "example_path": "learning-path/advanced/phase-d-data-platform", "example_file": "learning-path/advanced/phase-d-data-platform/repository_pattern.py"},
        {"stage": "Pha E: Reliability Engineering", "goals": ["timeout budget và retry", "circuit breaker và fallback", "bulkhead isolation"], "build": ["lớp adapter API có khả năng chịu lỗi"], "tools": ["httpx", "tenacity", "rate limiting"], "example_path": "learning-path/advanced/phase-e-reliability-engineering", "example_file": "learning-path/advanced/phase-e-reliability-engineering/resilient_http_client.py"},
        {"stage": "Pha F: Bảo mật", "goals": ["kiến trúc OIDC/JWT", "xoay khóa", "quản lý secret và policy"], "build": ["auth gateway", "service introspection token"], "tools": ["Auth0/Keycloak", "Vault", "OPA"], "example_path": "learning-path/advanced/phase-f-security", "example_file": "learning-path/advanced/phase-f-security/jwt_service_example.py"},
        {"stage": "Pha G: Quan sát hệ thống", "goals": ["dashboard golden signals", "distributed tracing", "alert routing và runbook"], "build": ["full telemetry stack cho 3 service"], "tools": ["Prometheus", "Grafana", "OpenTelemetry", "Loki"], "example_path": "learning-path/advanced/phase-g-observability", "example_file": "learning-path/advanced/phase-g-observability/structured_logging_example.py"},
        {"stage": "Pha H: Platform và Delivery", "goals": ["hardening container", "template deploy Kubernetes", "release canary/blue-green"], "build": ["bản thiết kế triển khai production"], "tools": ["Docker", "Kubernetes", "Argo Rollouts"], "example_path": "learning-path/advanced/phase-h-platform-delivery", "example_file": ""},
        {"stage": "Pha I: Governance và Cost", "goals": ["mô hình ownership cho service", "SLO và error budget", "tối ưu chi phí/hiệu năng"], "build": ["service catalog cho team + playbook vận hành"], "tools": ["Backstage", "FinOps dashboards"], "example_path": "learning-path/advanced/phase-i-governance-and-cost", "example_file": ""},
    ]

    capstone_vi = [
        {"name": "Nền tảng Market Intelligence Realtime", "scope": "ingestion -> processing -> alerting -> dashboard", "stack": ["FastAPI", "Kafka", "Redis", "PostgreSQL", "Grafana"]},
        {"name": "Microservice Sự kiện E-commerce", "scope": "catalog, cart, payment, shipment, notification", "stack": ["FastAPI", "RabbitMQ", "Celery", "OpenTelemetry", "Kubernetes"]},
        {"name": "Bộ điều phối AI Workflow", "scope": "job queue, model adapter, usage metering, billing", "stack": ["FastAPI", "Dramatiq", "Redis", "PostgreSQL", "Prometheus"]},
    ]

    open_source_stacks_vi = [
        {"name": "Event-Driven Core", "use_case": "Event domain và giao tiếp bất đồng bộ giữa service.", "packages": ["aiokafka", "pydantic", "tenacity"]},
        {"name": "Queue Worker Core", "use_case": "Xử lý nền đáng tin cậy với retry.", "packages": ["celery", "rabbitmq", "redis"]},
        {"name": "Service Platform Core", "use_case": "Nền API HTTP + DB + migration + cache.", "packages": ["fastapi", "sqlalchemy", "alembic", "redis", "httpx"]},
        {"name": "Observability Core", "use_case": "Metrics, tracing và liên kết log.", "packages": ["prometheus-client", "opentelemetry-sdk", "structlog"]},
        {"name": "Security Core", "use_case": "AuthN/AuthZ và quản lý secrets.", "packages": ["pyjwt", "passlib", "authlib", "hvac"]},
    ]

    mini_projects_vi = [
        {"name": "Cột mốc Advanced 1: Event Pipeline Starter", "path": "learning-path/projects/advanced-event-pipeline-starter", "focus": "Luồng producer-consumer + retry + outbox pattern", "stack": ["Kafka", "RabbitMQ", "SQLite", "Python workers"]},
        {"name": "Cột mốc Advanced 2: Observable Service Platform", "path": "learning-path/projects/advanced-observable-service-platform", "focus": "API + DB + metrics + structured logging + template deploy", "stack": ["FastAPI", "PostgreSQL", "Prometheus", "OpenTelemetry", "Docker"]},
        {"name": "Cột mốc Advanced 3: Capstone E2E Platform", "path": "learning-path/projects/capstone-e2e-platform", "focus": "API + queue + DB + metrics + dashboard + template deploy + tests", "stack": ["http.server", "sqlite3", "pytest", "docker-compose", "k8s manifest"]},
    ]

    architecture_diagrams_vi = [
        {"title": "Luồng Worker RabbitMQ", "file": "assets/diagrams/rabbitmq-flow.svg"},
        {"title": "Luồng Xử lý Stream Kafka", "file": "assets/diagrams/kafka-flow.svg"},
        {"title": "Luồng Transaction Outbox Pattern", "file": "assets/diagrams/outbox-pattern.svg"},
        {"title": "Luồng Điều phối Saga", "file": "assets/diagrams/saga-flow.svg"},
    ]

    extra_examples_vi = [
        {"title": "retry backoff", "path": "learning-path/advanced/extras/retry-backoff/example.py"},
        {"title": "circuit breaker", "path": "learning-path/advanced/extras/circuit-breaker/example.py"},
        {"title": "middleware idempotency", "path": "learning-path/advanced/extras/idempotency-middleware/example.py"},
        {"title": "saga compensation", "path": "learning-path/advanced/extras/saga-compensation/example.py"},
        {"title": "outbox relay", "path": "learning-path/advanced/extras/outbox-relay/example.py"},
        {"title": "contract testing", "path": "learning-path/advanced/extras/contract-testing/example.py"},
        {"title": "pattern tests", "path": "learning-path/advanced/extras/tests/test_patterns.py"},
    ]

    advanced_locales = {
        "en": {
            "title": "Python Advanced Architecture Track",
            "subtitle": "Production roadmap: microservices, queues, streams, reliability, platform engineering.",
            "ui": advanced_ui_en,
            "cheat_sheets": ADVANCED_CHEATSHEET,
            "roadmap": roadmap,
            "java_python_map": java_python_map,
            "open_source_stacks": open_source_stacks,
            "mini_projects": mini_projects,
            "architecture_diagrams": architecture_diagrams,
            "extra_examples": extra_examples,
            "capstone_projects": capstone,
            "recommended_services": advanced_services,
        },
        "vi": {
            "title": "Lộ trình Kiến Trúc Python Nâng Cao",
            "subtitle": "Lộ trình production về microservice, queue, stream, reliability và platform engineering.",
            "ui": advanced_ui_vi,
            "cheat_sheets": advanced_cheatsheet_vi,
            "roadmap": roadmap_vi,
            "java_python_map": java_python_map_vi,
            "open_source_stacks": open_source_stacks_vi,
            "mini_projects": mini_projects_vi,
            "architecture_diagrams": architecture_diagrams_vi,
            "extra_examples": extra_examples_vi,
            "capstone_projects": capstone_vi,
            "recommended_services": advanced_services,
        },
    }

    return {
        "generated_at": generated_at,
        "site": "advanced",
        "default_locale": "en",
        "supported_locales": ["en", "vi"],
        "title": "Python Advanced Architecture Track",
        "subtitle": "Production roadmap: microservices, queues, streams, reliability, platform engineering.",
        "example_root": "learning-path/advanced",
        "cheat_sheets": ADVANCED_CHEATSHEET,
        "roadmap": roadmap,
        "java_python_map": java_python_map,
        "open_source_stacks": open_source_stacks,
        "mini_projects": mini_projects,
        "architecture_diagrams": architecture_diagrams,
        "extra_examples": extra_examples,
        "capstone_projects": capstone,
        "recommended_services": advanced_services,
        "locales": advanced_locales,
    }


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    generated_at = datetime.now(timezone.utc).isoformat()
    services = _load_services()

    catalog = _build_catalog(services, generated_at)
    foundation = _build_foundation_track(services, generated_at)
    advanced = _build_advanced_track(services, generated_at)

    _write_json(CATALOG_FILE, catalog)
    _write_json(FOUNDATION_FILE, foundation)
    _write_json(ADVANCED_FILE, advanced)

    print(f"Built catalog: {CATALOG_FILE}")
    print(f"Built foundation track: {FOUNDATION_FILE}")
    print(f"Built advanced track: {ADVANCED_FILE}")


if __name__ == "__main__":
    main()
