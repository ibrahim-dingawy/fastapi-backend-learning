from app.models.user import User


def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "Test12345",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test User"
    assert data["email"] == "testuser@example.com"
    assert data["role"] == "user"

    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_email(client):
    user_data = {
        "name": "Test User",
        "email": "duplicate@example.com",
        "password": "Test12345",
    }

    client.post(
        "/auth/register",
        json=user_data,
    )

    response = client.post(
        "/auth/register",
        json=user_data,
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Email is already registered"
    )


def test_login_success(client):
    client.post(
        "/auth/register",
        json={
            "name": "Login User",
            "email": "login@example.com",
            "password": "Test12345",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "login@example.com",
            "password": "Test12345",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post(
        "/auth/register",
        json={
            "name": "Wrong Password User",
            "email": "wrong@example.com",
            "password": "CorrectPassword",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "wrong@example.com",
            "password": "WrongPassword",
        },
    )

    assert response.status_code == 401
    assert (
        response.json()["detail"]
        == "Invalid email or password"
    )


def test_me_without_token(client):
    response = client.get(
        "/auth/me"
    )

    assert response.status_code == 401


def test_me_with_valid_token(client):
    client.post(
        "/auth/register",
        json={
            "name": "Authenticated User",
            "email": "auth@example.com",
            "password": "Test12345",
        },
    )

    login_response = client.post(
        "/auth/login",
        data={
            "username": "auth@example.com",
            "password": "Test12345",
        },
    )

    token = login_response.json()[
        "access_token"
    ]

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": (
                f"Bearer {token}"
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "auth@example.com"
    assert data["name"] == "Authenticated User"


def test_normal_user_cannot_access_admin(
    client,
):
    client.post(
        "/auth/register",
        json={
            "name": "Normal User",
            "email": "normal@example.com",
            "password": "Test12345",
        },
    )

    login_response = client.post(
        "/auth/login",
        data={
            "username": "normal@example.com",
            "password": "Test12345",
        },
    )

    token = login_response.json()[
        "access_token"
    ]

    response = client.get(
        "/auth/admin-test",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 403


def test_admin_can_access_admin_endpoint(
    client,
    db,
):
    client.post(
        "/auth/register",
        json={
            "name": "Admin User",
            "email": "admin@example.com",
            "password": "Test12345",
        },
    )

    user = (
        db.query(User)
        .filter(
            User.email == "admin@example.com"
        )
        .first()
    )

    user.role = "admin"

    db.commit()

    login_response = client.post(
        "/auth/login",
        data={
            "username": "admin@example.com",
            "password": "Test12345",
        },
    )

    token = login_response.json()[
        "access_token"
    ]

    response = client.get(
        "/auth/admin-test",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Welcome admin"