from app.models.user import User


def register_and_login(
    client,
    email: str,
    password: str = "Test12345",
):
    client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": email,
            "password": password,
        },
    )

    login_response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )

    token = login_response.json()[
        "access_token"
    ]

    return {
        "Authorization": f"Bearer {token}"
    }


def test_create_video(client):
    headers = register_and_login(
        client,
        "create@example.com",
    )

    response = client.post(
        "/videos",
        json={
            "title": "Test Video",
            "description": "Testing video creation",
            "status": "processing",
        },
        headers=headers,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Test Video"
    assert (
        data["description"]
        == "Testing video creation"
    )
    assert data["status"] == "processing"
    assert "id" in data


def test_get_video_by_id(client):
    headers = register_and_login(
        client,
        "viewer@example.com",
    )

    create_response = client.post(
        "/videos",
        json={
            "title": "Video To Get",
            "description": "Get test",
            "status": "indexed",
        },
        headers=headers,
    )

    video_id = create_response.json()["id"]

    response = client.get(
        f"/videos/{video_id}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == video_id
    assert data["title"] == "Video To Get"


def test_get_missing_video_returns_404(
    client,
):
    headers = register_and_login(
        client,
        "missing@example.com",
    )

    response = client.get(
        "/videos/999999",
        headers=headers,
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Video not found"
    )


def test_normal_user_cannot_delete_video(
    client,
):
    headers = register_and_login(
        client,
        "normaldelete@example.com",
    )

    create_response = client.post(
        "/videos",
        json={
            "title": "Protected Video",
            "description": "Delete permission test",
            "status": "processing",
        },
        headers=headers,
    )

    video_id = create_response.json()["id"]

    response = client.delete(
        f"/videos/{video_id}",
        headers=headers,
    )

    assert response.status_code == 403


def test_admin_can_delete_video(
    client,
    db,
):
    headers = register_and_login(
        client,
        "deleteadmin@example.com",
    )

    create_response = client.post(
        "/videos",
        json={
            "title": "Delete Me",
            "description": "Admin delete test",
            "status": "processing",
        },
        headers=headers,
    )

    video_id = create_response.json()["id"]

    user = (
        db.query(User)
        .filter(
            User.email
            == "deleteadmin@example.com"
        )
        .first()
    )

    user.role = "admin"
    db.commit()

    response = client.delete(
        f"/videos/{video_id}",
        headers=headers,
    )

    assert response.status_code == 200

    assert (
        response.json()["message"]
        == "Video deleted successfully"
    )


def test_update_video_title(client):
    headers = register_and_login(
        client,
        "update@example.com",
    )

    create_response = client.post(
        "/videos",
        json={
            "title": "Old Title",
            "description": "Original description",
            "status": "processing",
        },
        headers=headers,
    )

    video_id = create_response.json()["id"]

    response = client.patch(
        f"/videos/{video_id}",
        json={
            "title": "New Title",
        },
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "New Title"
    assert (
        data["description"]
        == "Original description"
    )
    assert data["status"] == "processing"


def test_replace_video(client):
    headers = register_and_login(
        client,
        "replace@example.com",
    )

    create_response = client.post(
        "/videos",
        json={
            "title": "Old Title",
            "description": "Old Description",
            "status": "processing",
        },
        headers=headers,
    )

    video_id = create_response.json()["id"]

    response = client.put(
        f"/videos/{video_id}",
        json={
            "title": "New Title",
            "description": "New Description",
            "status": "indexed",
        },
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "New Title"
    assert data["description"] == "New Description"
    assert data["status"] == "indexed"


def test_search_videos(client):
    headers = register_and_login(
        client,
        "search@example.com",
    )

    client.post(
        "/videos",
        json={
            "title": "FastAPI Course",
            "description": "Backend learning",
            "status": "indexed",
        },
        headers=headers,
    )

    client.post(
        "/videos",
        json={
            "title": "Python Basics",
            "description": "Beginner course",
            "status": "processing",
        },
        headers=headers,
    )

    response = client.get(
        "/videos/search?q=fastapi",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert (
        data["results"][0]["title"]
        == "FastAPI Course"
    )


def test_filter_videos_by_status(client):
    headers = register_and_login(
        client,
        "filter@example.com",
    )

    client.post(
        "/videos",
        json={
            "title": "Indexed Video",
            "description": "Test",
            "status": "indexed",
        },
        headers=headers,
    )

    client.post(
        "/videos",
        json={
            "title": "Failed Video",
            "description": "Test",
            "status": "failed",
        },
        headers=headers,
    )

    response = client.get(
        "/videos/filter?status=failed",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert (
        data["results"][0]["status"]
        == "failed"
    )


def test_filter_pagination(client):
    headers = register_and_login(
        client,
        "pagination@example.com",
    )

    for i in range(5):
        client.post(
            "/videos",
            json={
                "title": f"Video {i}",
                "description": "Pagination test",
                "status": "processing",
            },
            headers=headers,
        )

    response = client.get(
        "/videos/filter?page=1&page_size=2",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 5
    assert data["page"] == 1
    assert data["page_size"] == 2
    assert len(data["results"]) == 2


def test_create_video_with_invalid_status(
    client,
):
    headers = register_and_login(
        client,
        "invalidstatus@example.com",
    )

    response = client.post(
        "/videos",
        json={
            "title": "Invalid Video",
            "description": "Invalid status",
            "status": "something_wrong",
        },
        headers=headers,
    )

    assert response.status_code == 422


def test_filter_rejects_invalid_page(
    client,
):
    response = client.get(
        "/videos/filter?page=0"
    )

    assert response.status_code == 422