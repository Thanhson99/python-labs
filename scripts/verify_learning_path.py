#!/usr/bin/env python3
"""Quality gate for learning-path examples."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEARNING = ROOT / "learning-path"

SAMPLES = [
    "learning-path/foundation/stage-01-python-core/main.py",
    "learning-path/foundation/stage-02-data-and-files/transform_data.py",
    "learning-path/foundation/stage-07-storage/sqlite_example.py",
    "learning-path/foundation/stage-08-async-and-concurrency/async_demo.py",
    "learning-path/advanced/phase-c-consistency-patterns/outbox_pattern_example.py",
    "learning-path/advanced/phase-e-reliability-engineering/resilient_http_client.py",
    "learning-path/projects/foundation-cli-data-toolkit/app.py",
    "learning-path/projects/advanced-event-pipeline-starter/event_pipeline.py",
    "learning-path/foundation/extras/decorators/example.py",
    "learning-path/foundation/extras/context-managers/example.py",
    "learning-path/foundation/extras/argparse-subcommands/example.py",
    "learning-path/advanced/extras/retry-backoff/example.py",
    "learning-path/advanced/extras/idempotency-middleware/example.py",
    "learning-path/projects/advanced-observable-service-platform/app.py",
    "learning-path/projects/capstone-e2e-platform/app/repository.py",
    "learning-path/projects/capstone-e2e-platform/app/worker.py",
]


def run_cmd(cmd: list[str], cwd: Path | None = None) -> tuple[bool, str]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd or ROOT),
            capture_output=True,
            text=True,
            timeout=25,
        )
    except Exception as exc:  # noqa: BLE001
        return False, f"exception: {exc}"

    output = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode == 0, output.strip()


def main() -> int:
    py = sys.executable
    failures: list[str] = []

    ok, out = run_cmd([py, "-m", "compileall", "-q", str(LEARNING)])
    if not ok:
        failures.append(f"compileall failed\n{out}")

    for sample in SAMPLES:
        sample_path = ROOT / sample
        cmd = [py, str(sample_path)]

        if sample.endswith("foundation-cli-data-toolkit/app.py"):
            cmd = [
                py,
                str(sample_path),
                "--input",
                str(sample_path.parent / "sample.json"),
                "--status",
                "active",
            ]
        elif sample.endswith("argparse-subcommands/example.py"):
            cmd = [py, str(sample_path), "hello", "--name", "qa"]

        ok, out = run_cmd(cmd, cwd=sample_path.parent)
        if not ok:
            failures.append(f"sample failed: {sample}\n{out}")

    pytest_file = ROOT / "learning-path/foundation/stage-09-testing-and-quality/test_math_utils.py"
    ok, out = run_cmd([py, "-m", "pytest", "-q", str(pytest_file)], cwd=ROOT)
    if not ok:
        failures.append(f"pytest failed\n{out}")

    advanced_tests = ROOT / "learning-path/advanced/extras/tests/test_patterns.py"
    ok, out = run_cmd([py, "-m", "pytest", "-q", str(advanced_tests)], cwd=ROOT)
    if not ok:
        failures.append(f"advanced pattern tests failed\n{out}")

    capstone_tests = ROOT / "learning-path/projects/capstone-e2e-platform/tests/test_repository.py"
    ok, out = run_cmd([py, "-m", "pytest", "-q", str(capstone_tests)], cwd=ROOT)
    if not ok:
        failures.append(f"capstone tests failed\n{out}")

    if failures:
        print("Learning-path quality gate: FAILED")
        for idx, item in enumerate(failures, start=1):
            print(f"\n[{idx}] {item}\n")
        return 1

    print("Learning-path quality gate: PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
