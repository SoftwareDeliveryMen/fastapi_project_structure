from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserUpdate

def test_create_user(db):
    repo = UserRepository(db)
    user_create = UserCreate(
        email="repo@example.com",
        username="repouser",
        password="password123",
        is_active=True
    )
    user = repo.create(user_create)
    assert user.id is not None
    assert user.email == "repo@example.com"
    assert user.username == "repouser"

def test_get_user_by_id(db, test_user):
    repo = UserRepository(db)
    user = repo.get_by_id(test_user.id)
    assert user is not None
    assert user.id == test_user.id

def test_get_user_by_email(db, test_user):
    repo = UserRepository(db)
    user = repo.get_by_email("test@example.com")
    assert user is not None
    assert user.email == "test@example.com"

def test_get_user_by_username(db, test_user):
    repo = UserRepository(db)
    user = repo.get_by_username("testuser")
    assert user is not None
    assert user.username == "testuser"

def test_update_user(db, test_user):
    repo = UserRepository(db)
    user_update = UserUpdate(email="newemail@example.com")
    updated_user = repo.update(test_user, user_update)
    assert updated_user.email == "newemail@example.com"

def test_delete_user(db, test_user):
    repo = UserRepository(db)
    repo.delete(test_user)
    user = repo.get_by_id(test_user.id)
    assert user is None
