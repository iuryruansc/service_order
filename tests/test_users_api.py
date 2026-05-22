def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "name": "Italo",
            "email": "italo@email.com",
            "password": "123456",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Italo"
    assert data["email"] == "italo@email.com"
    assert data["is_active"] is True
    assert "id" in data
    assert "password" not in data
    assert "hashed_password" not in data

def test_create_user_with_duplicate_email_returns_400(client):
    payload = {
        "name": "Italo",
        "email": "italo@email.com",
        "password": "123456",
    }

    first_response = client.post("/users/", json=payload)
    second_response = client.post("/users/", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Email already registered"