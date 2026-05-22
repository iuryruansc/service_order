def test_login_returns_access_token(client):
    client.post(
        "/users/",
        json={
            "name": "Italo",
            "email": "italo@email.com",
            "password": "123456",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "italo@email.com",
            "password": "123456",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_with_wrong_password_returns_401(client):
    client.post(
        "/users/",
        json={
            "name": "Italo",
            "email": "italo@email.com",
            "password": "123456",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "italo@email.com",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"