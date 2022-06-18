from fastapi import Response
import pytest
from fastapi.testclient import TestClient

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from main import app
from src.settings import Settings
from src.database.connection import get_db, Base

from src.apps.recipes.models import Recipe
from src.apps.reviews.models import Review
from src.apps.users.models import User


test_settings = Settings()
test_settings.TEST_MODE = True

SQLALCHEMY_DATABASE_URL = test_settings.postgres_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.fixture()
def session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    nested = connection.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]
