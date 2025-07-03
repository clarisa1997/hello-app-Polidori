
import requests

def test_get_name():
    response = requests.get("http://backend:5001/name")
    assert response.status_code == 200
    assert isinstance(response.text, str)
