from app import app

def test_version_route():
    client = app.test_client()
    response = client.get('/version')
    assert response.status_code == 200
    assert "version" in response.get_json()

def test_temperature_route():
    client = app.test_client()
    response = client.get('/temperature')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
