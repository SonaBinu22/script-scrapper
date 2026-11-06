# SCRIPT SCRAPPER — GATE 1 ACCEPTANCE CRITERIA

**Document Version:** 1.0  
**Authority:** Jarvis — CTO / Architecture and Quality Governance  
**Date:** November 6, 2026  
**Status:** Approved for Gate 1 Verification  

---

## 1. ACCEPTANCE VERIFICATION MATRIX

Gate 1 (Foundation Implementation) will be evaluated strictly against the following 6 objective, verifiable acceptance criteria. No developer claims will be accepted without direct execution logs and terminal output:

| Criteria ID | Verification Area | Target Standard | Verification Command / Method | Pass Criteria |
| :---: | :--- | :--- | :--- | :--- |
| **AC-01** | **Backend Health Check** | FastAPI starts, loads config, binds to 127.0.0.1:8000. | `curl -f http://127.0.0.1:8000/api/v1/health` | Returns HTTP 200 OK, JSON envelope `{"success": true, "data": {"status": "healthy"}}`. |
| **AC-02** | **Database Migrations** | Alembic migration applies all 14 tables with constraints. | `alembic upgrade head`<br>`SELECT table_name FROM information_schema.tables WHERE table_schema='public';` | All 14 tables exist; partial unique index on `script_versions.is_current` verified. |
| **AC-03** | **Connection Pool Bounds** | SQLAlchemy AsyncEngine respects pool limits. | Execute 20 concurrent requests to `/api/v1/system/status`<br>`SELECT count(*), state FROM pg_stat_activity GROUP BY state;` | Active connections $\le 40$ (FastAPI ceiling); zero connection timeouts; zero leaks. |
| **AC-04** | **Frontend Production Build** | Vite SPA compiles and renders without errors. | `npm run build` in `frontend/`<br>`curl -f https://localhost` via Caddy | Exit code 0; bundle size <1.5MB; client routing renders shell layout. |
| **AC-05** | **Caddy LAN HTTPS & CA Trust** | Caddy provisions internal TLS and serves `/system/ca.crt` over configurable host IP or hostname. | `$target = if ($env:HOST_IP_OR_HOSTNAME) { $env:HOST_IP_OR_HOSTNAME } else { (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias 'Ethernet*','Wi-Fi*' | Where-Object { $_.IPAddress -notmatch '^127\.' -and $_.IPAddress -notmatch '^169\.254\.' } | Select-Object -First 1).IPAddress }`<br>`curl -k "https://$target/system/ca.crt" -o test.crt`<br>`(Get-FileHash test.crt -Algorithm SHA256).Hash` | Download succeeds over configurable LAN address; SHA-256 matches host CA fingerprint; browser HTTPS padlock verified without warnings. |
| **AC-06** | **Live Coordinated Backup & Restore (Isolated Environment)** | End-to-end backup and disaster recovery verified strictly in an isolated test database and directory (never modifying production data). | 1. Execute `scripts/backup.ps1`<br>2. Execute `scripts/restore.ps1 -TargetDatabase script_scrapper_test_restore -TargetDir storage/test_restore`<br>3. Verify table counts and row hashes in `script_scrapper_test_restore`<br>4. Drop temporary `script_scrapper_test_restore` and clean `storage/test_restore` | Restored cleanly into isolated test database and directory; table counts and SHA-256 manifest match; zero corruption; production data completely untouched. |

---

## 2. EVIDENCE SUBMISSION PROTOCOL

Upon completion of Gate 1 tasks, the engineering team must submit:
1. Terminal output showing `alembic upgrade head` execution and table verification.
2. Terminal output showing `/api/v1/health` and `/api/v1/system/status` responses.
3. Terminal output showing `SELECT * FROM pg_stat_activity` under simulated load.
4. Browser screenshot demonstrating warning-free HTTPS connection over LAN IP.
5. Execution logs of `scripts/backup.ps1` and `scripts/restore.ps1`.

Gate 2 (Authentication & Project Management) will remain **BLOCKED** until all 6 criteria are verified and signed off by the System Architect and QA Architect.

