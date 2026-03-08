#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INFRA_DIR="${ROOT_DIR}/infra"
FRONT_DIR="${ROOT_DIR}/frontend/apps/web"

IDENTITY_DIR="${ROOT_DIR}/services/identity-service"
FINANCE_DIR="${ROOT_DIR}/services/finance-service"
GATEWAY_DIR="${ROOT_DIR}/gateway"

BACK_PID=""
FRONT_PID=""

cleanup() {
  echo ""
  echo "Stopping frontend and backend..."
  if [ -n "${FRONT_PID}" ]; then
    kill "${FRONT_PID}" 2>/dev/null || true
  fi
  if [ -n "${BACK_PID}" ]; then
    kill "${BACK_PID}" 2>/dev/null || true
  fi

  echo "Stopping Postgres (docker compose down)..."
  cd "${INFRA_DIR}"
  docker compose down || true
}

trap cleanup EXIT INT TERM

ensure_python_deps() {
  local SERVICE_DIR="$1"
  echo "==> Ensuring Python deps in: ${SERVICE_DIR}"

  cd "${SERVICE_DIR}"

  # Se a venv não existe, cria
  if [ ! -d ".venv" ]; then
    python3 -m venv .venv
  fi

  # Ativa a venv
  source .venv/bin/activate

  # Se o pip estiver quebrado/corrompido, recria a venv inteira
  if ! python3 -m pip --version >/dev/null 2>&1; then
    deactivate || true
    rm -rf .venv
    python3 -m venv .venv
    source .venv/bin/activate
  fi

  # Atualiza pip e instala dependências do requirements.txt
  python3 -m pip install --upgrade pip
  python3 -m pip install -r requirements.txt

  deactivate
}

ensure_frontend_deps() {
  echo "==> Ensuring frontend deps in: ${FRONT_DIR}"
  cd "${FRONT_DIR}"
  if [ ! -d "node_modules" ]; then
    npm install
  fi
}

echo "==> Starting Postgres..."
cd "${INFRA_DIR}"
docker compose up -d
docker compose ps

ensure_python_deps "${IDENTITY_DIR}"
ensure_python_deps "${FINANCE_DIR}"
ensure_python_deps "${GATEWAY_DIR}"
ensure_frontend_deps

echo "==> Starting backend (identity/finance/gateway)..."
cd "${ROOT_DIR}"
./run-dev.sh &
BACK_PID=$!

echo "==> Starting frontend (Vite)..."
cd "${FRONT_DIR}"
npm run dev -- --host 0.0.0.0 &
FRONT_PID=$!

echo ""
echo "All started:"
echo "- Gateway:  http://localhost:8000/health"
echo "- Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop everything."

wait
