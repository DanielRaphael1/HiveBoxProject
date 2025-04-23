from app import app

def test_version_route():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json() == {"version": "v0.0.1"}

def test_temperature_route():
    client = app.test_client()
    response = client.get('/temperature')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
