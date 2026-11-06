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
| **AC-05** | **Caddy LAN HTTPS & CA Trust** | Caddy provisions internal TLS and serves `/system/ca.crt`. | `curl -k https://192.168.1.150/system/ca.crt -o test.crt`<br>`(Get-FileHash test.crt -Algorithm SHA256).Hash` | Download succeeds; SHA-256 matches host CA fingerprint; HTTPS padlock verified. |
| **AC-06** | **Live Coordinated Backup & Restore** | End-to-end backup and disaster recovery verified. | Execute `scripts/backup.ps1`<br>Drop test table / delete file<br>Execute `scripts/restore.ps1` | Database restored cleanly; manifest SHA-256 matches; zero corruption. |

---

## 2. EVIDENCE SUBMISSION PROTOCOL

Upon completion of Gate 1 tasks, the engineering team must submit:
1. Terminal output showing `alembic upgrade head` execution and table verification.
2. Terminal output showing `/api/v1/health` and `/api/v1/system/status` responses.
3. Terminal output showing `SELECT * FROM pg_stat_activity` under simulated load.
4. Browser screenshot demonstrating warning-free HTTPS connection over LAN IP.
5. Execution logs of `scripts/backup.ps1` and `scripts/restore.ps1`.

Gate 2 (Authentication & Project Management) will remain **BLOCKED** until all 6 criteria are verified and signed off by the System Architect and QA Architect.
