import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import get_db
from app.models.user import Base
from app.core.security import get_password_hash

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(db):
    from app.models.user import User
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("TestPassword123"),
        is_active=True,
        is_superuser=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def test_superuser(db):
    from app.models.user import User
    user = User(
        email="admin@example.com",
        username="admin",
        hashed_password=get_password_hash("AdminPassword123"),
        is_active=True,
        is_superuser=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def user_token(client, test_user):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "TestPassword123"}
    )
    return response.json()["access_token"]

@pytest.fixture
def superuser_token(client, test_superuser):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "AdminPassword123"}
    )
    return response.json()["access_token"]
