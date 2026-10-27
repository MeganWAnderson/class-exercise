import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_requests_have_different_ids(client):
    # TODO: send two GET /health requests.
    # Assert that their X-Request-ID header values are different.
    response1 = client.get("/health")
    response2 = client.get("/health")
    request_id1 = response1.headers.get("X-Request-ID")
    request_id2 = response2.headers.get("X-Request-ID")
    assert request_id1 is not None
    assert request_id2 is not None
    assert request_id1 != request_id2
