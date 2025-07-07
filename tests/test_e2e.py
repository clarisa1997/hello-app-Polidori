# tests/test_e2e.py

import time
import requests

FRONTEND_URL = "http://localhost:8000"
BACKEND_URL = "http://localhost:5000/name"


def wait_for(url, timeout=30):
    """Poll `url` until it returns HTTP 200 or timeout expires."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(url, timeout=1)
            if r.status_code == 200:
                return r
        except requests.exceptions.RequestException:
            pass
        time.sleep(0.5)
    raise RuntimeError(
        f"Service at {url} did not \
                       become ready within {timeout}s"
    )


def test_e2e_backend_ready():
    # Wait for /name endpoint
    r = wait_for(BACKEND_URL)
    assert r.text.strip() != ""


def test_e2e_frontend_ready():
    # Wait for / endpoint
    r = wait_for(FRONTEND_URL)
    assert "Hello world" in r.text


def test_e2e_frontend_response():
    # Finally, do a real GET and check content
    r = requests.get(FRONTEND_URL)
    assert r.status_code == 200
    assert "Hello world" in r.text
