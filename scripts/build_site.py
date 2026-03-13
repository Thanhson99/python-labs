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
        "snippet": "user_name = 'hopee'\\nmax_retries = 3\\nis_ready = False",
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

    return {
        "generated_at": generated_at,
        "site": "foundation",
        "title": "Python Foundation Track",
        "subtitle": "Large practical cheatsheet + stepwise roadmap from beginner to strong intermediate.",
        "cheat_sheets": FOUNDATION_CHEATSHEET,
        "roadmap": roadmap,
        "open_source_stacks": open_source_stacks,
        "recommended_services": beginner_services,
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

    return {
        "generated_at": generated_at,
        "site": "advanced",
        "title": "Python Advanced Architecture Track",
        "subtitle": "Production roadmap: microservices, queues, streams, reliability, platform engineering.",
        "cheat_sheets": ADVANCED_CHEATSHEET,
        "roadmap": roadmap,
        "java_python_map": java_python_map,
        "open_source_stacks": open_source_stacks,
        "capstone_projects": capstone,
        "recommended_services": advanced_services,
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
