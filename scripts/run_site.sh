#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
START_PORT="${1:-8080}"

find_python_cmd() {
  if command -v python3 >/dev/null 2>&1; then
    echo "python3"
    return
  fi
  if command -v python >/dev/null 2>&1; then
    echo "python"
    return
  fi
  echo ""
}

port_in_use() {
  local port="$1"
  if command -v lsof >/dev/null 2>&1; then
    lsof -iTCP:"${port}" -sTCP:LISTEN -t >/dev/null 2>&1
    return $?
  fi
  if command -v netstat >/dev/null 2>&1; then
    netstat -an 2>/dev/null | grep -E "[\.:]${port} .*LISTEN" >/dev/null 2>&1
    return $?
  fi
  return 1
}

next_free_port() {
  local port="$1"
  "$PYTHON_CMD" - "$port" <<'PY'
import socket
import sys

start = int(sys.argv[1])

for candidate in range(start, start + 200):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", candidate))
    except OSError:
        continue
    finally:
        s.close()
    print(candidate)
    break
else:
    print("")
PY
}

PYTHON_CMD="$(find_python_cmd)"
if [ -z "$PYTHON_CMD" ]; then
  echo "No Python interpreter found (python3/python)." >&2
  exit 1
fi

FREE_PORT="$(next_free_port "$START_PORT")"
if [ -z "$FREE_PORT" ]; then
  echo "Unable to find free port from ${START_PORT}." >&2
  exit 1
fi

"$PYTHON_CMD" "$ROOT_DIR/scripts/build_site.py"

echo "Serving site at http://127.0.0.1:${FREE_PORT} using ${PYTHON_CMD}"
exec "$PYTHON_CMD" "$ROOT_DIR/scripts/serve_site.py" --host 127.0.0.1 --port "$FREE_PORT" --site-dir "$ROOT_DIR/site"
