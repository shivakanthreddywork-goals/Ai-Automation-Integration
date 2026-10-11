# Safe Natural-Language Analytics Demo

A deliberately constrained analytics API. It maps a small set of recognized questions to predefined, read-only SQL queries against a local SQLite sample database. It does **not** execute arbitrary LLM-generated SQL.

## Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Try `POST /query` with:
```json
{"question":"Which products have the highest revenue?"}
```

## Upgrade path
Add schema discovery, SQL parsing/validation, database read-only credentials, query timeouts, row limits, audit logging, user permissions and an evaluation suite. If using an LLM to generate SQL, treat its output as untrusted input and validate it before execution.
