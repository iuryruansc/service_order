def test_export_excel_as_admin_returns_200(client, admin_token):
    response = client.get(
        "/service-orders/export?format=excel",
        headers = {"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

def test_export_pdf_as_admin_returns_200(client, admin_token):
    response = client.get(
        "/service-orders/export?format=pdf",
        headers = {"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"

def test_export_as_regular_user_returns_403(client, auth_token):
    response = client.get(
        "/service-orders/export?format=excel",
        headers = {"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 403

def test_export_without_auth_returs_401(client):
    response = client.get(
        "/service-orders/export?format=excel",
    )

    assert response.status_code == 401

def test_export_with_invalid_format_returns_422(client, admin_token):
    response = client.get(
        "/service-orders/export?format=random",
        headers = {"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 422