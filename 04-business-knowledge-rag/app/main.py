import json
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel, Field
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(title="Business Knowledge Retrieval Demo")
DOCS = json.loads((Path(__file__).parent / "documents.json").read_text(encoding="utf-8"))
CORPUS = [d["title"] + " " + d["text"] for d in DOCS]
VECTORIZER = TfidfVectorizer(stop_words="english")
MATRIX = VECTORIZER.fit_transform(CORPUS)

class AskIn(BaseModel):
    question: str = Field(min_length=3, max_length=1000)
    top_k: int = Field(default=2, ge=1, le=3)

@app.get("/health")
def health():
    return {"status": "ok", "documents_loaded": len(DOCS)}

@app.post("/ask")
def ask(payload: AskIn):
    query = VECTORIZER.transform([payload.question])
    scores = cosine_similarity(query, MATRIX)[0]
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:payload.top_k]
    matches = []
    for idx, score in ranked:
        if score > 0:
            doc = DOCS[idx]
            matches.append({
                "document_id": doc["id"],
                "title": doc["title"],
                "excerpt": doc["text"],
                "relevance_score": round(float(score), 4)
            })
    if matches:
        answer = "Retrieved excerpts (verify these against the approved source documents): " + " ".join(
            f"[{m['document_id']}] {m['excerpt']}" for m in matches
        )
    else:
        answer = "I could not find a relevant passage in the indexed sample documents."
    return {"question": payload.question, "answer": answer, "sources": matches,
            "method": "TF-IDF retrieval baseline; not an LLM-generated answer."}
