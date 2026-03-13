#!/usr/bin/env python3
"""Build metadata for the learning portal from local services."""

from __future__ import annotations

import ast
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SERVICES_DIR = ROOT_DIR / "services"
OUTPUT_FILE = ROOT_DIR / "site" / "data" / "catalog.json"

ENTRYPOINT_PRIORITY = ["main.py", "app.py", "index.py", "run.py", "test.py"]
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


def _iter_python_files(service_dir: Path) -> list[Path]:
    files: list[Path] = []
    for path in service_dir.rglob("*.py"):
        if any(part in IGNORE_PARTS for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def _detect_entrypoint(service_dir: Path, python_files: list[Path]) -> str | None:
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

    if service_name in advanced_names or dep_count >= 8 or file_count >= 15:
        return "advanced"
    if service_name in intermediate_names or dep_count >= 4 or file_count >= 6:
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
        local_modules = {
            p.stem
            for p in python_files
            if p.name != "__init__.py"
        }
        top_imports = [
            module
            for module, _ in imports.most_common(20)
            if module not in STDLIB_MODULES and module not in local_modules and module != service_dir.name
        ]
        tech_stack = sorted(set(requirements + top_imports))[:12]
        topics = TOPIC_MAP.get(service_dir.name.lower(), ["python scripting", "module structure"])

        entrypoint = _detect_entrypoint(service_dir, python_files)
        level = _guess_level(service_dir.name, len(python_files), len(requirements))

        services.append(
            {
                "name": service_dir.name,
                "path": str(service_dir.relative_to(ROOT_DIR)),
                "entrypoint": entrypoint,
                "python_files": len(python_files),
                "requirements": requirements,
                "tech_stack": tech_stack[:12],
                "topics": topics,
                "level": level,
            }
        )

    return services


def main() -> None:
    services = _load_services()
    level_counts = Counter(service["level"] for service in services)

    data = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "overview": {
            "service_count": len(services),
            "basic_count": level_counts.get("basic", 0),
            "intermediate_count": level_counts.get("intermediate", 0),
            "advanced_count": level_counts.get("advanced", 0),
        },
        "roadmap": [
            {
                "phase": "1. Basic Foundations",
                "focus": [
                    "variables, data types, operators",
                    "if/else, loops",
                    "functions, arguments, return values",
                    "comments and docstrings",
                    "imports and standard library",
                ],
                "practice_with": ["services/get-data", "services/download-video", "services/basic-bot"],
            },
            {
                "phase": "2. Intermediate Python",
                "focus": [
                    "modular project structure",
                    "working with APIs",
                    "error handling and logging",
                    "files and JSON data",
                    "virtual environments and dependencies",
                ],
                "practice_with": [
                    "services/AI-search-engine",
                    "services/calculator-gradient-image",
                    "services/nft-ai-bot",
                ],
            },
            {
                "phase": "3. Advanced and Microservice Thinking",
                "focus": [
                    "service boundaries and contracts",
                    "schedulers/background jobs",
                    "testing strategy",
                    "external integrations",
                    "deployment and runtime scripts",
                ],
                "practice_with": ["services/crypto-bot", "services/dropshipping-bot", "services/composio"],
            },
            {
                "phase": "4. Specialized Domains",
                "focus": [
                    "web3 and smart contracts",
                    "automation pipelines",
                    "security and secret handling",
                    "project hardening for production",
                ],
                "practice_with": ["services/smart-contract"],
            },
        ],
        "services": services,
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Built site catalog: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
