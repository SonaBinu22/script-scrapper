# SCRIPT SCRAPPER — FIVE-MEMBER TEAM MODULE ASSIGNMENT

**Document Version:** 1.0  
**Authority:** Jarvis — CTO / Architecture and Quality Governance  
**Date:** November 6, 2026  
**Status:** Approved for Gate 1 Execution  

---

## 1. ORGANIZATIONAL MATRIX & ROLE BREAKDOWN

To ensure rigorous accountability, zero overlapping ambiguity, and strict ownership, the five production team members are assigned clear domain responsibilities across Gate 1 and subsequent development phases:

```text
====================================================================================================
                        FIVE-MEMBER PRODUCTION TEAM ALLOCATION
====================================================================================================

  [ Member 1: System Architect ]         --> Governance, Architecture Approval, PR Review, Release Gates
  [ Member 2: Senior Backend Engineer ]  --> FastAPI Core, PostgreSQL 16, SQLAlchemy 2.0, Alembic, Queue
  [ Member 3: Senior Frontend Engineer ] --> Vite + React 18 SPA, TypeScript, Tailwind, shadcn/ui, State
  [ Member 4: DevOps & Platform Eng ]    --> Caddy Reverse Proxy, Windows Services, Firewall, Backups
  [ Member 5: QA & Test Architect ]      --> Automated Testing, Screenplay Corpora, Locust Benchmarks
====================================================================================================
```

---

## 2. DETAILED MEMBER ASSIGNMENTS & DELIVERABLES (GATE 1)

### Member 1: System Architect / Governance Lead
- **Direct Responsibility:** Architecture Compliance, Governance Approval, and Release Gating.
- **Assigned Modules:** Overall Architecture Governance, Gate Approval Reviews.
- **Specific Deliverables:**
  - Independent architectural review of all Pull Requests merging into `develop` or `main`.
  - Final approval and sign-off on database schema migrations and external API contracts.
  - Formal closure authorization for Gate 1 upon reviewing QA evidence.
- **Dependencies:** None. Operates as the governing authority.
- **Test / Evidence Responsibilities:** Verify compliance against `FINAL_ARCHITECTURE_BASELINE_v1.3.md` and approved ADRs.

### Member 2: Senior Backend Engineer
- **Direct Responsibility:** Database Layer, Core Backend Application & Task Queue Engine.
- **Assigned Modules:** Module 2 (Database Foundation), Module 3 (Backend Foundation).
- **Specific Deliverables:**
  - `backend/app/core/config.py`: Pydantic Settings configuration loader.
  - `backend/app/database/connection.py`: SQLAlchemy AsyncEngine connection pool (`pool_size=15`, `max_overflow=5` per Uvicorn worker process, max 40 API peak).
  - `backend/migrations/versions/0001_initial_schema.py`: Alembic migration establishing all 14 core tables.
  - `backend/app/api/v1/health.py`: Healthcheck (`/health`) and system status (`/system/status`) endpoints.
  - `backend/app/core/exceptions.py`: Global exception handlers and error envelope schemas.
- **Dependencies:** Member 1 (Approved DDL Schema), Member 4 (PostgreSQL 16 Windows Service running).
- **Acceptance Criteria:** Satisfy AC-01 (Backend Health), AC-02 (Database Migrations), AC-03 (Connection Pool Bounds).
- **Evidence Requirements:** Terminal logs of `alembic upgrade head`, JSON responses for `/api/v1/health` and `/api/v1/system/status`.

### Member 3: Senior Frontend Engineer
- **Direct Responsibility:** User Interface Client, Design System & Client State.
- **Assigned Modules:** Module 4 (Frontend Foundation).
- **Specific Deliverables:**
  - `frontend/`: Clean Vite + React 18+ TypeScript application skeleton.
  - `frontend/src/index.css`: Tailwind CSS configuration with design tokens.
  - `frontend/src/components/ui/`: Base shadcn/ui primitives (`Button`, `Card`, `Input`, `Alert`).
  - `frontend/src/router.tsx`: Client-side routing with placeholder views (`/login`, `/register`, `/dashboard`).
  - `frontend/src/services/api-client.ts`: Axios API client with automatic CSRF header injection.
  - Production build output in `frontend/dist/`.
- **Dependencies:** Member 2 (Base API endpoints contract).
- **Acceptance Criteria:** Satisfy AC-04 (Frontend Production Build).
- **Evidence Requirements:** Zero-error TypeScript compilation log (`tsc --noEmit`), clean `npm run build` console output.

### Member 4: DevOps & Windows Platform Engineer
- **Direct Responsibility:** Host Ingress, Windows Service Architecture, Security & Disaster Recovery.
- **Assigned Modules:** Module 5 (Windows Deployment Foundation), Operational Scripting.
- **Specific Deliverables:**
  - `Caddyfile`: Reverse proxy, internal CA, static file routing (`try_files`), and `/system/ca.crt` endpoint.
  - `scripts/backup.ps1` & `scripts/restore.ps1`: Production coordinated backup and recovery scripts.
  - Windows Service definitions via WinSW or NSSM (`ScriptScrapper-API`, `ScriptScrapper-Proxy`, `ScriptScrapper-Worker`).
  - Windows Firewall configuration restricting ports 80/443 strictly to the configurable actual local LAN subnet (`$env:LAN_SUBNET`) and constraining IPv6 to Link-Local / ULA.
  - NTFS permissions hardening on `storage/` and `%LOCALAPPDATA%\Caddy\certificates\local\root.key`.
- **Dependencies:** Member 2 (Backend executable target), Member 3 (`frontend/dist/` build target).
- **Acceptance Criteria:** Satisfy AC-05 (Caddy Ingress & CA Trust over configurable host address), AC-06 (Live Coordinated Backup & Restore in isolated test environment).
- **Evidence Requirements:** Browser HTTPS connection logs over configurable host address, SHA-256 fingerprint verification output, successful isolated `scripts/backup.ps1` and `scripts/restore.ps1` execution logs.

### Member 5: QA & Test Architect
- **Direct Responsibility:** Test Frameworks, Screenplay Test Corpora & Independent Evidence Audit.
- **Assigned Modules:** Test Infrastructure & Verification.
- **Specific Deliverables:**
  - `tests/`: Pytest configuration (`pytest.ini`), database test fixtures with transactional rollback.
  - `fixtures/screenplays/`: Assembly of the 10-file screenplay test corpus (Letter, A4, Rotated, Cropped, Scanned OCR).
  - `tests/benchmarks/locustfile.py`: Locust concurrency benchmark suite for 5, 10, and 20 users.
  - Independent verification of all Gate 1 Acceptance Criteria (AC-01 through AC-06).
  - Formal submission of the Gate 1 Acceptance Evidence Package to Member 1 (System Architect).
- **Dependencies:** Member 2 (API endpoints), Member 4 (Running services).
- **Acceptance Criteria:** 100% of Gate 1 automated test suites execute and pass.
- **Evidence Requirements:** Formally compiled Gate 1 Verification Report with reproducible test logs and terminal output.

---

## 3. DEVELOPMENT & QUALITY WORKFLOW (THE 6-STEP CYCLE)

Every task executed by any team member must strictly adhere to the project governance cycle:

$$\mathbf{PLAN} \longrightarrow \mathbf{IMPLEMENT} \longrightarrow \mathbf{TEST} \longrightarrow \mathbf{EVIDENCE} \longrightarrow \mathbf{REVIEW} \longrightarrow \mathbf{APPROVAL}$$

1. **PLAN:** Author implementation plan referencing specific requirement IDs and branch conventions.
2. **IMPLEMENT:** Write code strictly within the assigned module scope on a feature branch (`feature/*`).
3. **TEST:** Execute automated unit and integration tests proving correctness and zero regressions.
4. **EVIDENCE:** Capture terminal outputs, database query logs, and reproducible verification scripts.
5. **REVIEW:** Submit Pull Request to `develop` for independent peer review (Jarvis + peer engineer).
6. **APPROVAL:** System Architect reviews compliance and authorizes merge into `develop`.

