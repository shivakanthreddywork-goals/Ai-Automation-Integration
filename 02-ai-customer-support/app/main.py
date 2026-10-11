import json
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Customer Support Draft Assistant",
              description="Demo only: drafts answers from sample knowledge base; no message is sent.")
KB = json.loads((Path(__file__).parent / "knowledge_base.json").read_text(encoding="utf-8"))

class TicketIn(BaseModel):
    customer_name: str = Field(min_length=1, max_length=120)
    message: str = Field(min_length=3, max_length=5000)

def retrieve(message: str):
    text = message.lower()
    ranked = []
    for item in KB:
        score = sum(1 for keyword in item["keywords"] if keyword in text)
        if score:
            ranked.append((score, item))
    ranked.sort(key=lambda pair: pair[0], reverse=True)
    return ranked[0][1] if ranked else None

def classify(message: str):
    text = message.lower()
    urgent_terms = ["charged twice", "fraud", "locked out", "urgent", "complaint"]
    if any(term in text for term in urgent_terms):
        return "needs_human_review"
    if any(term in text for term in ["return", "refund", "exchange"]):
        return "returns"
    if any(term in text for term in ["shipping", "delivery", "tracking", "arrive"]):
        return "shipping"
    return "general"

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/tickets/analyze")
def analyze_ticket(ticket: TicketIn):
    category = classify(ticket.message)
    article = retrieve(ticket.message)
    if category == "needs_human_review":
        draft = ("Hi " + ticket.customer_name + ",\n\n"
                 "Thanks for letting us know. A support specialist should review this issue. "
                 "Please do not send passwords or one-time codes.\n\nSupport Team")
        status = "human_review_required"
    elif article:
        draft = (f"Hi {ticket.customer_name},\n\n{article['answer']}\n\n"
                 "If this doesn't resolve your question, reply and our team can help.\n\nSupport Team")
        status = "draft_ready"
    else:
        draft = (f"Hi {ticket.customer_name},\n\nThanks for contacting us. "
                 "We need a support specialist to review your question before providing an answer.\n\nSupport Team")
        status = "human_review_required"
    return {
        "ticket_category": category,
        "status": status,
        "matched_topic": article["topic"] if article else None,
        "draft_reply": draft,
        "source_note": "Uses local sample policies only. Verify against approved company documentation."
    }
