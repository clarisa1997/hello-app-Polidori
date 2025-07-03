
from frontend import app as frontend_app
import pytest

def test_get_name_error(monkeypatch):
    # Forza il metodo get_name() a fallire
    monkeypatch.setattr(frontend_app, "get_name", lambda: -1)

    client = frontend_app.app.test_client()
    response = client.get("/")
    assert b"There was an error getting the name" in response.data
