from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_returns_ticket():
    r = client.post("/tickets/analyze", json={"customer_name":"Ravi","message":"What is your return policy?"})
    assert r.status_code == 200
    assert r.json()["matched_topic"] == "returns"
    assert r.json()["status"] == "draft_ready"

def test_urgent_ticket_escalates():
    r = client.post("/tickets/analyze", json={"customer_name":"Mira","message":"I was charged twice, urgent!"})
    assert r.json()["status"] == "human_review_required"
