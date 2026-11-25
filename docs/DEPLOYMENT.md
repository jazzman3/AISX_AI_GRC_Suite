# AISX AI GRC Suite — Deployment, Demo Operations, and Enterprise Hardening

**Release:** 1.0 reference/demo | **Date:** November 24, 2026  
**Scope:** Five self-contained FastAPI services. The same shared app code runs with one of five MODULE configurations.  
**Verification:** 20 API tests passed. Docker runtime and browser-to-localhost deployment were unavailable in the build environment. Dashboard PNGs are rendered from actual HTML with fixture responses, not live deployment captures.

## 1. Requirements
- Windows 11 with WSL2 and Docker Desktop, or macOS/Linux with Docker Engine + Compose v2
- At least 4 GB available RAM and 2 GB disk for images and persistent data (planning allowances; not a measured requirement)
- Ports 8201 through 8205 unoccupied
- Python 3.12+ only if running unit tests without Docker
- Do not use real sensitive data in this reference version

## 2. Install and configure
1. Download and unzip `AISX_AI_GRC_Five_Applications.zip`.
2. Open a terminal in `AISX_AI_GRC_Suite` (folder with `compose.yaml`).
3. Windows PowerShell: `Copy-Item .env.example .env`. macOS/Linux: `cp .env.example .env`.
4. Edit `.env`. Change `ADMIN_PASSWORD` to a unique randomly generated value of at least 24 characters (do not commit `.env`). Keep `ADMIN_USER=aisx-admin` or change it.
5. Keep `SEED_DEMO=1` for synthetic records. Use `0` for a clean new environment.
6. Confirm installation: `docker version` and `docker compose version`.
7. Inspect config: `docker compose config`. Ensure that only `127.0.0.1` binds ports.
8. Start: `docker compose up --build -d`.
9. Check: `docker compose ps` and `docker compose logs --tail 80`.
10. Verify health: `curl http://127.0.0.1:8201/health` (or `Invoke-RestMethod http://127.0.0.1:8201/health` in PowerShell). Repeat ports 8202–8205.
11. Visit each browser URL, enter `.env` credentials when prompted, confirm dashboard statistics and registers load.

## 3. Application URLs and functionality
| URL | Application | Demonstration |
|---|---|---|
| http://127.0.0.1:8201 | AI Asset Inventory | Create an AI use case, assign an owner, set data classification and review status |
| http://127.0.0.1:8202 | Risk Assessments | Score security/privacy/fairness/oversight factors 1–5, inspect calculated risk band |
| http://127.0.0.1:8203 | Compliance Evidence | Track framework, control owner, evidence reference, status and due date |
| http://127.0.0.1:8204 | Third-Party AI Risk | Register AI vendor, type of shared data, security review and contract status |
| http://127.0.0.1:8205 | Continuous Monitoring | Register a signal/incident, severity, owner, source and investigation status |

All five expose `GET /api/summary`, `GET/POST /api/records`, `PATCH /api/records/{id}`, `GET /api/audit`, and `GET /api/export.csv`. HTTP Basic credentials are required except `/health`.

### 3.1 Asset Inventory
1. Open port 8201.
2. Review 3 example AI systems (all synthetic).
3. In Add a record, enter a system name, owner, provider, intended usage, data class and status.
4. Save; the register and top-line counts update.
5. Export CSV to demonstrate an inventory for a governance review.
**Limitation:** assets are entered manually; there is no automatic discovery, CMDB synchronization or service graph.

### 3.2 AI Risk & Impact Assessments
1. Open port 8202 and review synthetic assessment rows.
2. Enter a system, owner, and four integer risk factors from 1–5.
3. Save; calculated score is `average(factors) × 20`, with high >=70, medium >=45, low below 45.
4. Explain the illustrative calculation and why legal/ethical risk tiers must be independently calibrated.
**Limitation:** this does not constitute a DPIA, algorithmic impact assessment, external audit or legally valid EU AI Act high-risk classification.

### 3.3 Compliance & Audit Evidence
1. Open port 8203; inspect seeded example controls for NIST AI RMF, ISO/IEC 42001 and EU AI Act.
2. Enter a control, framework, owner, evidence **reference** (not a sensitive attachment), status, and due date.
3. Export the controls CSV, then review gaps.
**Limitation:** evidence_uri is plain text; there is no secure file upload, automated mapping, legal obligation engine or evidence verification. Framework references are illustrative, not authoritative mappings.

### 3.4 Third-Party AI Vendor Risk
1. Open port 8204; inspect the pending reviews.
2. Register a synthetic vendor, product, owner, shared data class, security review and contract status.
3. Discuss gaps: contract controls, data retention, subprocessors and independent assurance evidence.
**Limitation:** no external vendor questionnaires, fourth-party discovery, vendor API integrations, contract parsing or automatic financial-risk assessment.

### 3.5 Continuous AI Risk Monitoring
1. Open port 8205, inspect risk events.
2. Register a signal with severity, owner, status and originating source.
3. Show high/critical event count, open investigations and CSV export.
**Limitation:** manual events only; there is no live event ingestion, anomaly detection, scheduled alerting, SIEM integration or on-call notification.

## 4. Verify APIs and data persistence
- `curl -u aisx-admin:YOUR_PASSWORD http://127.0.0.1:8201/api/summary` (avoid storing real passwords in shell history; use environment variables or interactive prompts).
- In PowerShell, browse to the web dashboard instead of embedding passwords in terminal commands.
- Create a synthetic record; then `docker compose restart inventory`; confirm it persists.
- Export CSV and confirm headers and values. Check `GET /api/audit` for write event.
- Run tests without Docker: `python -m pip install -r shared/requirements.txt pytest httpx` then `python -m pytest tests -q`.
- Verify bad credentials receive HTTP 401. Verify incomplete records receive 422 and missing IDs return 404.

## 5. Operational commands
```
docker compose ps
docker compose logs -f --tail 100
docker compose restart inventory
docker compose down
# WARNING: permanently destroys all five persistent data volumes:
docker compose down -v
```

## 6. Backup and restore
SQLite files are stored in five named Docker volumes. **Do not copy database files while writes are active** unless using SQLite online backup APIs. For a simple consistent demo backup:
1. Stop writes and `docker compose stop`.
2. Back up each Docker volume using an approved backup utility; retain access controls and test restoration on an isolated environment.
3. Start `docker compose up -d`.
For production replace this pattern with managed PostgreSQL, encrypted backups, tested PITR and restore drills.

## 7. Safe remote demonstration
Default host binding is 127.0.0.1. Do **not** change it to 0.0.0.0 to expose Basic auth over unencrypted HTTP. Preferred: screen-share a local demo or connect through a company-managed zero-trust tunnel that provides HTTPS, SSO/MFA and access restrictions. Never use this reference suite with actual regulated customer data.

## 8. Enterprise production upgrade gates
1. Identity: company SSO (OIDC/SAML), mandatory MFA, service accounts, session timeout, and per-role authorization.
2. Tenancy: hardened tenant scoping on every query, database row-level policies, tenant isolation tests.
3. Data: migrate SQLite to PostgreSQL; managed TLS, encryption at rest, migrations, backup and restore drills.
4. Audit: append-only/tamper-evident records shipped externally to WORM or SIEM; retention policies and admin monitoring.
5. Controls: authoritative, versioned NIST/ISO/EU legal mappings reviewed by counsel and control owners; evidence access restrictions.
6. Workflow: immutable assessment versions, multi-step approvals, exceptions, findings, action plans and ownership.
7. Integrations: AI platform discovery, cloud inventory, security scanners, risk signals, procurement/vendor datasets, ticketing and compliance evidence connectors.
8. Performance: worker queues, background jobs, idempotency, rate limits, connection pooling, load tests and SLOs.
9. Security: HTTPS at ingress, CSRF protection for cookie sessions, CSP without inline scripts, secure secrets management, input/output encoding, security scanning and penetration testing.
10. AI features: human-supervised LLM evidence summarization and vendor questionnaire extraction with citations and evaluation sets, where justified. This version contains **no AI model inference**.
11. Lifecycle: CI/CD, dependency updates, SBOM, vulnerability triage, signed containers, infrastructure as code, monitored staging and rollback.
12. Acceptance: audit a real end-to-end workflow with synthetic first, then masked client data after signed agreements and approvals; independent security test prior to use with sensitive records.

## 9. Common troubleshooting
- `docker: command not found` -> install Docker and restart shell.
- Port already allocated -> change host port in `compose.yaml`, not the container port 8000.
- App shows 503 -> ADMIN_PASSWORD absent/short; set at least 12 chars, preferably 24+.
- Authentication prompt repeats -> check exact credentials in `.env` and rebuild/recreate containers: `docker compose up -d --force-recreate`.
- No sample rows -> `SEED_DEMO=0` or database volume already initialized empty.
- DB permission error -> confirm volume mounted at `/data` and container UID can write; avoid mounting host directory without ownership alignment.
- Browser screenshot doesn't match -> bundled PNGs are rendered fixture previews, not live-server captures.

## 10. Suggested client demo agenda (10–12 minutes)
1. 60s: explain the AI governance problem and system-of-record opportunity.
2. 2 min: register a new AI agent in Inventory.
3. 2 min: complete the risk factor questionnaire; explain scoring limitations.
4. 2 min: associate compliance controls and evidence references.
5. 2 min: register a third-party AI supplier and identify pending review.
6. 2 min: triage a synthetic monitoring signal and export audit CSV.
7. 60s: discuss deployment roadmap, real integrations and validation.

## 11. Technical inventory
- FastAPI, SQLite, Python 3.12, Uvicorn, HTML/CSS/JavaScript
- Docker Compose five services, one shared source directory and separate persisted volumes
- HTTP Basic auth (demo only), security headers, validation, audit event table
- No third-party external account/paid model required

## References (for planning, not certification)
- NIST AI RMF Playbook: https://airc.nist.gov/airmf-resources/playbook/
- European Commission AI Act overview: https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai
- EU AI Act official timeline: https://ai-act-service-desk.ec.europa.eu/en/ai-act/timeline/timeline-implementation-eu-ai-act
- Gartner 2026 AI governance market forecast: https://www.gartner.com/en/newsroom/press-releases/2026-02-17-gartner-global-ai-regulations-fuel-billion-dollar-market-for-ai-governance-platforms
