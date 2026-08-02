def test_search_rejects_empty_query(client):
    response = client.post("/api/v1/search/", json={"query": ""})
    assert response.status_code == 422


def test_search_rejects_query_over_max_length(client):
    response = client.post("/api/v1/search/", json={"query": "a" * 501})
    assert response.status_code == 422


def test_search_rejects_limit_out_of_range(client):
    response = client.post("/api/v1/search/", json={"query": "ashwagandha", "limit": 21})
    assert response.status_code == 422
    response = client.post("/api/v1/search/", json={"query": "ashwagandha", "limit": 0})
    assert response.status_code == 422


def test_search_with_no_vector_store_returns_insufficient_evidence(client):
    # The test Chroma directory has no "ayurveda_texts" collection, so the
    # retriever falls back to an empty result without any network call.
    response = client.post("/api/v1/search/", json={"query": "ashwagandha benefits"})
    assert response.status_code == 200
    body = response.json()
    assert body["evidence_status"] == "Insufficient Evidence"
    assert body["retrieved_citations"] == []
    assert body["sql_matches"] == []


def test_search_includes_sql_matches_for_seeded_ingredient(client, admin_headers):
    client.post(
        "/api/v1/ingredients/",
        json={"name": "Ashwagandha", "botanical_name": "Withania somnifera"},
        headers=admin_headers,
    )

    response = client.post("/api/v1/search/", json={"query": "ashwagandha"})
    assert response.status_code == 200
    sql_matches = response.json()["sql_matches"]
    assert len(sql_matches) == 1
    assert sql_matches[0]["entity_type"] == "Ingredient"
    assert sql_matches[0]["name"] == "Ashwagandha"


def test_search_escapes_sql_wildcards(client, admin_headers):
    client.post(
        "/api/v1/ingredients/",
        json={"name": "Ashwagandha"},
        headers=admin_headers,
    )

    # "%" is a SQL LIKE wildcard; unescaped it would match every row.
    response = client.post("/api/v1/search/", json={"query": "%"})
    assert response.status_code == 200
    assert response.json()["sql_matches"] == []


def test_search_uses_mocked_rag_pipeline(client, monkeypatch):
    mocked_result = {
        "evidence_status": "Supported",
        "confidence_score": 0.91,
        "generated_answer": "Ashwagandha is used as a rasayana (rejuvenative).",
        "retrieved_citations": [
            {
                "source_title": "Charaka Samhita",
                "chapter": "Chikitsa Sthana",
                "verse": "1.1",
                "exact_passage": "...",
                "similarity_score": 0.91,
            }
        ],
    }

    def fake_process_query(query, top_k=None):
        assert top_k == 5
        return mocked_result

    monkeypatch.setattr("app.services.search.process_query", fake_process_query)

    response = client.post("/api/v1/search/", json={"query": "ashwagandha", "limit": 5})
    assert response.status_code == 200
    body = response.json()
    assert body["evidence_status"] == "Supported"
    assert body["generated_answer"] == mocked_result["generated_answer"]
    assert len(body["retrieved_citations"]) == 1


def test_search_rate_limit_enforced(client, monkeypatch):
    from app.core.config import get_settings

    monkeypatch.setenv("SEARCH_RATE_LIMIT", "2/minute")
    get_settings.cache_clear()
    try:
        payload = {"query": "ashwagandha"}
        client.post("/api/v1/search/", json=payload)
        client.post("/api/v1/search/", json=payload)
        third = client.post("/api/v1/search/", json=payload)
        assert third.status_code == 429
    finally:
        monkeypatch.setenv("SEARCH_RATE_LIMIT", "1000/minute")
        get_settings.cache_clear()
