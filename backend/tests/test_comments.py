import pytest
from httpx import AsyncClient


async def create_task_for_comments(client, auth_headers):
    board_response = await client.post("/api/boards", json={"title": "Test Board"}, headers=auth_headers)
    board_id = board_response.json()["id"]
    columns_response = await client.get(f"/api/boards/{board_id}/columns", headers=auth_headers)
    column_id = columns_response.json()[0]["id"]
    task_response = await client.post(f"/api/columns/{column_id}/tasks", json={
        "title": "Test Task",
        "column_id": column_id,
    }, headers=auth_headers)
    task_id = task_response.json()["id"]
    return board_id, task_id


@pytest.mark.asyncio
async def test_add_comment(client: AsyncClient, auth_headers):
    _, task_id = await create_task_for_comments(client, auth_headers)

    response = await client.post(f"/api/tasks/{task_id}/comments", json={
        "content": "This is a comment",
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["content"] == "This is a comment"


@pytest.mark.asyncio
async def test_list_comments(client: AsyncClient, auth_headers):
    _, task_id = await create_task_for_comments(client, auth_headers)

    await client.post(f"/api/tasks/{task_id}/comments", json={
        "content": "Comment 1",
    }, headers=auth_headers)
    await client.post(f"/api/tasks/{task_id}/comments", json={
        "content": "Comment 2",
    }, headers=auth_headers)

    response = await client.get(f"/api/tasks/{task_id}/comments", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_list_comments_with_pagination(client: AsyncClient, auth_headers):
    _, task_id = await create_task_for_comments(client, auth_headers)

    for i in range(5):
        await client.post(f"/api/tasks/{task_id}/comments", json={
            "content": f"Comment {i}",
        }, headers=auth_headers)

    response = await client.get(f"/api/tasks/{task_id}/comments?skip=0&limit=2", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_update_own_comment(client: AsyncClient, auth_headers):
    _, task_id = await create_task_for_comments(client, auth_headers)

    create_response = await client.post(f"/api/tasks/{task_id}/comments", json={
        "content": "Original",
    }, headers=auth_headers)
    comment_id = create_response.json()["id"]

    response = await client.put(f"/api/tasks/{task_id}/comments/{comment_id}", json={
        "content": "Updated",
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["content"] == "Updated"


@pytest.mark.asyncio
async def test_cannot_update_others_comment(client: AsyncClient, auth_headers, second_auth_headers):
    _, task_id = await create_task_for_comments(client, auth_headers)

    create_response = await client.post(f"/api/tasks/{task_id}/comments", json={
        "content": "My comment",
    }, headers=auth_headers)
    comment_id = create_response.json()["id"]

    response = await client.put(f"/api/tasks/{task_id}/comments/{comment_id}", json={
        "content": "Hacked",
    }, headers=second_auth_headers)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_own_comment(client: AsyncClient, auth_headers):
    _, task_id = await create_task_for_comments(client, auth_headers)

    create_response = await client.post(f"/api/tasks/{task_id}/comments", json={
        "content": "Delete me",
    }, headers=auth_headers)
    comment_id = create_response.json()["id"]

    response = await client.delete(f"/api/tasks/{task_id}/comments/{comment_id}", headers=auth_headers)
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_cannot_delete_others_comment(client: AsyncClient, auth_headers, second_auth_headers):
    _, task_id = await create_task_for_comments(client, auth_headers)

    create_response = await client.post(f"/api/tasks/{task_id}/comments", json={
        "content": "My comment",
    }, headers=auth_headers)
    comment_id = create_response.json()["id"]

    response = await client.delete(f"/api/tasks/{task_id}/comments/{comment_id}", headers=second_auth_headers)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_comment_task_not_found(client: AsyncClient, auth_headers):
    response = await client.post("/api/tasks/nonexistent/comments", json={
        "content": "Comment",
    }, headers=auth_headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_cannot_comment_on_other_user_task(client: AsyncClient, auth_headers, second_auth_headers):
    _, task_id = await create_task_for_comments(client, auth_headers)

    response = await client.post(f"/api/tasks/{task_id}/comments", json={
        "content": "Intrusion",
    }, headers=second_auth_headers)
    assert response.status_code == 404
