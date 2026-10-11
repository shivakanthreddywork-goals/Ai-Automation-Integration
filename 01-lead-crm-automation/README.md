# Lead Intake & CRM Automation

A FastAPI demo that accepts leads, scores them with transparent rules, stores them in SQLite, and drafts a follow-up email. The LLM integration is intentionally provider-neutral: the default mode works without a paid API.

## Run
```bash
python -m venv .venv
# activate the environment
pip install -r requirements.txt
copy .env.example .env   # Windows; on macOS/Linux use cp
uvicorn app.main:app --reload
```
Visit `/docs`. Try `POST /leads` with the example JSON below.

```json
{
  "name": "Asha Rao",
  "email": "asha@example.com",
  "company": "Northwind Demo",
  "message": "We need to automate lead routing and follow-up for our sales team.",
  "source": "website"
}
```

## Features
- Input validation with Pydantic.
- Transparent rule-based score and priority.
- SQLite persistence.
- Draft-only follow-up message (no email is sent).
- Health endpoint and basic tests.

## Portfolio upgrades
Add an n8n webhook, CRM sandbox integration, authentication, duplicate detection, audit logs, tenant isolation, and human-approved email sending. Use OAuth/API credentials from environment variables; do not commit them.
