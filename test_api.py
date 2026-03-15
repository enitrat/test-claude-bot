# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "fastapi",
#   "httpx",
#   "pytest",
# ]
# ///
from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


def test_health_check_returns_200() -> None:
    response = client.get("/")
    assert response.status_code == 200


def test_health_check_returns_json_status_ok() -> None:
    response = client.get("/")
    assert response.headers["content-type"].startswith("application/json")
    assert response.json() == {"status": "ok"}
