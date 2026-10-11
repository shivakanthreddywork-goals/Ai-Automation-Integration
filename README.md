
# AI Automation Freelance Portfolio

Six portfolio-ready starter projects for AI automation and integration freelancing.

## Projects

1. `01-lead-crm-automation` — capture leads, classify them with an LLM-compatible interface, store them, and draft follow-up messages.
2. `02-ai-customer-support` — classify support tickets and draft grounded answers from a small knowledge base.
3. `03-document-processing` — extract and validate structured fields from sample invoices.
4. `04-business-knowledge-rag` — document ingestion and semantic retrieval with a simple local TF-IDF baseline.
5. `05-ai-data-analyst` — read-only natural-language analytics demo with safe, predefined queries.
6. `06-research-report-agent` — collect supplied source notes and generate a traceable report outline.

Each project is a starter implementation intended for learning and portfolio demonstration. It is not production-ready and does not include live integrations to a real CRM, email provider, accounting system, or web search provider.

## Quick start

Requirements: Python 3.11+ recommended.

For each project:
```bash
cd <project-folder>
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Windows users can copy `.env.example` to `.env` manually if `cp` is unavailable.

Open the API docs at `http://127.0.0.1:8000/docs`.

Some projects run entirely with sample data and deterministic fallback logic. To use an LLM, configure the relevant environment variables and implement/enable the provider adapter as described in each project's README. Never commit API keys or customer data.

## Suggested GitHub publishing approach

1. Review each project's README and run its tests.
2. Replace sample data with synthetic data of your own.
3. Add a short screen recording or screenshots.
4. Push the six folders as separate repositories, or push this entire folder as one portfolio repository.
5. Do not claim that demo integrations are production integrations.

## Responsible-use checklist

- Use synthetic/sample data in public repositories.
- Keep credentials in environment variables.
- Obtain permission before processing business/customer data.
- Require human approval before sending messages or taking consequential actions.
- Validate model output; never trust generated SQL or extracted fields without checks.
- Apply authentication, rate limits, logging, access controls and deployment hardening before real-world use.
