"""Advanced pathlib operations."""

from pathlib import Path


if __name__ == "__main__":
    base = Path(__file__).resolve().parent
    py_files = sorted(p.name for p in base.rglob("*.py"))
    print({"count": len(py_files), "files": py_files})
