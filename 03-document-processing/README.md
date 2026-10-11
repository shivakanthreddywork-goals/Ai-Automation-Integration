# Document Processing & Validation Demo

Demonstrates extracting structured fields from a supplied JSON representation of an invoice and validating totals. It intentionally avoids pretending to perform OCR; add OCR/PDF extraction as a separate, testable stage.

## Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open `/docs` and call `POST /invoices/validate`.

## Example
```json
{
  "supplier":"Example Supplies",
  "invoice_number":"INV-1001",
  "currency":"INR",
  "subtotal":1000,
  "tax":180,
  "total":1180,
  "items":[{"description":"Demo item","quantity":2,"unit_price":500}]
}
```

## Production considerations
Use OCR/document extraction for PDFs, validate currencies and tax rules with domain experts, detect duplicates, store original-document references securely, redact sensitive data, and route low-confidence cases to a human.
