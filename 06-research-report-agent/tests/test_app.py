from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_report_keeps_source_ids():
    r = client.post("/reports/draft", json={
        "research_question":"Compare support features",
        "sources":[{"source_id":"S1","title":"Demo source","url":"https://example.com",
                    "notes":"Offers email support and a ticket dashboard."}]
    })
    assert r.status_code == 200
    assert "[S1]" in r.json()["draft_markdown"]
    assert r.json()["status"] == "draft_requires_human_verification"
