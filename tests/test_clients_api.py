
def test_client_create_with_success_returns_201(client, auth_token):
    payload = {
        "name": "Test Client",
        "email": "test@email.com",
    }

    response = client.post(
        "/clients/",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "Test Client"
    assert data["email"] == "test@email.com"
    assert data["is_active"] is True
    assert "id" in data

def test_client_create_without_auth_returns_401(client):
    payload = {
        "name": "Test Client",
        "email": "test@email.com",
    }

    response = client.post("/clients/", json=payload)

    assert response.status_code == 401

def test_client_create_with_same_email_returns_400(client, auth_token):
    payload = {
        "name": "Test Client",
        "email": "test@email.com",
    }
    client.post( "/clients/", json=payload, headers={"Authorization": f"Bearer {auth_token}"},)
    response = client.post( "/clients/", json=payload, headers={"Authorization": f"Bearer {auth_token}"},)

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_list_clients_returns_200(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get(
        "/clients/",
        headers=headers,
    )
    assert response.status_code == 200

def test_list_clients_without_auth_returns_401(client):
    response = client.get("/clients/")
    assert response.status_code == 401