#!/usr/bin/env bash
# scripts/smoke_test.sh
#
# Teste rápido de health endpoint para CI ou dev.
#

set -euo pipefail

APP_URL=${1:-http://localhost:10000}

echo "🔍 Verificando health em $APP_URL/health"
if curl --fail --silent "$APP_URL/health"; then
  echo "✔ Health OK"
else
  echo "❌ Health FAILED"
  exit 1
fi

echo "✅ Smoke test concluído"