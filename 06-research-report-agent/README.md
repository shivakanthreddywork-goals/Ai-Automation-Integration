# Research & Reporting Assistant (Source-Traceable Demo)

This demo accepts a question and source notes supplied by the user, then generates a structured report draft that retains source IDs. It does not browse the web; it avoids invented sources and makes the user provide evidence.

## Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open `/docs` and call `POST /reports/draft`.

## Example
```json
{
  "research_question":"Compare the customer-support features of three demo products",
  "sources":[
    {"source_id":"S1","title":"Product A notes","url":"https://example.com/a","notes":"Offers email and chat support."},
    {"source_id":"S2","title":"Product B notes","url":"https://example.com/b","notes":"Offers chat support and a ticket dashboard."}
  ]
}
```

## Upgrade path
Connect approved search/data providers, store retrieved pages and timestamps, deduplicate sources, validate citations, label unsupported claims, and require a reviewer before publishing. The example URLs are placeholders and must not be represented as actual research.
