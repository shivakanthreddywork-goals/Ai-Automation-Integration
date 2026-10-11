# Business Knowledge Retrieval Assistant

A local demo for document Q&A retrieval. It uses TF-IDF ranking as a dependency-light baseline, not embeddings or a production vector database. This makes the retrieval pipeline easy to inspect and replace with embeddings/vector search later.

## Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open `/docs`; use `POST /ask`.

## Example
```json
{"question":"How many days do employees have to submit expenses?"}
```

## Upgrade path
Replace TF-IDF with an embedding model and vector store; add document-level permissions, ingestion/versioning, citations, retrieval evaluation, deletion workflows and a grounded answer-generation step. Do not index confidential documents without authorization.
