from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_product_query():
    r = client.post("/query", json={"question":"Which products have highest revenue?"})
    assert r.status_code == 200
    assert r.json()["intent"] == "revenue_by_product"
    assert len(r.json()["rows"]) > 0

def test_unsupported_query_does_not_run_sql():
    r = client.post("/query", json={"question":"Delete every sales record"})
    assert r.json()["status"] == "needs_clarification"
