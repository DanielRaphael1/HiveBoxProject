import pytest
from app import app
from unittest.mock import patch

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_version_route(client):
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json == {"version": "v0.0.2"}

@patch("app.requests.get")
def test_temperature_route_success(mock_get, client):
    mock_get.return_value.json.return_value = [
        {"value": "15.5", "createdAt": "now"},
        {"value": "16.0", "createdAt": "now"}
    ]
    mock_get.return_value.raise_for_status = lambda: None

    response = client.get("/temperature")
    assert response.status_code == 200
    data = response.get_json()

    assert isinstance(data, list)
    for box in data:
        assert "box" in box
        assert "status" in box
        assert box["status"] in ["Too Cold", "Good", "Too Hot", "No Data"]

@patch("app.requests.get")
def test_temperature_route_failure(mock_get, client):
    mock_get.side_effect = Exception("API failed")

    response = client.get("/temperature")
    assert response.status_code == 200
    data = response.get_json()

    for box in data:
        assert "error" in box
