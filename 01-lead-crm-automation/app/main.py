import os
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field

load_dotenv()
DB_PATH = os.getenv("DATABASE_PATH", "./leads.db")
Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)

app = FastAPI(title=os.getenv("APP_NAME", "Lead Intake Automation"),
              description="Portfolio demo: lead intake, transparent scoring and follow-up drafts.")

class LeadIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    company: str = Field(default="Unknown", max_length=160)
    message: str = Field(min_length=5, max_length=5000)
    source: str = Field(default="manual", max_length=80)

class LeadOut(LeadIn):
    id: int
    score: int
    priority: str
    follow_up_draft: str
    created_at: str

def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with closing(connect()) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, email TEXT NOT NULL, company TEXT NOT NULL,
            message TEXT NOT NULL, source TEXT NOT NULL, score INTEGER NOT NULL,
            priority TEXT NOT NULL, follow_up_draft TEXT NOT NULL, created_at TEXT NOT NULL
        )
        """)
        conn.commit()

def score_lead(message: str) -> tuple[int, str]:
    """Explainable demo scoring. Replace with client-approved criteria."""
    text = message.lower()
    score = 20
    signals = {
        "timeline": ["this week", "urgent", "asap", "this month"],
        "budget": ["budget", "pricing", "quote", "cost"],
        "intent": ["implement", "automate", "integration", "proposal", "demo"],
    }
    for terms in signals.values():
        if any(term in text for term in terms):
            score += 25
    score = min(score, 95)
    priority = "high" if score >= 70 else "medium" if score >= 45 else "low"
    return score, priority

def draft_follow_up(lead: LeadIn, priority: str) -> str:
    return (
        f"Hi {lead.name},\n\n"
        f"Thanks for contacting us about: {lead.message[:240]}\n\n"
        "I'd be happy to learn more about your workflow and discuss a suitable approach. "
        "Would you be available for a short discovery call?\n\n"
        "Best,\nYour Team\n\n"
        f"[Internal note: demo priority = {priority}. Review before sending.]"
    )

init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/leads", response_model=LeadOut, status_code=201)
def create_lead(lead: LeadIn):
    score, priority = score_lead(lead.message)
    draft = draft_follow_up(lead, priority)
    created_at = datetime.now(timezone.utc).isoformat()
    with closing(connect()) as conn:
        cursor = conn.execute(
            """INSERT INTO leads (name,email,company,message,source,score,priority,follow_up_draft,created_at)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (lead.name, str(lead.email), lead.company, lead.message, lead.source,
             score, priority, draft, created_at)
        )
        conn.commit()
        lead_id = cursor.lastrowid
    return LeadOut(id=lead_id, **lead.model_dump(), score=score,
                   priority=priority, follow_up_draft=draft, created_at=created_at)

@app.get("/leads", response_model=list[LeadOut])
def list_leads(limit: int = 50):
    if not 1 <= limit <= 200:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 200")
    with closing(connect()) as conn:
        rows = conn.execute("SELECT * FROM leads ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    return [dict(row) for row in rows]

@app.get("/leads/{lead_id}", response_model=LeadOut)
def get_lead(lead_id: int):
    with closing(connect()) as conn:
        row = conn.execute("SELECT * FROM leads WHERE id = ?", (lead_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Lead not found")
    return dict(row)
