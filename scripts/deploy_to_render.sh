#!/usr/bin/env bash
# scripts/deploy_to_render.sh
#
# Script de deploy via Render CLI. Espera:
#   - RENDER_SERVICE_ID
#   - RENDER_API_KEY
#

set -euo pipefail

if [[ -z "${RENDER_SERVICE_ID:-}" ]]; then
  echo "❌ RENDER_SERVICE_ID não definido"; exit 1
fi
if [[ -z "${RENDER_API_KEY:-}" ]]; then
  echo "❌ RENDER_API_KEY não definido"; exit 1
fi

echo "🔄 Deploy no Render: Service ${RENDER_SERVICE_ID}"
render login --api-key "${RENDER_API_KEY}"
render services update "${RENDER_SERVICE_ID}"
render deploy "${RENDER_SERVICE_ID}"
echo "🚀 Deploy acionado"