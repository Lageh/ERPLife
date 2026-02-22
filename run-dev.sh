#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

check_port() {
  local PORT="$1"
  if ss -ltn | grep -q ":${PORT} "; then
    echo "Port ${PORT} is already in use. Stop the process using it before running."
    ss -ltnp | grep ":${PORT}" || true
    exit 1
  fi
}

check_port 8001
check_port 8002
check_port 8000

[ -d "${ROOT_DIR}/services/identity-service" ] || { echo "Missing: services/identity-service"; exit 1; }
[ -d "${ROOT_DIR}/services/finance-service" ] || { echo "Missing: services/finance-service"; exit 1; }
[ -d "${ROOT_DIR}/gateway" ] || { echo "Missing: gateway"; exit 1; }

cd "${ROOT_DIR}/services/identity-service"
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload &
deactivate

cd "${ROOT_DIR}/services/finance-service"
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload &
deactivate

cd "${ROOT_DIR}/gateway"
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &

echo "All services started:"
echo "- Identity: http://localhost:8001/health"
echo "- Finance:  http://localhost:8002/health"
echo "- Gateway:  http://localhost:8000/health"

wait
