from decimal import Decimal
from fastapi import FastAPI
from pydantic import BaseModel, Field, model_validator

app = FastAPI(title="Document Processing Validation Demo")

class InvoiceItem(BaseModel):
    description: str = Field(min_length=1, max_length=250)
    quantity: Decimal = Field(gt=0)
    unit_price: Decimal = Field(ge=0)

class InvoiceIn(BaseModel):
    supplier: str = Field(min_length=1, max_length=200)
    invoice_number: str = Field(min_length=1, max_length=100)
    currency: str = Field(min_length=3, max_length=3)
    subtotal: Decimal = Field(ge=0)
    tax: Decimal = Field(ge=0)
    total: Decimal = Field(ge=0)
    items: list[InvoiceItem]

    @model_validator(mode="after")
    def check_currency_and_totals(self):
        self.currency = self.currency.upper()
        if self.currency not in {"INR", "USD", "EUR", "GBP"}:
            raise ValueError("Unsupported demo currency")
        return self

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/invoices/validate")
def validate_invoice(invoice: InvoiceIn):
    calculated_subtotal = sum((item.quantity * item.unit_price for item in invoice.items), Decimal("0"))
    subtotal_ok = abs(calculated_subtotal - invoice.subtotal) <= Decimal("0.02")
    total_ok = abs(invoice.subtotal + invoice.tax - invoice.total) <= Decimal("0.02")
    issues = []
    if not subtotal_ok:
        issues.append("Line-item sum does not match supplied subtotal.")
    if not total_ok:
        issues.append("Subtotal plus tax does not match supplied total.")
    return {
        "invoice_number": invoice.invoice_number,
        "supplier": invoice.supplier,
        "currency": invoice.currency,
        "calculated_subtotal": str(calculated_subtotal.quantize(Decimal("0.01"))),
        "subtotal_matches": subtotal_ok,
        "total_matches": total_ok,
        "status": "valid" if not issues else "needs_review",
        "issues": issues,
        "note": "Demo validation only; it does not verify tax compliance, authenticity, or payment status."
    }
