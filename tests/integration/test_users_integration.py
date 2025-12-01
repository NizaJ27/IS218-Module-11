import os
import time
import pytest
from fastapi.testclient import TestClient

from main import app
from app.db import init_db


@pytest.fixture(autouse=True)
def setup_db():
    # Ensure tables exist for the configured DATABASE_URL
    # If using the default sqlite file, remove it to start fresh between runs
    try:
        from app.db import DATABASE_URL
        if DATABASE_URL.startswith("sqlite") and "test_db.sqlite" in DATABASE_URL:
            import os

            if os.path.exists("./test_db.sqlite"):
                os.remove("./test_db.sqlite")
    except Exception:
        pass
    init_db()
    yield


def test_register_and_uniqueness():
    client = TestClient(app)
    payload = {"username": "tester1", "email": "tester1@example.com", "password": "pass123"}
    r = client.post("/users", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["username"] == "tester1"
    assert data["email"] == "tester1@example.com"
    assert "password_hash" not in data

    # Attempt duplicate
    r2 = client.post("/users", json=payload)
    assert r2.status_code == 400


def test_invalid_email_via_endpoint():
    client = TestClient(app)
    payload = {"username": "tester2", "email": "not-an-email", "password": "pass123"}
    r = client.post("/users", json=payload)
    # This application maps validation errors to HTTP 400 in the handler
    assert r.status_code == 400
