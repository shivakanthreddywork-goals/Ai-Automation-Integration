from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_valid_invoice():
    payload = {"supplier":"Example Supplies","invoice_number":"INV-1","currency":"INR",
               "subtotal":1000,"tax":180,"total":1180,
               "items":[{"description":"Demo item","quantity":2,"unit_price":500}]}
    r = client.post("/invoices/validate", json=payload)
    assert r.status_code == 200
    assert r.json()["status"] == "valid"

def test_total_mismatch():
    payload = {"supplier":"Example Supplies","invoice_number":"INV-2","currency":"INR",
               "subtotal":1000,"tax":180,"total":1100,
               "items":[{"description":"Demo item","quantity":2,"unit_price":500}]}
    assert client.post("/invoices/validate", json=payload).json()["status"] == "needs_review"
