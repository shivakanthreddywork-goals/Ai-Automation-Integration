from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_retrieves_expense_policy():
    r = client.post("/ask", json={"question":"How many days to submit expense claims?"})
    assert r.status_code == 200
    assert any(s["document_id"] == "HR-001" for s in r.json()["sources"])

def test_unknown_question_returns_no_sources():
    r = client.post("/ask", json={"question":"What is the recipe for mango chutney?"})
    assert r.status_code == 200
    assert r.json()["sources"] == []
