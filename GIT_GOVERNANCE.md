# SCRIPT SCRAPPER — GIT GOVERNANCE & CONTRIBUTION SPECIFICATION

**Document Version:** 1.0  
**Authority:** System Architect / CTO  
**Effective Date:** November 6, 2026  
**Status:** Approved for Gate 0 Closure  

---

## 1. BRANCH STRATEGY & TOPOLOGY

The Script Scrapper codebase strictly adheres to a structured Git-Flow branching topology:

```text
main (Protected — Production Releases Only)
  │
  └── develop (Protected — Continuous Integration Branch)
        │
        ├── feature/gate1-foundation
        ├── feature/auth-and-projects
        ├── feature/document-processing
        ├── feature/screenplay-parser
        ├── feature/ai-integration
        └── fix/issue-description
```

### Branch Classifications & Rules

| Branch | Purpose | Base Branch | Merge Target | Direct Commits Allowed? | Protection Rules |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **`main`** | Production-ready, stable releases. Every commit is tagged (`v1.0.0`). | N/A | N/A | **NO** | Mandatory PR, System Architect approval, CI pass. |
| **`develop`** | Active integration branch. Aggregates completed features. | `main` | `main` | **NO** | Mandatory PR, peer review, CI pass. |
| **`feature/*`** | Individual feature implementation. | `develop` | `develop` | **Yes (Author)** | Rebase on `develop` prior to PR submission. |
| **`fix/*`** | Non-critical bug fixes identified in `develop`. | `develop` | `develop` | **Yes (Author)** | Requires unit test proving bug & fix. |
| **`hotfix/*`** | Emergency patches for critical production defects. | `main` | `main` & `develop` | **Yes (Author)** | System Architect sign-off required. |

---

## 2. COMMIT MESSAGE CONVENTIONS

All commits must follow the **Conventional Commits 1.0.0** specification:

```text
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

### Approved Types
- `feat`: A new user-facing feature or API endpoint.
- `fix`: A bug fix in existing functionality.
- `docs`: Documentation modifications or additions only.
- `style`: Code style changes (formatting, semicolons, whitespace) that do not affect logic.
- `refactor`: Code restructuring without bug fixes or new features.
- `perf`: Code changes improving computational performance or reducing memory.
- `test`: Adding missing unit/integration tests or correcting existing tests.
- `chore`: Build scripts, dependencies, configuration, or CI pipeline changes.

### Example Commit Messages
- `feat(auth): implement public registration endpoint with argon2id hashing`
- `fix(parser): correct parenthetical bounding box horizontal offset`
- `docs(adr): approve ADR-014 empirical performance verification plan`
- `test(ocr): add regression test for 300 dpi scanned courier screenplay`

---

## 3. ZERO-CREDENTIALS & DATA LEAKAGE PREVENTION POLICY

To ensure absolute security of proprietary screenplay intellectual property and system keys:

1. **No Credentials in Git:** API keys (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`), database passwords, JWT secrets, and SSL private keys must **NEVER** be committed to source control.
2. **Environment Template Standard:** Secrets must only reside in uncommitted `.env` files. The repository maintains `.env.example` containing dummy key templates.
3. **Screenplay Data Isolation:** Real-world screenplay files (PDF, DOCX, TXT) must never be committed to repository branches. Only synthetic, publicly licensed test fixtures (`fixtures/screenplays/sample_courier.pdf`) may be committed.
4. **Automated Pre-Commit Checks:** Prior to committing, developers must verify `git status` to ensure temporary storage directories (`storage/originals/*`, `storage/backups/*`, `storage/temporary/*`) are ignored.

---

## 4. ARCHITECTURE DECISION RECORD (ADR) GOVERNANCE

1. **Architecture as Code:** All architecture baselines and decision records are version-controlled within `documentation/architecture/`.
2. **Immutability of Approved ADRs:** Once marked `Approved`, an ADR cannot be rewritten. Any change to an approved decision requires authoring a new ADR that explicitly references and supersedes the preceding ADR (e.g. `ADR-005 supersedes ADR-006`).
3. **Approval Gate:** No pull request introducing an architectural deviation or new external dependency may be merged into `develop` without documented System Architect sign-off.

---

## 5. PULL REQUEST & CODE REVIEW PROTOCOL

Before any PR can be merged into `develop` or `main`:
1. **Linear History:** Rebase feature branches on the latest `develop` branch. Squash trivial intermediate commits.
2. **Automated Verification:** All unit and integration test suites must pass cleanly.
3. **Peer Review:** Minimum of one thorough code review from a designated senior engineer.
4. **Evidence Submission:** The PR description must link to the requirement ID, provide terminal output showing passing test commands, and document any database migrations.

---

## 6. REMOTE REPOSITORY PROVISIONING & BRANCH PROTECTION AUDIT

### 6.1 GitHub Remote Repository Configuration & Synchronization Evidence
The Script Scrapper codebase is officially connected and synchronized with GitHub:

- **Remote URL:** `https://github.com/SonaBinu22/script-scrapper.git`
- **Remote Identifier:** `origin`
- **Default Branch:** `main` (Verified via `git remote show origin`)
- **Published Branches & Verified Hashes:**
  - `origin/main` $\longrightarrow$ Commit `5dff8bf8dc349df6c643359a2896b3aecc486a2e` (Protected Release Branch)
  - `origin/develop` $\longrightarrow$ Commit `cd41258edf9988f6a74edbae7faf081046386fa2` (Active Integration Branch)
- **Local Branch Tracking:**
  - `develop` tracks `origin/develop`
  - `main` tracks `origin/main`
- **Network Resolution Standard:** Host Git configured with `http.ipResolve = ipv4` to eliminate Windows NAT64 connection resets.

### 6.2 GitHub Plan Eligibility & Branch Protection Verification
An independent API audit of repository capabilities was conducted against GitHub REST API v3:
- **Repository Visibility:** `Private`
- **Owner Account Type:** Personal User (`SonaBinu22`)
- **Subscription Tier:** **GitHub Free**
- **API Audit Finding:**
  Querying `/repos/SonaBinu22/script-scrapper/rulesets` returned:
  ```json
  {
    "message": "Upgrade to GitHub Pro or make this repository public to enable this feature.",
    "documentation_url": "https://docs.github.com/rest/repos/rules#get-all-repository-rulesets",
    "status": "403"
  }
  ```
- **Governance Attestation:** In accordance with audit instructions (*"Do not claim protection is active until verified"*), **server-side GitHub branch protection is currently UNAVAILABLE due to GitHub Free tier restrictions on private personal repositories**.

### 6.3 Proposed Solutions for Remote Protection
To establish server-side branch protection for `main` and `develop`, the System Architect must select from the following options:
1. **Option A (GitHub Pro Upgrade — Recommended for Private Development):** Upgrade the repository owner account to GitHub Pro ($4/month). This immediately enables full branch protection rules and rulesets for private repositories.
2. **Option B (GitHub Organization Transfer):** Transfer `script-scrapper` to a GitHub Organization on the GitHub Team plan.
3. **Option C (Public Repository):** If proprietary IP confidentiality requirements permit (the codebase maintains zero credentials and synthetic test screenplays only), converting the repository to Public instantly unlocks full branch protection rules on GitHub Free.
4. **Option D (Interim Local Pre-Push Hook Enforcement):** While awaiting account upgrade authorization, enforce branch protection across all engineering team clones via local Git hooks (`.githooks/pre-push`), blocking direct pushes to `main` and `develop`.

---

## 7. TEAM DEVELOPMENT & FEATURE BRANCH TOPOLOGY

All parallel development across the five engineering modules must adhere to the three-tier branching topology:

```text
main (Production Release — Tagged Versions)
  ↑ (PR with System Architect Sign-Off)
develop (Integration Branch — Continuous Integration)
  ↑ (PR with Peer Review + Automated Tests)
feature/<module>-<task>
```

### Approved Gate 1 Feature Branches
- `feature/backend-foundation` — FastAPI initialization, structured logging, error handling, health endpoints.
- `feature/database-foundation` — PostgreSQL 16 schema, SQLAlchemy AsyncEngine pool, Alembic migration 0001.
- `feature/frontend-foundation` — Vite + React 18 SPA, Tailwind CSS, shadcn/ui, client routing.
- `feature/windows-deployment` — Caddy reverse proxy, local CA trust, Windows Firewall rules, storage ACLs.
- `feature/test-infrastructure` — Pytest fixtures, 10-file screenplay test corpora, Locust load benchmarks.

### Development Rules
1. **No Direct Commits to `main`:** `main` reflects only formally signed-off release milestones.
2. **No Direct Commits to `develop`:** All work must originate on an assigned `feature/<module>-<task>` branch.
3. **Mandatory PR & Peer Review:** No branch may merge into `develop` without passing test execution logs and an approving review from a peer engineer or the System Architect.
