def test_create_service_order_with_success_returns_201(client, auth_token, created_client, created_user):
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {
        "title": "Test Service Order",
        "description": "Test Service Order",
        "priority": "medium",
        "client_id": created_client["id"],
    }

    response = client.post(
        "/service-orders/",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 201

    data = response.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["priority"] == payload["priority"]
    assert data["client_id"] == payload["client_id"]
    assert data["responsible_user_id"] == created_user["id"]

def test_create_service_order_without_auth_returns_401(client, created_client):
    payload = {
        "title": "Test Service Order",
        "description": "Test Service Order",
        "priority": "medium",
        "client_id": created_client["id"],
    }

    response = client.post("/service-orders/", json=payload)

    assert response.status_code == 401

def test_list_service_order_returns_200(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    response = client.get(
        "/service-orders/",
        headers=headers
    )

    assert response.status_code == 200

def test_list_service_order_without_auth_returns_401(client):
    response = client.get("/service-orders/")
    assert response.status_code == 401

def test_get_service_order_by_id_returns_200(client, auth_token, created_service_order):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get(
        f"/service-orders/{created_service_order['id']}",
        headers=headers
    )
    assert response.status_code == 200

def test_get_service_order_by_id_not_found_returns_404(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get(
        "/service-orders/999",
        headers=headers
    )
    assert response.status_code == 404

def test_create_service_order_with_invalid_client_id_returns_404(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {
        "title": "Test Service Order",
        "description": "Test Service Order",
        "priority": "medium",
        "client_id": 999,  # Invalid client ID
    }

    response = client.post(
        "/service-orders/",
        json=payload,
        headers=headers
    )
    assert response.status_code == 404

def test_get_service_order_history_returns_200(client, auth_token, created_service_order):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get(
        f"/service-orders/{created_service_order['id']}/history",
        headers=headers
    )
    assert response.status_code == 200

def test_update_service_order_status_with_valid_transition_returns_200(client, auth_token, created_service_order):
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {"status": "in_progress"}

    response = client.patch(
        f"/service-orders/{created_service_order['id']}/status",
        json=payload,
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"

def test_update_service_order_status_with_invalid_transition_returns_400(client, auth_token, created_service_order):
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {"status": "done"}

    response = client.patch(
        f"/service-orders/{created_service_order['id']}/status",
        json=payload,
        headers=headers
    )
    assert response.status_code == 400