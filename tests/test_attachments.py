def test_attachment_upload_returns_201(client, auth_token, created_service_order):
    response = client.post(
        f"/service-orders/{created_service_order['id']}/attachments",
        files={"file": ("test.jpg", b"fake image content", "image/jpeg")},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 201

    data = response.json()
    assert data["filename"] == "test.jpg"
    assert "id" in data

def test_attachment_upload_without_auth_returns_401(client, created_service_order):
    response = client.post(
        f"/service-orders/{created_service_order['id']}/attachments",
        files={"file": ("test.jpg", b"fake image content", "image/jpeg")},
    )

    assert response.status_code == 401

def test_attachment_upload_with_invalid_type_returns_400(client, auth_token, created_service_order):
    response = client.post(
        f"/service-orders/{created_service_order['id']}/attachments",
        files={"file": ("malware.exe", b"fake content", "application/octet-stream")},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 400

def test_attachment_upload_from_nonexistent_order_returns_404(client, auth_token):
    response = client.post(
        f"/service-orders/1/attachments",
        files={"file": ("test.jpg", b"fake image content", "image/jpeg")},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 404

def test_get_all_attachments_from_an_order_returns_200(client, auth_token, created_service_order):
    response = client.get(
        f"/service-orders/{created_service_order['id']}/attachments",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200

def test_delete_attachment_as_admin_returns_204(client, admin_token, created_service_order, created_attachment):
    response = client.delete(
        f"/service-orders/{created_service_order['id']}/attachments/{created_attachment['id']}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 204

def test_delete_attachment_as_non_admin_returns_403(client, auth_token, created_service_order, created_attachment):
    response = client.delete(
        f"/service-orders/{created_service_order['id']}/attachments/{created_attachment['id']}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 403