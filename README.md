# Freelance Client & Invoice Manager API

A FastAPI backend for managing freelance clients, invoices, payments, and summary reports.

## Features

- Client CRUD
- Client search
- Invoice creation and listing
- Invoice filters by status and client
- Mark invoices as paid
- Summary report
- Email and request validation
- SQLite database storage
- Automated tests
- Swagger API documentation

## Tech Stack

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- pytest
- Uvicorn

## Main Endpoints

### Clients

```text
POST   /clients/
GET    /clients/
GET    /clients/{client_id}
PUT    /clients/{client_id}
DELETE /clients/{client_id}
```

### Invoices

```text
POST  /invoices/
GET   /invoices/
GET   /invoices/{invoice_id}
PATCH /invoices/{invoice_id}/pay
```

### Reports

```text
GET /reports/summary
```

## Run Locally

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Open Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## Testing

Run:

```bash
python -m pytest -v
```

The project includes 8 automated tests covering clients, invoices, validation, payments, and reports.

## Example Client

```json
{
  "name": "Test Client",
  "email": "test@example.com",
  "company": "Test Company",
  "phone": "555-1000"
}
```

## Example Invoice

```json
{
  "client_id": 1,
  "service": "Website Design",
  "amount": "750.00",
  "status": "unpaid",
  "due_date": "2026-10-15"
}
```

## Author

Navya Dava