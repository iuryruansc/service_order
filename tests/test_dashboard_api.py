def test_get_dashboard_as_admin_returns_200(client, admin_token):
    response = client.get(
        "/dashboard/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    
def test_get_dashboard_as_regular_user_returns_403(client, auth_token):
    response = client.get(
        "/dashboard/",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 403

def test_get_dashboard_without_auth_returns_401(client):
    response = client.get(
        "/dashboard/"
    )
    assert response.status_code == 401

def test_get_dashboard_returns_correct_structure(client, admin_token):
    response = client.get(
        "/dashboard/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    data = response.json()

    assert "total_service_orders" in data
    assert "by_status" in data
    assert "by_priority" in data
    assert "open" in data["by_status"]
    assert "low" in data["by_priority"]