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

def test_list_users_as_admin_returns_200(client, admin_token):
    response = client.get(
        "/users/",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200

def test_list_users_as_regular_user_returns_403(client, auth_token):
    response = client.get(
        "/users/",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 403

def test_list_users_without_auth_returns_401(client):
    response = client.get("/users/")
    assert response.status_code == 401

def test_activate_user_as_admin_returns_200(client, admin_token):
    create_response = client.post(
        "/users/",
        json={
            "name": "Inactive User",
            "email": "inactiveuser@email.com",
            "password": "123456",
        },
    )

    user_id = create_response.json()["id"]

    activate_response = client.patch(
        f"/users/{user_id}/activate",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert activate_response.status_code == 200
    assert activate_response.json()["is_active"] is True

def test_activate_user_as_regular_user_returns_403(client, auth_token):
    create_response = client.post(
        "/users/",
        json={
            "name": "Inactive User",
            "email": "inactiveuser@email.com",
            "password": "123456",
        },
    )
    user_id = create_response.json()["id"]

    activate_response = client.patch(
        f"/users/{user_id}/activate",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert activate_response.status_code == 403

def test_activate_nonexistent_user_as_admin_returns_404(client, admin_token):
    activate_response = client.patch(
        "/users/9999/activate",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert activate_response.status_code == 404
    assert activate_response.json()["detail"] == "User not found"

def test_deactivate_user_as_admin_returns_200(client, admin_token):
    create_response = client.post(
        "/users/",
        json={
            "name": "Active User",
            "email": "Activeuser@email.com",
            "password": "123456",
        },
    )

    user_id = create_response.json()["id"]

    deactivate_response = client.patch(
        f"/users/{user_id}/deactivate",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert deactivate_response.status_code == 200
    assert deactivate_response.json()["is_active"] is False

def test_deactivate_user_as_regular_user_returns_403(client, auth_token):
    create_response = client.post(
        "/users/",
        json={
            "name": "Active User",
            "email": "Activeuser@email.com",
            "password": "123456",
        },
    )
    user_id = create_response.json()["id"]

    deactivate_response = client.patch(
        f"/users/{user_id}/deactivate",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert deactivate_response.status_code == 403

def test_deactivate_nonexistent_user_as_admin_returns_404(client, admin_token):
    deactivate_response = client.patch(
        "/users/9999/deactivate",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert deactivate_response.status_code == 404
    assert deactivate_response.json()["detail"] == "User not found"