# SCRIPT SCRAPPER

## SYSTEM ARCHITECTURE BASELINE v1.0

**Document Classification:** Technical Architecture & Development Governance  
**Version:** 1.0  
**Status:** Proposed Baseline — Pending Architecture Approval  
**Product:** Script Scrapper  
**Architecture Owner:** System Architect  
**Development Environment:** Antigravity  
**Development Team:** 5 Members  
**Primary Development Governance:** System Architect + ChatGPT + Antigravity

---

# PART 1 — PROJECT DEFINITION

## 1.1 Product Overview

Script Scrapper is a lightweight, web-based screenplay processing and analysis application.

The initial implementation will operate as a locally hosted application rather than a SaaS platform.

The application will primarily run on one computer. Users will access it through a web browser on that computer, with optional access from other devices through the local network.

External AI APIs will be integrated for features requiring AI-based interpretation and analysis.

The system must support the following screenplay document formats:

1. PDF
2. DOCX
3. TXT
4. Fountain

## 1.2 Architectural Objectives

The architecture must satisfy these objectives:

1. Lightweight application execution.
2. Reliable screenplay document extraction.
3. Consistent screenplay parsing across supported formats.
4. Separation of deterministic processing and AI-based analysis.
5. Local storage of original documents and processing results.
6. Secure user authentication and authorization.
7. Modular and maintainable backend architecture.
8. Independently testable components.
9. Reproducible development and deployment.
10. Future migration to centralized or cloud hosting without major architectural reconstruction.

## 1.3 Initial Scope Boundaries

### Included

- Web application.
- Local installation.
- Optional LAN access.
- User authentication.
- Project management.
- Screenplay upload.
- Four document formats.
- Document extraction.
- Screenplay structural parsing.
- Background processing.
- External AI integration.
- Analysis result storage.
- Results interface.
- Backup and restoration.
- Testing and performance optimization.

### Excluded from Initial Release

- Subscription management.
- Payment gateway.
- SaaS billing.
- Tenant-based infrastructure.
- Kubernetes.
- Microservices.
- Distributed databases.
- Public user registration.
- Public cloud file storage.
- Dedicated vector database.

These exclusions can be reconsidered through future architecture decisions.

---

# PART 2 — FINAL TECHNOLOGY STACK

## 2.1 Frontend

| Technology | Responsibility |
| --- | --- |
| Next.js | Frontend application framework |
| React | UI architecture |
| TypeScript | Type safety |
| Tailwind CSS | Styling |
| shadcn/ui | Component foundation |
| Zustand | Client-side state |
| TanStack Query | Server-state management |
| React Hook Form | Form management |
| Zod | Frontend validation |

### Frontend development rules

- Use TypeScript throughout.
- Prefer reusable components.
- Separate UI components from business logic.
- Do not put API communication directly inside large UI components.
- Centralize API configuration.
- Implement loading, error and empty states.
- Avoid unnecessary client-side rendering.
- Avoid introducing additional state libraries without justification.

## 2.2 Backend

| Technology | Responsibility |
| --- | --- |
| Python | Primary backend language |
| FastAPI | REST API framework |
| Pydantic | Request and response validation |
| SQLAlchemy | ORM |
| Alembic | Database migrations |
| Uvicorn | ASGI server |

### Backend development rules

- Follow modular architecture.
- Keep business logic outside API route handlers.
- Use dependency injection where appropriate.
- Validate all incoming requests.
- Use asynchronous operations where they provide genuine benefits.
- Keep database access behind repository interfaces.
- Never expose internal exceptions or sensitive information to users.

## 2.3 Database

| Technology | Responsibility |
| --- | --- |
| PostgreSQL | Primary relational database |
| SQLAlchemy | Database access |
| Alembic | Schema versioning |
| JSONB | Extensible structured metadata |

PostgreSQL is the single source of truth for application records.

We will not introduce MongoDB.

pgvector is not part of the initial stack.

## 2.4 Background Processing

| Technology | Responsibility |
| --- | --- |
| Redis | Job queue coordination |
| RQ | Background task execution |
| Python worker | Document processing and analysis |

The worker must run separately from the FastAPI request-handling process.

## 2.5 Document Processing

| Technology | Responsibility |
| --- | --- |
| PyMuPDF | PDF extraction |
| python-docx | DOCX extraction |
| Python standard libraries | TXT handling |
| Fountain parser adapter | Fountain parsing |
| Custom screenplay parser | Structural interpretation |
| lxml | XML processing when required |

A specific Fountain parser library must be selected only after a short compatibility and accuracy evaluation.

## 2.6 AI Integration

- External AI provider APIs.
- Provider-independent service interface.
- Version-controlled prompts.
- Pydantic response validation.
- Usage and cost tracking.
- Retry and timeout policies.

## 2.7 Infrastructure

| Technology | Responsibility |
| --- | --- |
| Docker | Containerization |
| Docker Compose | Local orchestration |
| Nginx | Reverse proxy |
| GitHub | Source control |
| GitHub Actions | CI/CD |
| Linux | Preferred production operating system |
| Pytest | Backend testing |
| Vitest | Frontend unit testing |
| Playwright | Browser-based testing |

---

# PART 3 — SYSTEM ARCHITECTURE

## 3.1 Architecture Pattern

The approved architectural direction is:

**Modular Monolith + Separate Background Worker**

We will not implement microservices in the initial version.

The backend will be deployed as one application with clearly separated modules.

The processing worker will be deployed separately but will reuse the same application services and domain logic.

## 3.2 High-Level Architecture

```text
                    USERS
                      |
                      |
                WEB BROWSER
                      |
                      |
               LOCAL APPLICATION
                      |
                    NGINX
                      |
             +--------+--------+
             |                 |
         NEXT.JS             FASTAPI
         FRONTEND            BACKEND
                               |
                 +-------------+-------------+
                 |             |             |
              AUTH         PROJECTS       SCRIPTS
                 |             |             |
                 +-------------+-------------+
                               |
                         SERVICE LAYER
                               |
                 +-------------+-------------+
                 |             |             |
              DATABASE    PROCESSING      AI SERVICE
                 |          ENGINE             |
                 |             |          EXTERNAL API
                 |          REDIS              |
                 |             |               |
                 |          WORKER              |
                 |             |               |
                 +-------------+---------------+
                               |
                         LOCAL STORAGE
                               |
                         RESULTS STORE
```

## 3.3 Application Execution Flow

1. User opens Script Scrapper.
2. Frontend loads.
3. User authenticates.
4. User selects or creates a project.
5. User uploads a screenplay.
6. Backend validates the document.
7. Backend stores the original file.
8. Backend creates a processing job.
9. Redis queues the job.
10. Worker extracts and processes the document.
11. Worker generates structured screenplay data.
12. Results are validated.
13. Results are stored in PostgreSQL.
14. Frontend retrieves processing status.
15. User views the results.

AI-based analysis is triggered separately when required.

---

# PART 4 — FOLDER STRUCTURE

## 4.1 Root Directory

```text
script-scrapper/
│
├── frontend/
│
├── backend/
│
├── storage/
│
├── infrastructure/
│
├── documentation/
│
├── scripts/
│
├── tests/
│
├── docker-compose.yml
│
├── .env.example
│
├── .gitignore
│
└── README.md
```

## 4.2 Frontend Structure

```text
frontend/
│
├── app/
│   ├── login/
│   ├── dashboard/
│   ├── projects/
│   ├── scripts/
│   ├── analysis/
│   ├── settings/
│   ├── layout.tsx
│   └── page.tsx
│
├── components/
│   ├── ui/
│   ├── layout/
│   ├── navigation/
│   └── shared/
│
├── features/
│   ├── authentication/
│   ├── projects/
│   ├── scripts/
│   ├── uploads/
│   ├── processing/
│   └── analysis/
│
├── services/
│   ├── api-client.ts
│   ├── auth.service.ts
│   ├── project.service.ts
│   └── script.service.ts
│
├── hooks/
├── stores/
├── types/
├── schemas/
├── utils/
│
└── tests/
```

### Frontend boundaries

- app/: Routing and page composition.
- components/: Reusable UI components.
- features/: Feature-specific functionality.
- services/: API communication.
- hooks/: Reusable React hooks.
- stores/: Client-side state.
- schemas/: Frontend validation.
- types/: Shared frontend types.

Do not place backend business logic in frontend feature modules.

## 4.3 Backend Structure

```text
backend/
│
├── app/
│
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── projects.py
│   │       ├── scripts.py
│   │       ├── uploads.py
│   │       ├── processing.py
│   │       └── analysis.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── exceptions.py
│   │   ├── logging.py
│   │   └── dependencies.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── base.py
│   │   └── session.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── script.py
│   │   ├── script_version.py
│   │   ├── processing_job.py
│   │   ├── scene.py
│   │   ├── character.py
│   │   ├── dialogue.py
│   │   └── analysis.py
│   │
│   ├── schemas/
│   │
│   ├── repositories/
│   │
│   ├── modules/
│   │
│   ├── services/
│   │
│   ├── processing/
│   │   ├── adapters/
│   │   │   ├── pdf_adapter.py
│   │   │   ├── docx_adapter.py
│   │   │   ├── txt_adapter.py
│   │   │   └── fountain_adapter.py
│   │   │
│   │   ├── extraction/
│   │   ├── normalization/
│   │   ├── screenplay_parser/
│   │   └── validation/
│   │
│   ├── ai/
│   │   ├── providers/
│   │   ├── prompts/
│   │   ├── services/
│   │   └── validators/
│   │
│   ├── workers/
│   │   ├── queue.py
│   │   └── tasks/
│   │
│   └── main.py
│
├── migrations/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│
└── requirements/
```

This structure is the architectural target. Developers may refine file placement when implementation evidence supports a better arrangement, but module boundaries must remain intact.

---

# PART 5 — MODULE BOUNDARIES AND RESPONSIBILITIES

## 5.1 Authentication Module

Responsibilities:

- Login.
- Logout.
- Password management.
- Session management.
- User status.
- Permission verification.

Must not handle project or screenplay business logic.

## 5.2 User Management Module

Responsibilities:

- User creation.
- User updates.
- User activation and deactivation.
- Role assignment.
- Account management.

Public registration is excluded initially.

## 5.3 Project Management Module

Responsibilities:

- Create projects.
- Update projects.
- Archive projects.
- Retrieve projects.
- Assign ownership.
- Enforce project access.

## 5.4 Script Management Module

Responsibilities:

- Register screenplay documents.
- Manage script metadata.
- Maintain versions.
- Track original documents.
- Track processing status.
- Maintain relationships with projects.

## 5.5 Document Processing Module

Responsibilities:

- File validation.
- File type detection.
- Extraction.
- Normalization.
- Parsing.
- Structural validation.
- Error reporting.

This module must remain independent of the AI module.

## 5.6 Screenplay Parser Module

Responsibilities:

- Scene identification.
- Scene heading identification.
- Character identification.
- Dialogue identification.
- Parenthetical identification.
- Action identification.
- Structural relationships.
- Parsing confidence and warnings.

The actual parsing rules must be documented separately and validated against representative screenplay samples.

## 5.7 AI Module

Responsibilities:

- AI provider communication.
- Prompt management.
- Context preparation.
- AI request handling.
- Response validation.
- Usage tracking.
- Error handling.

The AI module must not directly modify original screenplay documents.

## 5.8 Analysis Module

Responsibilities:

- Coordinate analysis workflows.
- Combine deterministic and AI-generated results.
- Store analysis runs.
- Track analysis versions.
- Maintain references to source scenes and dialogue.
- Display analysis provenance.

## 5.9 Background Processing Module

Responsibilities:

- Job creation.
- Job scheduling.
- Job execution.
- Job status.
- Retry handling.
- Failure handling.
- Processing history.

---

# PART 6 — DATABASE ARCHITECTURE

## 6.1 Database Design Principles

1. PostgreSQL is the primary database.
2. Every major entity has a primary key.
3. Foreign keys must be enforced.
4. Database migrations must be version-controlled.
5. Project ownership must be enforced.
6. Original document metadata must be retained.
7. Processing results must be traceable.
8. AI results must retain provenance.
9. Large original files must not be stored as database blobs.
10. Database records must not be deleted through uncontrolled cascading operations.

Use UUID primary keys for major application entities.

## 6.2 Proposed Entity Structure

### Users

```text
users
-----
id
username
email
password_hash
role
is_active
created_at
updated_at
```

Roles initially:

- Administrator.
- Standard User.

Additional roles require documented requirements.

### Projects

```text
projects
--------
id
name
description
owner_id
status
created_at
updated_at
```

Relationship:

One user can own multiple projects.

### Project Members

```text
project_members
---------------
id
project_id
user_id
permission_level
created_at
```

This table supports controlled project sharing.

### Scripts

```text
scripts
-------
id
project_id
title
description
current_version_id
status
created_by
created_at
updated_at
```

### Script Versions

```text
script_versions
---------------
id
script_id
version_number
original_filename
file_format
storage_path
file_size
file_hash
extracted_text_path
processing_status
created_by
created_at
```

Each upload creates an immutable version record.

### Processing Jobs

```text
processing_jobs
---------------
id
script_version_id
job_type
status
progress
attempt_count
error_code
error_message
started_at
completed_at
created_at
```

### Scenes

```text
scenes
------
id
script_version_id
scene_number
scene_heading
location
time_of_day
interior_exterior
start_position
end_position
created_at
```

### Characters

```text
characters
----------
id
script_version_id
canonical_name
first_appearance
created_at
```

### Character Aliases

```text
character_aliases
-----------------
id
character_id
alias
```

### Dialogue

```text
dialogue
--------
id
scene_id
character_id
dialogue_text
sequence_number
start_position
end_position
created_at
```

### Analysis Runs

```text
analysis_runs
-------------
id
script_version_id
analysis_type
provider
model
prompt_version
status
created_at
completed_at
```

### Analysis Results

```text
analysis_results
----------------
id
analysis_run_id
result_type
result_data
confidence
created_at
```

### Audit Logs

```text
audit_logs
----------
id
user_id
action
entity_type
entity_id
metadata
created_at
```

Do not store passwords, API keys, screenplay text or sensitive personal information in audit metadata.

## 6.3 Important Relationships

```text
USERS
  |
  +------ PROJECTS
              |
              +------ PROJECT_MEMBERS
              |
              +------ SCRIPTS
                         |
                         +------ SCRIPT_VERSIONS
                                      |
                                      +------ PROCESSING_JOBS
                                      |
                                      +------ SCENES
                                      |          |
                                      |          +------ DIALOGUE
                                      |
                                      +------ CHARACTERS
                                      |          |
                                      |          +------ CHARACTER_ALIASES
                                      |
                                      +------ ANALYSIS_RUNS
                                                  |
                                                  +------ ANALYSIS_RESULTS
```

## 6.4 Additional Database Requirements

- Unique constraint on project membership.
- Unique constraint on script version number within a script.
- Appropriate indexes on ownership and foreign keys.
- Indexes on processing status and creation timestamps.
- Indexes on script version and scene sequence.
- Database transactions for multi-record operations.
- JSONB only for genuinely variable analysis output.
- UTC timestamps throughout.

### Important architectural decision

Scene, character and dialogue records must be tied to a specific script version.

A new screenplay upload must not silently overwrite the previous parsed structure.

This provides traceability and prevents results from different screenplay versions being mixed.

---

# PART 7 — DOCUMENT PROCESSING ARCHITECTURE

## 7.1 Processing Pipeline

```text
UPLOAD
  |
  v
FILE VALIDATION
  |
  v
FORMAT DETECTION
  |
  v
FORMAT-SPECIFIC EXTRACTION
  |
  v
COMMON INTERMEDIATE REPRESENTATION
  |
  v
SCREENPLAY PARSING
  |
  v
STRUCTURAL VALIDATION
  |
  v
NORMALIZATION
  |
  v
PERSISTENCE
  |
  v
ANALYSIS
```

## 7.2 Format-Specific Requirements

### PDF

- Extract text.
- Preserve page information.
- Preserve text ordering where possible.
- Detect extraction failures.
- Identify image-based PDFs.
- Report when OCR is required.

OCR is a separately approved capability.

### DOCX

- Extract paragraphs.
- Preserve paragraph order.
- Extract relevant text from tables.
- Preserve useful structural information.
- Handle unsupported document features gracefully.

### TXT

- Detect supported encodings.
- Normalize line endings.
- Preserve original text.
- Handle malformed encoding safely.

### Fountain

- Parse Fountain syntax.
- Identify scene headings.
- Identify action.
- Identify character cues.
- Identify dialogue.
- Identify parentheticals.
- Preserve formatting markers where relevant.

## 7.3 Common Intermediate Representation

Every supported format must produce a common internal representation.

Example:

```json
{
  "document_id": "uuid",
  "source_format": "fountain",
  "title": "Example Screenplay",
  "elements": [
    {
      "type": "scene_heading",
      "text": "INT. OFFICE - DAY",
      "sequence": 1
    },
    {
      "type": "action",
      "text": "A man enters the room.",
      "sequence": 2
    },
    {
      "type": "character",
      "text": "JOHN",
      "sequence": 3
    },
    {
      "type": "dialogue",
      "text": "We need to talk.",
      "sequence": 4
    }
  ]
}
```

This is an illustrative schema, not the final validated parser specification.

The intermediate representation must preserve source references such as page numbers, offsets or source element identifiers whenever available.

## 7.4 Processing Quality Requirements

- Never silently discard extracted text.
- Record parsing warnings.
- Preserve original files.
- Record extraction failures.
- Separate extraction errors from parser errors.
- Make processing repeatable.
- Do not overwrite completed processing results without a new processing run.

---

# PART 8 — API CONTRACT SPECIFICATION

## 8.1 API Standards

Base path:

```text
/api/v1/
```

Use REST conventions.

All responses must follow consistent JSON structures.

## 8.2 Authentication APIs

| Method | Endpoint | Purpose |
| --- | --- | --- |
| POST | /api/v1/auth/login | Login |
| POST | /api/v1/auth/logout | Logout |
| GET | /api/v1/auth/me | Current user |
| POST | /api/v1/auth/change-password | Change password |

## 8.3 User APIs

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | /api/v1/users | List users |
| POST | /api/v1/users | Create user |
| GET | /api/v1/users/{id} | Retrieve user |
| PATCH | /api/v1/users/{id} | Update user |
| PATCH | /api/v1/users/{id}/status | Activate/deactivate |

Administrative permissions are mandatory for user management operations.

## 8.4 Project APIs

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | /api/v1/projects | List accessible projects |
| POST | /api/v1/projects | Create project |
| GET | /api/v1/projects/{id} | Retrieve project |
| PATCH | /api/v1/projects/{id} | Update project |
| DELETE | /api/v1/projects/{id} | Archive or delete according to policy |

## 8.5 Script APIs

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | /api/v1/projects/{id}/scripts | List scripts |
| POST | /api/v1/projects/{id}/scripts | Register script |
| GET | /api/v1/scripts/{id} | Retrieve script |
| PATCH | /api/v1/scripts/{id} | Update metadata |
| GET | /api/v1/scripts/{id}/versions | List versions |
| GET | /api/v1/scripts/{id}/versions/{version_id} | Retrieve version |

## 8.6 Upload APIs

| Method | Endpoint | Purpose |
| --- | --- | --- |
| POST | /api/v1/scripts/{id}/upload | Upload screenplay |
| GET | /api/v1/uploads/{id}/status | Retrieve upload status |

Supported extensions:

- .pdf
- .docx
- .txt
- .fountain

MIME type and actual file content must also be validated.

## 8.7 Processing APIs

| Method | Endpoint | Purpose |
| --- | --- | --- |
| POST | /api/v1/processing/{version_id}/start | Start processing |
| GET | /api/v1/processing/{job_id} | Retrieve job |
| GET | /api/v1/processing/{job_id}/status | Retrieve status |
| POST | /api/v1/processing/{job_id}/retry | Retry eligible failed job |

## 8.8 Analysis APIs

| Method | Endpoint | Purpose |
| --- | --- | --- |
| POST | /api/v1/analysis/{version_id}/start | Start analysis |
| GET | /api/v1/analysis/{id} | Retrieve analysis |
| GET | /api/v1/analysis/{id}/results | Retrieve results |
| GET | /api/v1/scripts/{id}/analysis | List analysis runs |

## 8.9 Standard API Response

Successful response:

```json
{
  "success": true,
  "data": {},
  "message": "Operation completed successfully"
}
```

Error response:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_FILE_FORMAT",
    "message": "The uploaded file format is not supported"
  }
}
```

Paginated responses must include pagination metadata.

## 8.10 API Rules

- Use appropriate HTTP status codes.
- Validate request bodies.
- Validate path parameters.
- Enforce authorization at the backend.
- Never trust frontend-supplied ownership identifiers.
- Use consistent error codes.
- Document endpoints through OpenAPI.
- Avoid exposing internal filesystem paths.
- Avoid exposing stack traces.
- Use idempotency protection where duplicate processing could create incorrect results.

The OpenAPI specification is the source of truth for frontend/backend integration contracts.

---

# PART 9 — SECURITY ARCHITECTURE

Security is mandatory even though this is a locally hosted application.

## 9.1 Authentication

Recommended:

- Password hashing with Argon2id.
- Secure session management.
- HTTP-only cookies.
- Secure cookie attributes.
- Session expiration.
- Login rate limiting.
- Password change capability.

Do not store plaintext passwords.

## 9.2 Authorization

Initial roles:

Administrator:

- Manage users.
- Manage projects.
- Access authorized administrative functions.
- View system status.

Standard User:

- Create or access authorized projects.
- Upload scripts.
- Process documents.
- View permitted results.

Every request involving a project or screenplay must verify access on the backend.

## 9.3 File Security

- Allow only approved file formats.
- Validate file signatures.
- Do not trust filenames or extensions.
- Generate internal storage filenames.
- Restrict upload size.
- Prevent path traversal.
- Reject malformed files.
- Prevent arbitrary file execution.
- Store uploaded files outside publicly served directories.
- Apply retention and deletion policies.

PDF and DOCX files must be treated as untrusted input.

## 9.4 Local Network Security

Default configuration:

- Bind application services to localhost.
- Expose only the reverse proxy when LAN access is enabled.
- Restrict LAN access through firewall rules.
- Do not expose PostgreSQL or Redis ports to the LAN.
- Require authentication for remote-device access.
- Do not expose the application directly to the public internet.

Optional LAN access must be explicitly enabled by the administrator.

HTTPS should be used for LAN access, with a managed local certificate strategy.

## 9.5 AI Security

- API keys remain server-side.
- Do not expose keys to frontend JavaScript.
- Do not include secrets in logs.
- Apply request timeouts.
- Apply usage limits.
- Validate AI outputs.
- Treat AI responses as untrusted input.
- Maintain prompt versions.
- Record provider and model information.

### Screenplay confidentiality

Before external AI submission, establish:

1. What screenplay content is transmitted.
2. Which AI provider receives it.
3. Whether the provider retains submitted data.
4. Whether submitted data may be used for model training.
5. Whether data is transmitted over encrypted connections.
6. Whether the user has authorized external processing.

The system should support an explicit policy controlling which analysis operations may transmit screenplay content externally.

## 9.6 Backup Security

- Backups must not be publicly accessible.
- Sensitive configuration must be protected.
- Backup storage should be separate from primary application storage.
- Restoration must be tested.
- Encryption should be used for backups containing confidential screenplay data.

---

# PART 10 — STORAGE ARCHITECTURE

Recommended structure:

```text
storage/
│
├── originals/
│   └── project_id/
│       └── script_id/
│           └── version_id/
│
├── extracted/
│
├── processing/
│
├── exports/
│
├── backups/
│
└── temporary/
```

Important rules:

- Original files are immutable.
- Extracted text is stored separately.
- Temporary files must be cleaned up.
- File references must be stored in PostgreSQL.
- Files must not be served directly from unrestricted public directories.
- Backups must not be treated as ordinary application files.

The application must handle missing files and database/file-storage inconsistencies safely.

---

# PART 11 — DEPLOYMENT ARCHITECTURE

## 11.1 Initial Deployment

The application runs on one computer.

Preferred operating system: Ubuntu LTS.

Windows compatibility can be evaluated during the environment setup stage.

Docker Compose will manage:

1. Frontend.
2. Backend.
3. PostgreSQL.
4. Redis.
5. Worker.
6. Reverse proxy.

## 11.2 Access Modes

Primary access:

```text
http://localhost
```

Optional LAN access:

```text
http://LOCAL-MACHINE-IP
```

Production LAN access should use an appropriately configured HTTPS endpoint.

## 11.3 Startup Requirements

The final installation should provide:

- One-command startup.
- One-command shutdown.
- Health checks.
- Automatic service restart where appropriate.
- Persistent database volumes.
- Persistent document storage.
- Backup and restoration commands.

The application must not lose data when containers restart.

## 11.4 Internet Dependency

Core local application functions should remain available without internet connectivity where technically possible.

External AI analysis requires internet connectivity.

The system must clearly communicate when an external provider is unavailable.

---

# PART 12 — PERFORMANCE REQUIREMENTS

Initial engineering targets:

| Metric | Target |
| --- | --- |
| Frontend LCP | Target ≤ 2.5 seconds on representative hardware |
| Ordinary API operations | Target ≤ 300 ms for common operations |
| Document upload | No unnecessary memory buffering |
| Large screenplay processing | Background execution |
| Database access | Appropriate indexing |
| Frontend rendering | Avoid unnecessary re-renders |
| Worker execution | Controlled concurrency |
| Memory usage | Monitored under realistic workload |

These targets must be measured.

They are not claims of existing performance.

## 12.1 Optimization Rules

- Avoid unnecessary dependencies.
- Avoid loading entire large files into memory when streaming is practical.
- Avoid duplicate document extraction.
- Cache only when justified.
- Paginate large result sets.
- Use database indexes based on actual query patterns.
- Keep worker concurrency configurable.
- Profile before optimizing.

---

# PART 13 — TESTING ARCHITECTURE

## 13.1 Backend Testing

Use Pytest.

Test categories:

1. Unit tests.
2. Integration tests.
3. API tests.
4. Database tests.
5. Processing tests.
6. Security tests.
7. Failure recovery tests.

## 13.2 Frontend Testing

Use:

- Vitest.
- React Testing Library.
- Playwright.

Test categories:

- Component behavior.
- Form validation.
- API interaction.
- Authentication.
- Navigation.
- Error handling.
- Complete user workflows.

## 13.3 Document Processing Testing

This is a critical quality area.

Create a controlled screenplay test corpus.

Include:

- PDF with selectable text.
- PDF with unusual formatting.
- Scanned PDF for OCR capability evaluation.
- DOCX with screenplay-style paragraphs.
- DOCX containing tables.
- TXT with different encodings.
- Fountain with standard screenplay elements.
- Fountain with edge cases.
- Malformed documents.
- Large documents.

Expected outputs must be manually validated.

A successful extraction test does not automatically mean screenplay parsing is correct.

## 13.4 AI Testing

Test:

- Valid responses.
- Malformed responses.
- API timeouts.
- Provider failures.
- Token limit errors.
- Invalid model output.
- Retry behavior.
- Usage tracking.
- Prompt versioning.

AI-generated results must be evaluated against documented quality criteria.

---

# PART 14 — DEVELOPMENT PROTOCOLS

## 14.1 Development Environment

Every developer must use:

- Approved Git repository.
- Approved branch strategy.
- Approved dependency versions.
- Approved environment configuration.
- Approved folder structure.
- Approved coding conventions.

No developer should independently introduce major infrastructure or framework changes.

## 14.2 Git Strategy

```text
main
  |
develop
  |
  +-- feature/authentication
  |
  +-- feature/projects
  |
  +-- feature/document-upload
  |
  +-- feature/document-processing
  |
  +-- feature/screenplay-parser
  |
  +-- feature/ai-integration
  |
  +-- feature/analysis
```

Rules:

- No direct commits to main.
- Feature branches must be reviewed.
- Commit messages must describe actual changes.
- Database migrations must accompany schema changes.
- Secrets must never be committed.
- Pull requests must include test evidence.

## 14.3 Antigravity Development Protocol

Antigravity is the primary implementation environment.

Every task must follow this sequence:

### STEP 1 — Repository Inspection

Before making changes, Antigravity must inspect:

- Existing folder structure.
- Existing dependencies.
- Current implementation.
- Related modules.
- Existing tests.
- Configuration.

It must not assume that files or functionality do not already exist.

### STEP 2 — Implementation Planning

Produce:

- Requirement reference.
- Files to be created.
- Files to be modified.
- Dependencies.
- Implementation steps.
- Expected behavior.
- Test plan.
- Potential risks.

### STEP 3 — Architecture Compliance

Verify the proposed implementation against this baseline.

Any architectural conflict must be reported before implementation.

### STEP 4 — Implementation

Implement only the approved scope.

Avoid unrelated refactoring.

### STEP 5 — Testing

Run relevant tests.

Do not claim tests passed unless they were actually executed.

### STEP 6 — Evidence Collection

Provide:

- Changed file list.
- Test commands.
- Test results.
- API responses.
- Database verification.
- Screenshots when relevant.
- Known limitations.
- Outstanding issues.

### STEP 7 — Independent Audit

ChatGPT reviews:

- Requirement compliance.
- Architecture compliance.
- Code quality.
- Security.
- Test evidence.
- Potential regressions.

### STEP 8 — Acceptance

The System Architect decides whether the module is:

- Accepted.
- Accepted with documented limitations.
- Rejected for correction.

---

# PART 15 — FIVE-MEMBER TEAM RESPONSIBILITIES

## Member 1 — System Architect

Primary responsibility:

- Architecture.
- Technical governance.
- Integration.
- Database design approval.
- API contract approval.
- Code review.
- Release authorization.

## Member 2 — Frontend Developer

Primary responsibility:

- Next.js application.
- UI components.
- Dashboard.
- Project management interface.
- Script upload interface.
- Processing interface.
- Analysis results interface.

## Member 3 — Backend Developer

Primary responsibility:

- FastAPI.
- Authentication.
- User management.
- Project APIs.
- Database integration.
- API contracts.
- Security implementation.

## Member 4 — Processing Engineer

Primary responsibility:

- PDF extraction.
- DOCX extraction.
- TXT processing.
- Fountain parsing.
- Common intermediate representation.
- Screenplay parser.
- Processing worker.

## Member 5 — QA / Full-stack Developer

Primary responsibility:

- Test architecture.
- Automated testing.
- Integration testing.
- Regression testing.
- Performance testing.
- Defect tracking.
- Evidence collection.

QA must have the authority to reject implementations that do not satisfy acceptance criteria.

---

# PART 16 — DEVELOPMENT MILESTONES AND APPROVAL GATES

## GATE 0 — Architecture Approval

Deliverables:

- Approved SRS.
- Approved architecture.
- Approved technology stack.
- Approved module boundaries.

No production implementation before this gate.

## GATE 1 — Foundation

Deliverables:

- Repository.
- Frontend foundation.
- Backend foundation.
- Database connection.
- Docker Compose.
- Health checks.

Acceptance:

All services start successfully and communicate correctly.

## GATE 2 — Authentication and Projects

Deliverables:

- Login.
- User management.
- Project creation.
- Project access control.

Acceptance:

Unauthorized users cannot access protected resources.

## GATE 3 — Document Processing

Deliverables:

- Upload.
- File validation.
- PDF extraction.
- DOCX extraction.
- TXT extraction.
- Fountain parsing.

Acceptance:

Representative documents produce validated extraction outputs.

## GATE 4 — Screenplay Parsing

Deliverables:

- Scene identification.
- Character identification.
- Dialogue extraction.
- Structured representation.
- Validation reports.

Acceptance:

Results meet the agreed parsing accuracy criteria.

## GATE 5 — AI Integration

Deliverables:

- Provider abstraction.
- API integration.
- Prompt management.
- Output validation.
- Error handling.

Acceptance:

Successful and failed AI requests are handled correctly.

## GATE 6 — Analysis Interface

Deliverables:

- Results retrieval.
- Analysis presentation.
- Processing status.
- Error states.

Acceptance:

Users can complete the approved screenplay-processing workflow.

## GATE 7 — Production Readiness

Deliverables:

- Security testing.
- Performance testing.
- Backup and restoration.
- Installation documentation.
- User documentation.
- Final audit.

Acceptance:

All critical and high-severity defects are resolved or explicitly approved with documented mitigation.

---

# PART 17 — ARCHITECTURE DECISION RECORDS

The following decisions form the initial ADR register.

| ADR | Decision | Status |
| --- | --- | --- |
| ADR-001 | Next.js frontend | Proposed |
| ADR-002 | FastAPI backend | Proposed |
| ADR-003 | PostgreSQL database | Proposed |
| ADR-004 | Modular monolith | Proposed |
| ADR-005 | Separate background worker | Proposed |
| ADR-006 | Redis + RQ | Proposed |
| ADR-007 | Local filesystem storage | Proposed |
| ADR-008 | External AI provider abstraction | Proposed |
| ADR-009 | Local standalone deployment | Confirmed |
| ADR-010 | Optional LAN access | Confirmed |
| ADR-011 | Four document formats | Confirmed |
| ADR-012 | No initial SaaS infrastructure | Confirmed |

An ADR must contain:

- Decision ID.
- Context.
- Problem.
- Options considered.
- Selected approach.
- Reasoning.
- Consequences.
- Approval.
- Date.

Changes to approved ADRs require documented review.

---

# PART 18 — NON-NEGOTIABLE ENGINEERING RULES

1. No unauthorized technology changes.
2. No unnecessary dependencies.
3. No duplicate business logic.
4. No business logic inside API route handlers.
5. No frontend-only security enforcement.
6. No hardcoded secrets.
7. No direct database access from frontend.
8. No uncontrolled file-system access.
9. No synchronous processing of large documents inside ordinary HTTP requests.
10. No overwriting original screenplay versions.
11. No mixing AI output with deterministic results without provenance.
12. No undocumented database changes.
13. No merging untested features into the main branch.
14. No accepting work based solely on developer claims.
15. No release without documented testing and backup verification.

---

# PART 19 — ITEMS REQUIRING TECHNICAL VALIDATION

The following must not be treated as finalized simply because they appear in this architecture document.

| Item | Required action |
| --- | --- |
| PDF OCR | Determine whether it belongs in the first release |
| Fountain parser library | Conduct compatibility evaluation |
| Maximum upload size | Establish from actual screenplay requirements |
| Maximum concurrent processing jobs | Benchmark |
| AI provider | Select based on quality, privacy and cost |
| AI model | Evaluate against representative screenplay tasks |
| Screenplay parser accuracy | Establish measurable acceptance criteria |
| Windows support | Validate if required |
| Local HTTPS | Select certificate strategy |
| Backup retention | Agree on retention policy |
| Hardware | Validate against representative workload |

These are open engineering decisions, not reasons to delay foundational implementation.

---

# PART 20 — DEFINITION OF DONE

A module is considered complete only when:

1. Its requirements are documented.
2. Its implementation follows approved architecture.
3. Its interfaces are documented.
4. Its validation is implemented.
5. Its unit tests pass.
6. Its integration tests pass where applicable.
7. Its security implications are reviewed.
8. Its error handling is implemented.
9. Its documentation is updated.
10. Its evidence is submitted.
11. Its integration is verified.
12. Its acceptance is recorded.

A successful code generation operation does not constitute module completion.

---

# FINAL ARCHITECTURAL DECLARATION

The initial Script Scrapper architecture is defined as:

**Product:** Script Scrapper  
**Architecture:** Modular Monolith  
**Frontend:** Next.js + TypeScript  
**Backend:** Python + FastAPI  
**Database:** PostgreSQL  
**Background Processing:** Redis + RQ  
**Document Processing:** Format-specific extraction adapters and a common screenplay representation  
**AI:** External APIs through a provider abstraction  
**Storage:** Local filesystem  
**Deployment:** Standalone local computer  
**Optional Access:** Local network  
**Containerization:** Docker Compose  
**Development Environment:** Antigravity  
**Development Governance:** System Architect + ChatGPT + Antigravity  
**Initial Product Model:** Non-SaaS

This baseline is the proposed technical reference for all initial implementation activities.

Any deviation must be documented through an Architecture Decision Record and approved by the System Architect.

**END OF ARCHITECTURE BASELINE v1.0**
