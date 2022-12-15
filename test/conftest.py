from server.db_config import Base, get_db
from server.api.vehicles.vehicle_routes import vehicle_router
from typing import Any
from typing import Generator
from fastapi import FastAPI
from fastapi.testclient import TestClient
from server.db_config import engine, Session
import pytest

def start_application():
    app = FastAPI()
    app.include_router(vehicle_router)
    return app

@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    
    # Create a fresh database on each test case.
    
    Base.metadata.create_all(engine)
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[Session, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session  
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(
    app: FastAPI, db_session: Session
) -> Generator[TestClient, Any, None]:

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client