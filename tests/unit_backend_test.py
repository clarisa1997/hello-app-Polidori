from psycopg2 import OperationalError
import tempfile
from backend.app import create_conn, get_name

# Dummy cursor class to simulate a database cursor
class DummyCursor:
    def __init__(self, result):
        self._result = result

    def execute(self, query):
        pass  # No actual execution

    def fetchone(self):
        return self._result  # Return the mocked query result


# Dummy connection class to simulate a database connection
class DummyConn:
    def __init__(self, cursor):
        self._cursor = cursor

    def cursor(self):
        return self._cursor

    def close(self):
        pass  # No real close


# Test create_conn: simulate successful DB connection
def test_create_conn_success(monkeypatch):
    # Create a temp file to mock the DB password secret
    with tempfile.NamedTemporaryFile("w", delete=False) as tmp:
        tmp.write("dummy_password")
        tmp_path = tmp.name

    # Override env var to use the temp file
    monkeypatch.setenv("DB_PASSWORD_FILE", tmp_path)

    # Patch psycopg2.connect to return a dummy connection
    monkeypatch.setattr(
        "backend.app.psycopg2.connect",
        lambda **kw: DummyConn(DummyCursor(["ok"]))
    )

    # Assert that connection is successfully created
    conn = create_conn()
    assert conn is not None


# Test create_conn: simulate a connection failure
def test_create_conn_failure(monkeypatch):
    with tempfile.NamedTemporaryFile("w", delete=False) as tmp:
        tmp.write("dummy_password")
        tmp_path = tmp.name

    monkeypatch.setenv("DB_PASSWORD_FILE", tmp_path)

    # Raise OperationalError to simulate failure
    def raiser(**kw):
        raise OperationalError("fail")

    monkeypatch.setattr("backend.app.psycopg2.connect", raiser)

    # Assert that the connection fails and returns None
    conn = create_conn()
    assert conn is None


# Test get_name: should return "Clarissa" from mocked connection
def test_get_name_success(monkeypatch):
    dummy = DummyConn(DummyCursor(["Clarissa"]))
    monkeypatch.setattr("backend.app.create_conn", lambda: dummy)
    name = get_name()
    assert name == "Clarissa"


# Test get_name: should return "-1" when connection is None
def test_get_name_conn_none(monkeypatch):
    monkeypatch.setattr("backend.app.create_conn", lambda: None)
    assert get_name() == "-1"
