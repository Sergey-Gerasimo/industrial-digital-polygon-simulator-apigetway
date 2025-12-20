from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root(client: TestClient) -> None:
    response = client.get("/api/")
    assert response.status_code == 200
    payload = response.json()
    assert payload["version"]
    assert payload["message"].startswith("Industrial Digital Polygon")
