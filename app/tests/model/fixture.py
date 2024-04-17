from ...src.model.model import Model
from app.src.model.database import connect, close
import pytest


@pytest.fixture(scope="package")
def model():
    conn = connect()
    yield Model(conn)
    close(conn)


@pytest.fixture(scope="package")
def cursor():
    conn = connect()
    cursor = conn.cursor()
    yield cursor
    close(conn)


@pytest.fixture(scope="package")
def ledger(model):
    yield model.get_ledger()


@pytest.fixture(scope="package")
def journal(model):
    yield model.get_journal()


@pytest.fixture(scope="package")
def month():
    return 2


@pytest.fixture(scope="package")
def year():
    return 2024
