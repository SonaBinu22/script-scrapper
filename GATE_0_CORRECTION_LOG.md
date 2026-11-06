# SCRIPT SCRAPPER — GATE 0 CORRECTION LOG

**Document Version:** 1.0  
**Authority:** Jarvis — CTO / Architecture and Quality Governance  
**Date:** November 6, 2026  
**Status:** Approved for Gate 0 Closure  

---

## 1. COMPREHENSIVE ARCHITECTURAL CORRECTION REGISTER

This log documents all technical corrections, rationales, and repository impacts enacted during the Gate 0 architectural audit and revision process:

| Log ID | Domain | Initial Baseline v1.0 Flaw | Corrective Architectural Action | Repository Document Updated | Status |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **COR-01** | **Task Queue** | RQ relied on POSIX `os.fork()`, causing immediate fatal crashes on Windows native host. | Replaced RQ with PostgreSQL `FOR UPDATE SKIP LOCKED` worker and `LISTEN / NOTIFY`. Eliminates Redis. | Baseline v1.3 Part 4, ADR-005 | **Resolved & Committed** |
| **COR-02** | **Frontend** | Next.js SSR required persistent Node container (~250MB RAM) for a single-machine local app. | Adopted Vite + React 18+ (SPA) with TypeScript and Tailwind CSS. Static files served directly by Caddy. | Baseline v1.3 Part 1, ADR-001 | **Resolved & Committed** |
| **COR-03** | **Relational DB** | Circular foreign key deadlock between `scripts.current_version_id` and `script_versions.script_id`. | Removed `current_version_id`. Designated active version via `script_versions.is_current = TRUE` partial unique index. | Baseline v1.3 Part 1, ADR-010 | **Resolved & Committed** |
| **COR-04** | **Screenplay Schema**| Schema only stored scenes and dialogue; Action lines and Parentheticals were completely omitted. | Introduced unified `scene_elements` table storing Action, Character, Parenthetical, Dialogue, and Transition elements. | Baseline v1.3 Part 1, ADR-008 | **Resolved & Committed** |
| **COR-05** | **REST APIs** | Complete omission of screenplay content reader endpoints (`/scenes`, `/elements`, `/characters`). | Added full suite of paginated screenplay reader endpoints, member management APIs, and job cancellation. | Baseline v1.3 Part 1 | **Resolved & Committed** |
| **COR-06** | **LAN Security** | Baseline specified plain HTTP (`http://LOCAL-IP`), exposing session cookies to LAN eavesdropping. | Mandated Caddy v2 with automated internal CA TLS, enforcing HTTPS and `Secure; HttpOnly; SameSite=Lax` cookies. | Baseline v1.3 Part 5, ADR-009 | **Resolved & Committed** |
| **COR-07** | **Authentication**| Public registration excluded; required manual administrative provisioning for all users. | Implemented public registration with SHA-256 email verification tokens, rate limiting, and default `STANDARD_USER`. | Baseline v1.3 Part 8, ADR-011 | **Resolved & Committed** |
| **COR-08** | **Governance** | Unclear co-ownership rules creating potential project governance deadlocks. | Enforced exactly one primary `PROJECT_OWNER` per project (`projects.owner_id`); collaborators assigned `EDITOR`/`VIEWER`. | Baseline v1.3 Part 8, ADR-013 | **Resolved & Committed** |
| **COR-09** | **Pool Sizing** | Connection allocation arithmetic totaled 90 instead of 100 connections. | Standardized connection budget to exact 100: 40 API Peak, 2 Worker, 5 Admin, 3 Watchdog, 3 Superuser, 47 Free. | Baseline v1.3 Part 3 | **Resolved & Committed** |
| **COR-10** | **Pool Strategy** | Incompatible mixing of raw `asyncpg.create_pool` parameters with SQLAlchemy engine arguments. | Selected single strategy: SQLAlchemy 2.0 `AsyncEngine` with `asyncpg` driver (`postgresql+asyncpg://...`). | Baseline v1.3 Part 3, ADR-003 | **Resolved & Committed** |
| **COR-11** | **Job Claiming SQL**| Malformed scalar subquery `WHERE id = (SELECT id FROM ... FOR UPDATE SKIP LOCKED)` was syntactically invalid in Postgres. | Replaced with canonical, atomic CTE: `WITH next_job AS (...) UPDATE processing_jobs j ... FROM next_job`. | Baseline v1.3 Part 4, ADR-005 | **Resolved & Committed** |
| **COR-12** | **DB Transactions**| Risk of holding database transactions open during multi-minute OCR or AI operations. | Strictly mandated 3-phase lifecycle: Claim (short tx) $\rightarrow$ Execute OCR/AI (OUTSIDE tx) $\rightarrow$ Persist results (short tx). | Baseline v1.3 Part 4 | **Resolved & Committed** |
| **COR-13** | **CA Security** | Instructed operators to delete CA storage directory as routine recovery; insecure certificate download. | Prohibited CA deletion; mandated restricted NTFS ACLs on `root.key`; mandated out-of-band SHA-256 fingerprint verification. | Baseline v1.3 Part 5, ADR-009 | **Resolved & Committed** |
| **COR-14** | **CIR Coordinate Space**| Coordinates assumed fixed US Letter points, failing on A4 paper, rotated pages, or non-zero CropBoxes. | Standardized coordinate contract to top-left unrotated origin; defined proportional margin classification for Letter & A4. | Baseline v1.3 Part 6, ADR-007 | **Resolved & Committed** |
| **COR-15** | **Audit Evidence** | Documentation of procedures (e.g. backup restore, load testing) was previously marked as "VERIFIED". | Reclassified unexecuted implementation-stage tests to `DOCUMENTED` or `NOT TESTED`; assigned live tests to Gate 1/3/7. | `GATE_0_CLOSURE_CHECKLIST.md` | **Resolved & Committed** |
| **COR-16** | **Connection Pooling** | Uvicorn worker count unspecified; aggregate per-process pool multiplication risked exceeding connection budget. | Mandated 2 Uvicorn workers; each process configured with `pool_size=15`, `max_overflow=5` (20 max per process, 40 peak API). Total across all processes ($40+2+5+3+3+47=100$) confirmed within PostgreSQL ceiling. | Baseline v1.3 Part 3 | **Resolved & Committed** |
| **COR-17** | **Worker SQL Testing** | Worker CTE SQL needed formal transaction boundary check and execution milestone assignment. | Formally validated CTE syntax; documented strict short-transaction boundaries (<50ms claim, processing outside DB tx, <200ms write); assigned live execution testing to Gate 1. | Baseline v1.3 Part 4 | **Resolved & Committed** |
| **COR-18** | **Windows Firewall** | Firewall allowed overly broad LAN ranges; lacked explicit IPv6 scoping and host port isolation confirmation. | Replaced broad CIDRs with configurable subnet (`$env:LAN_SUBNET`); restricted IPv6 to Link-Local/ULA; verified FastAPI (8000) and PostgreSQL (5432) bind to loopback only. | Baseline v1.3 Part 9 | **Resolved & Committed** |
| **COR-19** | **Git Governance** | Remote branch protection not formally attested as pending remote provisioning before parallel work. | Documented private GitHub/GitLab remote setup and PR rules; classified remote protection as `DOCUMENTED (PENDING REMOTE PROVISIONING)` until verified. | `GIT_GOVERNANCE.md` | **Resolved & Committed** |
| **COR-20** | **Gate 1 Acceptance** | Hardcoded IP `192.168.1.150` in AC-05; AC-06 restore test risked dropping production development data. | AC-05 updated to configurable host addressing (`HOST_IP_OR_HOSTNAME`); AC-06 updated to mandate isolated test database and directory for restoration verification. | `GATE_1_ACCEPTANCE_CRITERIA.md` | **Resolved & Committed** |
| **COR-21** | **Remote Integration** | Remote repository unlinked; branch protection feasibility unverified against actual GitHub plan. | Connected `origin` to `https://github.com/SonaBinu22/script-scrapper.git`; published `main` and `develop`; audited GitHub API, identifying Free plan limitation on private personal repos; documented solutions & local pre-push enforcement. | `GIT_GOVERNANCE.md` Section 6 | **Resolved & Committed** |

---

## 2. AUDIT COMPLIANCE ATTESTATION

All 21 corrective actions have been applied to the authoritative baseline documentation, verified for architectural consistency, and tracked in Git. Zero unresolved technical contradictions remain.

