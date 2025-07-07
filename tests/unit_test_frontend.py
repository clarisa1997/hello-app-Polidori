import pytest
from frontend.app import app as frontend_app


@pytest.fixture
def client(monkeypatch):
    # Patch get_name to return a known value
    monkeypatch.setattr("frontend.app.get_name", lambda: "Clarissa")
    frontend_app.config["TESTING"] = True
    with frontend_app.test_client() as client:
        yield client


def test_hello_success(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Hello world, Clarissa!" in resp.data


def test_hello_backend_error(monkeypatch):
    # Simulate get_name returning -1 => error message
    frontend_app.config["TESTING"] = True
    monkeypatch.setattr("frontend.app.get_name", lambda: -1)
    with frontend_app.test_client() as client:
        resp = client.get("/")
        assert resp.status_code == 200
        assert b"There was an error getting the name" in resp.data
