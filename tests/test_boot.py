import pytest
from fastapi import FastAPI

def test_boot():
    from app.core import main
    assert hasattr(main, "app"), "main.app não encontrado"
    assert isinstance(main.app, FastAPI), "main.app não é FastAPI"

def test_validate_contracts():
    import subprocess
    result = subprocess.run(
        ["python", "scripts/validate_contracts.py"],
        capture_output=True
    )
    assert result.returncode == 0, f"Contracts inválidos:\n{result.stderr.decode()}"