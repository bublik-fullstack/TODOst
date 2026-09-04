import pytest
from httpx import AsyncClient


async def create_board_with_column(client, auth_headers):
    board_response = await client.post("/api/boards", json={"title": "Test Board"}, headers=auth_headers)
    board_id = board_response.json()["id"]
    columns_response = await client.get(f"/api/boards/{board_id}/columns", headers=auth_headers)
    column_id = columns_response.json()[0]["id"]
    return board_id, column_id


@pytest.mark.asyncio
async def test_create_task(client: AsyncClient, auth_headers):
    _, column_id = await create_board_with_column(client, auth_headers)

    response = await client.post(f"/api/columns/{column_id}/tasks", json={
        "title": "Test Task",
        "description": "A test task",
        "column_id": column_id,
        "priority": "high",
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["priority"] == "high"


@pytest.mark.asyncio
async def test_create_task_column_not_found(client: AsyncClient, auth_headers):
    response = await client.post("/api/columns/nonexistent/tasks", json={
        "title": "Test Task",
        "column_id": "nonexistent",
    }, headers=auth_headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_board_tasks(client: AsyncClient, auth_headers):
    _, column_id = await create_board_with_column(client, auth_headers)

    await client.post(f"/api/columns/{column_id}/tasks", json={
        "title": "Task 1",
        "column_id": column_id,
    }, headers=auth_headers)
    await client.post(f"/api/columns/{column_id}/tasks", json={
        "title": "Task 2",
        "column_id": column_id,
    }, headers=auth_headers)

    board_response = await client.post("/api/boards", json={"title": "Board"}, headers=auth_headers)
    board_id = board_response.json()["id"]

    response = await client.get(f"/api/boards/{board_id}/tasks", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2


@pytest.mark.asyncio
async def test_list_tasks_with_search(client: AsyncClient, auth_headers):
    _, column_id = await create_board_with_column(client, auth_headers)

    await client.post(f"/api/columns/{column_id}/tasks", json={
        "title": "Important Task",
        "column_id": column_id,
    }, headers=auth_headers)
    await client.post(f"/api/columns/{column_id}/tasks", json={
        "title": "Other Task",
        "column_id": column_id,
    }, headers=auth_headers)

    board_response = await client.post("/api/boards", json={"title": "Board"}, headers=auth_headers)
    board_id = board_response.json()["id"]

    response = await client.get(f"/api/boards/{board_id}/tasks?search=Important", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["tasks"][0]["title"] == "Important Task"


@pytest.mark.asyncio
async def test_list_tasks_with_priority_filter(client: AsyncClient, auth_headers):
    _, column_id = await create_board_with_column(client, auth_headers)

    await client.post(f"/api/columns/{column_id}/tasks", json={
        "title": "High Task",
        "column_id": column_id,
        "priority": "high",
    }, headers=auth_headers)
    await client.post(f"/api/columns/{column_id}/tasks", json={
        "title": "Low Task",
        "column_id": column_id,
        "priority": "low",
    }, headers=auth_headers)

    board_response = await client.post("/api/boards", json={"title": "Board"}, headers=auth_headers)
    board_id = board_response.json()["id"]

    response = await client.get(f"/api/boards/{board_id}/tasks?priority=high", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["tasks"][0]["priority"] == "high"


@pytest.mark.asyncio
async def test_get_task(client: AsyncClient, auth_headers):
    _, column_id = await create_board_with_column(client, auth_headers)

    create_response = await client.post(f"/api/columns/{column_id}/tasks", json={
        "title": "Get Me",
        "column_id": column_id,
    }, headers=auth_headers)
    task_id = create_response.json()["id"]

    response = await client.get(f"/api/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Get Me"


@pytest.mark.asyncio
async def test_update_task(client: AsyncClient, auth_headers):
    _, column_id = await create_board_with_column(client, auth_headers)

    create_response = await client.post(f"/api/columns/{column_id}/tasks", json={
        "title": "Old Title",
        "column_id": column_id,
    }, headers=auth_headers)
    task_id = create_response.json()["id"]

    response = await client.put(f"/api/tasks/{task_id}", json={
        "title": "New Title",
        "priority": "low",
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"
    assert response.json()["priority"] == "low"


@pytest.mark.asyncio
async def test_delete_task(client: AsyncClient, auth_headers):
    _, column_id = await create_board_with_column(client, auth_headers)

    create_response = await client.post(f"/api/columns/{column_id}/tasks", json={
        "title": "Delete Me",
        "column_id": column_id,
    }, headers=auth_headers)
    task_id = create_response.json()["id"]

    response = await client.delete(f"/api/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_move_task_same_column(client: AsyncClient, auth_headers):
    _, column_id = await create_board_with_column(client, auth_headers)

    task1_response = await client.post(f"/api/columns/{column_id}/tasks", json={
        "title": "Task 1",
        "column_id": column_id,
    }, headers=auth_headers)
    task2_response = await client.post(f"/api/columns/{column_id}/tasks", json={
        "title": "Task 2",
        "column_id": column_id,
    }, headers=auth_headers)

    task1_id = task1_response.json()["id"]

    response = await client.patch(f"/api/tasks/{task1_id}/move", json={
        "column_id": column_id,
        "order_position": 1,
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["order_position"] == 1


@pytest.mark.asyncio
async def test_move_task_cross_column(client: AsyncClient, auth_headers):
    board_id, col1_id = await create_board_with_column(client, auth_headers)

    columns_response = await client.get(f"/api/boards/{board_id}/columns", headers=auth_headers)
    col2_id = columns_response.json()[1]["id"]

    task_response = await client.post(f"/api/columns/{col1_id}/tasks", json={
        "title": "Moving Task",
        "column_id": col1_id,
    }, headers=auth_headers)
    task_id = task_response.json()["id"]

    response = await client.patch(f"/api/tasks/{task_id}/move", json={
        "column_id": col2_id,
        "order_position": 0,
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["column_id"] == col2_id


@pytest.mark.asyncio
async def test_cannot_access_other_user_task(client: AsyncClient, auth_headers, second_auth_headers):
    _, column_id = await create_board_with_column(client, auth_headers)

    create_response = await client.post(f"/api/columns/{column_id}/tasks", json={
        "title": "Private Task",
        "column_id": column_id,
    }, headers=auth_headers)
    task_id = create_response.json()["id"]

    response = await client.get(f"/api/tasks/{task_id}", headers=second_auth_headers)
    assert response.status_code == 404
