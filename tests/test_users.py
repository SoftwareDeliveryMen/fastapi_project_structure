def test_create_user(client):
    response = client.post(
        "/api/v1/users/",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "newpassword123",
            "is_active": True
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"
    assert "id" in data
    assert "hashed_password" not in data

def test_create_user_duplicate_email(client, test_user):
    response = client.post(
        "/api/v1/users/",
        json={
            "email": "test@example.com",
            "username": "anotheruser",
            "password": "password123",
            "is_active": True
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_create_user_duplicate_username(client, test_user):
    response = client.post(
        "/api/v1/users/",
        json={
            "email": "another@example.com",
            "username": "testuser",
            "password": "password123",
            "is_active": True
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already taken"

def test_read_current_user(client, user_token):
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"

def test_read_current_user_unauthorized(client):
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401

def test_read_user_by_id(client, user_token, test_user):
    response = client.get(
        f"/api/v1/users/{test_user.id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["username"] == "testuser"

def test_read_users_as_superuser(client, superuser_token, test_user):
    response = client.get(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {superuser_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_read_users_as_regular_user(client, user_token):
    response = client.get(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403

def test_update_user(client, user_token, test_user):
    response = client.put(
        f"/api/v1/users/{test_user.id}",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"email": "updated@example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "updated@example.com"

def test_delete_user_as_superuser(client, superuser_token, test_user):
    response = client.delete(
        f"/api/v1/users/{test_user.id}",
        headers={"Authorization": f"Bearer {superuser_token}"}
    )
    assert response.status_code == 204

def test_delete_user_as_regular_user(client, user_token, test_user):
    response = client.delete(
        f"/api/v1/users/{test_user.id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403
