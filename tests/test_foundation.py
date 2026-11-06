import subprocess
import pytest
from backend.app.core.config import settings
from backend.app.database.connection import engine


def test_connection_budget_invariants():
    """
    Validate that SQLAlchemy connection pool parameters strictly adhere
    to the System Architect's connection budget:
    - pool_size = 15
    - max_overflow = 5
    - per-process peak = 20
    - 2 workers * 20 = 40 peak API connections (well within PostgreSQL 100 limit).
    """
    assert settings.DB_POOL_SIZE == 15
    assert settings.DB_MAX_OVERFLOW == 5
    assert settings.UVICORN_WORKERS == 2
    per_worker_max = settings.DB_POOL_SIZE + settings.DB_MAX_OVERFLOW
    aggregate_api_peak = settings.UVICORN_WORKERS * per_worker_max
    assert per_worker_max == 20
    assert aggregate_api_peak == 40
    # Reserved connections = 3, worker peak = 40, total peak = 83 <= 100
    assert aggregate_api_peak <= 40


def test_caddyfile_validation():
    """
    Verify that the production Caddyfile is syntactically valid according to Caddy binary.
    """
    caddy_exe = r"D:\tools\caddy.exe"
    result = subprocess.run(
        [caddy_exe, "validate", "--config", "Caddyfile"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Valid configuration" in result.stdout or "Valid configuration" in result.stderr


def test_firewall_script_dry_run():
    """
    Verify that configure_firewall.ps1 parses and passes dry-run validation.
    """
    cmd = [
        "powershell",
        "-ExecutionPolicy", "Bypass",
        "-File", r"scripts\configure_firewall.ps1",
        "-DryRun",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0
    assert "DRY RUN" in result.stdout
