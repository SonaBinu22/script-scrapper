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
