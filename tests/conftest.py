import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.deps import get_db
from app.core.database import Base
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine,
)

def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def auth_token(client):
    client.post("/users/", json={
        "name": "Test User",
        "email": "test@email.com",
        "password": "123456",
    })

    response = client.post("/auth/login", data={
        "username": "test@email.com",
        "password": "123456",
    })
    return response.json()["access_token"]

@pytest.fixture()
def created_client(client, auth_token):
    response = client.post("/clients/", json={
        "name": "Test Client", 
        "email": "client@email.com"
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    return response.json()

@pytest.fixture()
def created_user(client, auth_token):
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    return response.json()

@pytest.fixture()
def created_service_order(client, auth_token, created_client, created_user):
    response = client.post(
        "/service-orders/",
        json={
            "title": "Test Service Order",
            "description": "Test Service Order",
            "status": "open",
            "priority": "medium",
            "client_id": created_client["id"],
            "responsible_user_id": created_user["id"],
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    return response.json()