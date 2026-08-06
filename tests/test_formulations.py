def test_list_formulations_empty(client):
    response = client.get("/api/v1/formulations/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_formulation_requires_api_key(client):
    response = client.post("/api/v1/formulations/", json={"name": "Panchagavya"})
    assert response.status_code == 401


def test_create_and_fetch_formulation(client, admin_headers):
    create_response = client.post(
        "/api/v1/formulations/",
        json={"name": "Panchagavya", "therapeutic_use": "Detoxification"},
        headers=admin_headers,
    )
    assert create_response.status_code == 200
    created = create_response.json()

    get_response = client.get(f"/api/v1/formulations/{created['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["therapeutic_use"] == "Detoxification"


def test_get_formulation_not_found(client):
    response = client.get("/api/v1/formulations/999999")
    assert response.status_code == 404
