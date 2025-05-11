#!/usr/bin/env python3
import importlib
import sys

REQUIRED = {
    "app.core.exceptions": ["CredentialsException", "ValidationException", "InternalError"],
    "app.core.settings": ["settings"],
    "app.services.llm_service": ["llm_service", "LLMService"],
    "app.core.main": ["app"],
}

errors = []
for module, symbols in REQUIRED.items():
    try:
        mod = importlib.import_module(module)
    except ImportError as e:
        errors.append(f"Módulo ausente: {module} ({e})")
        continue
    for sym in symbols:
        if not hasattr(mod, sym):
            errors.append(f"Símbolo ausente: {module}.{sym}")

if errors:
    print("✖ Erros de contrato detectados:")
    for e in errors:
        print("  -", e)
    sys.exit(1)

print("✔ Todos os contratos essenciais estão presentes.")
sys.exit(0)