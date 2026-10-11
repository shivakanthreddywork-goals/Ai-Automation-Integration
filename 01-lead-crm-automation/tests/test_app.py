from fastapi.testclient import TestClient
from app.main import app, score_lead

client = TestClient(app)

def test_health():
    assert client.get("/health").json()["status"] == "ok"

def test_score_is_bounded():
    score, priority = score_lead("urgent quote to implement automation this week")
    assert 0 <= score <= 100
    assert priority == "high"

def test_create_lead():
    response = client.post("/leads", json={
        "name": "Demo Person",
        "email": "demo@example.com",
        "company": "Example Co",
        "message": "We need a quote to automate our workflow this month.",
        "source": "test"
    })
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "demo@example.com"
    assert "review before sending" in body["follow_up_draft"].lower()
