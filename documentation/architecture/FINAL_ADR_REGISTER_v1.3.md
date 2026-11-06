# SCRIPT SCRAPPER — FINAL ARCHITECTURE DECISION RECORD (ADR) REGISTER v1.3

**Document Version:** 1.3  
**Status:** Approved for Gate 0 Closure Preparation  
**Authority:** System Architect / CTO  
**Date:** November 6, 2026  

---

## INDEX OF APPROVED ARCHITECTURAL DECISIONS

| ADR ID | Decision Summary | Status | Supersedes | Approved Version |
| :--- | :--- | :---: | :--- | :---: |
| **ADR-001** | **Vite + React SPA Frontend Architecture** | **Approved** | ADR-001 (v1.0 Next.js) | v1.1 |
| **ADR-002** | **FastAPI Python Async ASGI Backend** | **Approved** | ADR-002 (v1.0) | v1.0 |
| **ADR-003** | **PostgreSQL 16 Relational Database Engine** | **Approved** | ADR-003 (v1.0) | v1.0 |
| **ADR-004** | **Modular Monolith Software Architecture** | **Approved** | ADR-004 (v1.0) | v1.0 |
| **ADR-005** | **PostgreSQL SKIP LOCKED Background Queue**| **Approved** | ADR-006 (v1.0 RQ) | v1.1 |
| **ADR-006** | **Tesseract OCR (v5.3+) Engine Integration** | **Approved** | N/A (New) | v1.1 |
| **ADR-007** | **PyMuPDF Bounding-Box Coordinate Extraction** | **Approved** | N/A (New) | v1.1 |
| **ADR-008** | **Unified Scene Elements Relational Table** | **Approved** | N/A (New) | v1.1 |
| **ADR-009** | **Caddy v2 Reverse Proxy with Internal CA** | **Approved** | N/A (New) | v1.1 |
| **ADR-010** | **Partial Unique Index for Active Version** | **Approved** | N/A (New) | v1.1 |
| **ADR-011** | **Public Registration with Email Verification** | **Approved** | ADR-011 (v1.1) | v1.2 |
| **ADR-012** | **Multi-Computer LAN Deployment Topology** | **Approved** | ADR-010 (v1.0) | v1.2 |
| **ADR-013** | **Single Primary Project Owner Governance** | **Approved** | N/A (New) | v1.2 |
| **ADR-014** | **Empirical Performance Verification Plan** | **Approved** | N/A (New) | v1.2 |

---

## DETAILED DECISION RECORDS

### ADR-001: Vite + React SPA Frontend Architecture
- **Context:** Baseline v1.0 specified Next.js. However, Next.js requires a persistent Node.js runtime container (~250MB RAM) and App Router static export exhibits quirks with dynamic routes.
- **Decision:** Adopt Vite + React 18+ (SPA) with TypeScript, Tailwind CSS, shadcn/ui, Zustand, and TanStack Query.
- **Consequences:** Eliminates Node.js production runtime container. Static build served directly by Caddy. Cuts host memory consumption by ~250MB.

### ADR-002: FastAPI Python Async ASGI Backend
- **Context:** Need high-performance, asynchronous REST API with automatic schema validation and documentation.
- **Decision:** Adopt Python 3.11+ with FastAPI, Pydantic v2, and Uvicorn.
- **Consequences:** Native OpenAPI documentation generation, strict validation, high asynchronous request throughput.

### ADR-003: PostgreSQL 16 Relational Database Engine
- **Context:** Multi-user concurrent access on LAN causes SQLite write lock contention (`SQLITE_BUSY`).
- **Decision:** Adopt PostgreSQL 16 with JSONB support.
- **Consequences:** MVCC row-level locking supports concurrent users and workers; indexed JSONB enables rich analysis queries.

### ADR-004: Modular Monolith Software Architecture
- **Context:** Avoiding premature microservices complexity while maintaining clean module boundaries.
- **Decision:** Implement a modular monolith with discrete domains (`auth`, `projects`, `scripts`, `processing`, `ai`).
- **Consequences:** Single deployable unit, straightforward transactions, zero distributed network latency.

### ADR-005: PostgreSQL SKIP LOCKED Background Task Queue
- **Context:** Redis Queue (RQ) relies strictly on POSIX `os.fork()`, which fatally crashes on native Windows environments.
- **Decision:** Implement background worker queue using PostgreSQL `SELECT ... FOR UPDATE SKIP LOCKED` combined with `LISTEN / NOTIFY`.
- **Consequences:** 100% native Windows compatibility. Eliminates Redis service dependency. 100% ACID persistence.

### ADR-006: Tesseract OCR (v5.3+) Engine Integration
- **Context:** Confirmed requirement mandates processing scanned and image-based PDF screenplays.
- **Decision:** Integrate Tesseract OCR (v5.3+) via PyMuPDF 300 DPI rasterization and `pytesseract`.
- **Consequences:** Permissive Apache 2.0 license. Word-level bounding box coordinates preserve typographical margins. Memory usage <150MB.

### ADR-007: PyMuPDF Bounding-Box Coordinate Extraction
- **Context:** Plain-text PDF extraction strips visual indentation margins, crippling character and dialogue parsing accuracy.
- **Decision:** Mandate PyMuPDF coordinate extraction (`page.get_text("blocks")` / `"words"`).
- **Consequences:** Captures $(x_0, y_0, x_1, y_1)$ bounding coordinates for typographical classification of sluglines, characters, and dialogue.

### ADR-008: Unified Scene Elements Relational Table
- **Context:** Baseline v1.0 only stored scenes and dialogue, omitting Action descriptions, Parentheticals, and Transitions.
- **Decision:** Introduce a unified `scene_elements` table linked to `scenes` with strict `sequence_index`.
- **Consequences:** Screenplays can be reconstructed and rendered with 100% textual fidelity in the reader UI.

### ADR-009: Caddy v2 Reverse Proxy with Automated Local CA
- **Context:** Multi-computer LAN access requires HTTPS to protect authentication cookies, but self-signed certificates cause browser security warnings.
- **Decision:** Adopt Caddy v2 with its embedded internal Certificate Authority (`local_certs`).
- **Consequences:** Single executable (`caddy.exe`). Exposes root CA certificate at `/system/ca.crt` for one-click client trust installation.

### ADR-010: Partial Unique Index for Active Script Version
- **Context:** Circular foreign key between `scripts.current_version_id` and `script_versions.script_id` caused insertion deadlocks.
- **Decision:** Remove `current_version_id` from `scripts`. Designate active version via `script_versions.is_current = TRUE` with partial unique index.
- **Consequences:** Clean relational insertions and version rollback capabilities without constraint conflicts.

### ADR-011: Public Registration with Email Verification
- **Context:** Phase 0.2 Decision 1 mandated open registration while preventing malicious bot abuse.
- **Decision:** Provide public registration endpoint with SHA-256 hashed email verification tokens and rate limiting. Immutable default role: `STANDARD_USER`.
- **Consequences:** Seamless onboarding; new users strictly isolated from existing projects.

### ADR-012: Multi-Computer LAN Deployment Topology
- **Context:** Phase 0.2 Decision 2 mandated simultaneous multi-computer access across LAN devices.
- **Decision:** Deploy single centralized Windows host running backend, DB, worker, and Caddy; remote browser clients connect over HTTPS.
- **Consequences:** Zero client-side installation. Centralized data backup and governance.

### ADR-013: Single Primary Project Owner Governance
- **Context:** Need unambiguous project ownership to prevent administrative deadlocks.
- **Decision:** Enforce exactly one primary `PROJECT_OWNER` per project in `projects.owner_id`. Collaborators assigned `PROJECT_EDITOR` or `PROJECT_VIEWER`.
- **Consequences:** Clear project deletion and ownership transfer hierarchy.

### ADR-014: Empirical Performance Verification Plan
- **Context:** Architecture rules prohibit claiming performance targets without empirical measurement.
- **Decision:** Mandate automated Locust load testing across 5, 10, and 20 simultaneous users recording CPU, RAM, DB connections, and OCR throughput.
- **Consequences:** High confidence in multi-client stability before production sign-off.
