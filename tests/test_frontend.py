
import requests

def test_frontend_root():
    response = requests.get("http://frontend:8000/")
    assert response.status_code == 200
    assert "Hello world" in response.text
