from psycopg2 import OperationalError
from backend.app import create_conn, get_name


class DummyCursor:
    def __init__(self, result):
        self._result = result

    def execute(self, query):
        pass

    def fetchone(self):
        return self._result


class DummyConn:
    def __init__(self, cursor):
        self._cursor = cursor

    def cursor(self):
        return self._cursor

    def close(self):
        pass


def test_create_conn_success(monkeypatch):
    # Simulate psycopg2.connect returning a connection
    monkeypatch.setattr(
        "backend.app.psycopg2." "connect",
        lambda **kw: DummyConn(DummyCursor(["ok"]))
    )
    conn = create_conn()
    assert conn is not None


def test_create_conn_failure(monkeypatch):
    # Simulate psycopg2.connect raising OperationalError
    def raiser(**kw):
        raise OperationalError("fail")

    monkeypatch.setattr("backend.app.psycopg2.connect", raiser)
    conn = create_conn()
    assert conn is None


def test_get_name_success(monkeypatch):
    # Simulate create_conn returning a connection
    # whose cursor returns ["Clarissa"]
    dummy = DummyConn(DummyCursor(["mario"]))
    monkeypatch.setattr("backend.app.create_conn", lambda: dummy)
    name = get_name()
    assert name == "mario"


def test_get_name_conn_none(monkeypatch):
    # Simulate create_conn returning None => get_name() should return -1
    monkeypatch.setattr("backend.app.create_conn", lambda: None)
    assert get_name() == -1
