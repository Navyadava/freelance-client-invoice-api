from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import Client, Invoice


TEST_DATABASE_URL = "sqlite://"


test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


def setup_function():
    db = TestingSessionLocal()

    db.query(Invoice).delete()
    db.query(Client).delete()
    db.commit()

    db.close()


def test_create_client_successfully():
    response = client.post(
        "/clients/",
        json={
            "name": "Test Client",
            "email": "test@example.com",
            "company": "Test Company",
            "phone": "555-1000"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Client"
    assert data["email"] == "test@example.com"

def test_reject_invalid_client_email():
    response = client.post(
        "/clients/",
        json={
            "name": "Bad Email Client",
            "email": "not-an-email",
            "company": "Test Company",
            "phone": "555-2000"
        }
    )

    assert response.status_code == 422

def test_read_clients():
    client.post(
        "/clients/",
        json={
            "name": "Client One",
            "email": "clientone@example.com",
            "company": "Company One",
            "phone": "555-3000"
        }
    )

    response = client.get("/clients/")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Client One"

def test_unknown_client_returns_404():
    response = client.get("/clients/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Client not found"

def test_create_invoice_for_valid_client():
    client_response = client.post(
        "/clients/",
        json={
            "name": "Invoice Client",
            "email": "invoiceclient@example.com",
            "company": "Invoice Company",
            "phone": "555-4000"
        }
    )

    client_id = client_response.json()["id"]

    response = client.post(
        "/invoices/",
        json={
            "client_id": client_id,
            "service": "Website Design",
            "amount": "750.00",
            "status": "unpaid",
            "due_date": "2026-10-15"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["client_id"] == client_id
    assert data["service"] == "Website Design"
    assert data["status"] == "unpaid"

def test_reject_invoice_for_unknown_client():
    response = client.post(
        "/invoices/",
        json={
            "client_id": 999,
            "service": "Logo Design",
            "amount": "300.00",
            "status": "unpaid",
            "due_date": "2026-10-20"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Client not found"

def test_mark_invoice_paid():
    client_response = client.post(
        "/clients/",
        json={
            "name": "Paid Client",
            "email": "paid@example.com",
            "company": "Paid Company",
            "phone": "555-5000"
        }
    )

    client_id = client_response.json()["id"]

    invoice_response = client.post(
        "/invoices/",
        json={
            "client_id": client_id,
            "service": "Consulting",
            "amount": "500.00",
            "status": "unpaid",
            "due_date": "2026-10-25"
        }
    )

    invoice_id = invoice_response.json()["id"]

    response = client.patch(
        f"/invoices/{invoice_id}/pay"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "paid"
    assert data["paid_at"] is not None

def test_get_summary_report():
    client_response = client.post(
        "/clients/",
        json={
            "name": "Report Client",
            "email": "report@example.com",
            "company": "Report Company",
            "phone": "555-6000"
        }
    )

    client_id = client_response.json()["id"]

    invoice_response = client.post(
        "/invoices/",
        json={
            "client_id": client_id,
            "service": "API Development",
            "amount": "1000.00",
            "status": "unpaid",
            "due_date": "2026-10-30"
        }
    )

    invoice_id = invoice_response.json()["id"]

    client.patch(
        f"/invoices/{invoice_id}/pay"
    )

    response = client.get("/reports/summary")

    assert response.status_code == 200

    data = response.json()

    assert data["total_invoices"] == 1
    assert data["total_income"] == 1000.0
    assert data["unpaid_total"] == 0.0