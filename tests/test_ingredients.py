def test_list_ingredients_empty(client):
    response = client.get("/api/v1/ingredients/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_ingredient_requires_api_key(client):
    response = client.post("/api/v1/ingredients/", json={"name": "Ashwagandha"})
    assert response.status_code == 401


def test_create_ingredient_rejects_wrong_api_key(client):
    response = client.post(
        "/api/v1/ingredients/",
        json={"name": "Ashwagandha"},
        headers={"X-Api-Key": "wrong-key"},
    )
    assert response.status_code == 401


def test_create_and_fetch_ingredient(client, admin_headers):
    create_response = client.post(
        "/api/v1/ingredients/",
        json={"name": "Ashwagandha", "botanical_name": "Withania somnifera"},
        headers=admin_headers,
    )
    assert create_response.status_code == 200
    created = create_response.json()
    assert created["name"] == "Ashwagandha"
    assert created["id"] is not None

    get_response = client.get(f"/api/v1/ingredients/{created['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["botanical_name"] == "Withania somnifera"


def test_get_ingredient_not_found(client):
    response = client.get("/api/v1/ingredients/999999")
    assert response.status_code == 404


def test_list_ingredients_rejects_limit_above_max(client):
    response = client.get("/api/v1/ingredients/", params={"limit": 500})
    assert response.status_code == 422


def test_list_ingredients_rejects_negative_skip(client):
    response = client.get("/api/v1/ingredients/", params={"skip": -1})
    assert response.status_code == 422


def test_admin_api_key_unconfigured_disables_writes(client, monkeypatch):
    from app.core.config import get_settings

    monkeypatch.setenv("ADMIN_API_KEY", "")
    get_settings.cache_clear()
    try:
        response = client.post(
            "/api/v1/ingredients/",
            json={"name": "Ashwagandha"},
            headers={"X-Api-Key": ""},
        )
        assert response.status_code == 503
    finally:
        monkeypatch.setenv("ADMIN_API_KEY", "test-admin-secret")
        get_settings.cache_clear()
