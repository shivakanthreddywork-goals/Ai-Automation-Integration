# AI Customer Support Draft Assistant

A demo support API that classifies a ticket, retrieves a relevant answer from a small knowledge base, and drafts a reply for human review. It does not send emails or access a real helpdesk.

## Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open `/docs`, then call `POST /tickets/analyze`.

Example:
```json
{"customer_name":"Ravi","message":"How long do I have to return an unused item?"}
```

## Upgrade path
Connect an approved helpdesk sandbox, use a proper retrieval system for larger knowledge bases, add authentication and PII redaction, evaluate groundedness, and require approval for refunds, account changes, or outbound replies.
