# AISX Enterprise AI GRC Suite

Five standalone, locally deployable AI governance, risk and compliance services with live dashboards, CRUD APIs, audit events, CSV exports, seeded synthetic examples, tests and Docker Compose.

## Quick start

```bash
cp .env.example .env
# Replace ADMIN_PASSWORD with a long random password. Keep .env out of source control.
docker compose up --build -d
docker compose ps
```

Open localhost dashboards at ports **8201** inventory, **8202** risk assessments, **8203** compliance, **8204** vendor risk, **8205** continuous monitoring. HTTP Basic authentication uses configured credentials. Keep all ports bound to localhost and use a secure tunnel for remote demos.

## Run tests

```bash
python -m pip install -r shared/requirements.txt pytest httpx
python -m pytest tests/ -q
```

## API usage

Authenticated endpoints per service: `GET /api/summary`, `GET/POST /api/records`, `PATCH /api/records/{id}`, `GET /api/audit`, `GET /api/export.csv`. Unauthenticated `GET /health`.

Example: `curl -u aisx-admin:YOUR_PASSWORD http://127.0.0.1:8201/api/summary`

## Deployment safety

This release is **a deployable, tested reference/demo system**, not enterprise production-ready. It does not automatically discover assets, monitor live models, collect audit evidence, or determine legal compliance. The EU AI Act mapping is a training/sample register, not a legal mapping. For enterprise production use replace HTTP Basic auth, implement SSO+MFA/RBAC, rate limiting, encrypted managed database, tenant isolation, background jobs, audit immutability, integrations, SIEM, tests and monitoring. See `docs/DEPLOYMENT.md`.

Synthetic demonstration records only. Never upload client secrets, PII, regulated data, or actual contract evidence to this reference deployment. No LLM calls are made; risk scores are deterministic illustrations.

