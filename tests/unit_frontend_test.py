import pytest
from frontend.app import app as frontend_app

# Define a pytest fixture that provides a test client for the frontend app
# It monkeypatches the get_name function to return a known fixed value
@pytest.fixture
def client(monkeypatch):
    # Replace get_name with a lambda that returns "Clarissa"
    monkeypatch.setattr("frontend.app.get_name", lambda: "Clarissa")
    frontend_app.config["TESTING"] = True  # Enable testing mode in Flask
    with frontend_app.test_client() as client:
        yield client  # Yield the test client to the test functions

# Test that the frontend returns the expected message when backend works correctly
def test_hello_success(client):
    resp = client.get("/")  # Send a GET request to the root endpoint
    assert resp.status_code == 200  # Check that the response status is OK
    assert b"Hello world, Clarissa!" in resp.data  # Verify the correct greeting is in the response

# Test that the frontend handles a backend error properly
def test_hello_backend_error(monkeypatch):
    frontend_app.config["TESTING"] = True
    # Replace get_name with a lambda that returns -1 to simulate a backend failure
    monkeypatch.setattr("frontend.app.get_name", lambda: -1)
    with frontend_app.test_client() as client:
        resp = client.get("/")  # Send a GET request to the root endpoint
        assert resp.status_code == 200  # The response should still be successful
        assert b"There was an error getting the name" in resp.data  # Check that the error message is displayed
