import sqlite3
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Safe Analytics Demo")
DB = Path(__file__).parent / "sample_sales.db"

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY, product TEXT, region TEXT, quantity INTEGER,
            unit_price REAL, quarter TEXT
        )""")
        count = conn.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
        if count == 0:
            conn.executemany("INSERT INTO sales(product,region,quantity,unit_price,quarter) VALUES(?,?,?,?,?)", [
                ("Keyboard","South",20,1500.0,"Q1"),
                ("Mouse","South",50,500.0,"Q1"),
                ("Monitor","West",12,12000.0,"Q1"),
                ("Keyboard","West",15,1500.0,"Q2"),
                ("Monitor","South",8,12000.0,"Q2"),
                ("Mouse","North",40,500.0,"Q2")
            ])
init_db()

class QueryIn(BaseModel):
    question: str = Field(min_length=3, max_length=500)

def run_query(sql: str):
    # This demo only runs SQL constants defined in this source file.
    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        return [dict(row) for row in conn.execute(sql).fetchall()]
    finally:
        conn.close()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/query")
def query(payload: QueryIn):
    q = payload.question.lower()
    if "region" in q and ("revenue" in q or "sales" in q):
        intent = "revenue_by_region"
        sql = """SELECT region, ROUND(SUM(quantity * unit_price),2) AS revenue
                 FROM sales GROUP BY region ORDER BY revenue DESC LIMIT 100"""
    elif "quarter" in q and ("revenue" in q or "sales" in q):
        intent = "revenue_by_quarter"
        sql = """SELECT quarter, ROUND(SUM(quantity * unit_price),2) AS revenue
                 FROM sales GROUP BY quarter ORDER BY quarter LIMIT 100"""
    elif "product" in q or "highest revenue" in q:
        intent = "revenue_by_product"
        sql = """SELECT product, ROUND(SUM(quantity * unit_price),2) AS revenue
                 FROM sales GROUP BY product ORDER BY revenue DESC LIMIT 100"""
    else:
        return {"status": "needs_clarification",
                "message": "Supported questions: revenue by product, revenue by region, or revenue by quarter.",
                "rows": []}
    return {"status": "ok", "intent": intent, "rows": run_query(sql),
            "note": "Uses fixed, read-only SQL against synthetic sample data."}
