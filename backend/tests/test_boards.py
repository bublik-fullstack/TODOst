import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_board(client: AsyncClient, auth_headers):
    response = await client.post("/api/boards", json={
        "title": "My Board",
        "description": "A test board",
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My Board"
    assert data["description"] == "A test board"


@pytest.mark.asyncio
async def test_create_board_default_columns(client: AsyncClient, auth_headers):
    board_response = await client.post("/api/boards", json={
        "title": "Board with Columns",
    }, headers=auth_headers)
    board_id = board_response.json()["id"]

    columns_response = await client.get(f"/api/boards/{board_id}/columns", headers=auth_headers)
    assert columns_response.status_code == 200
    columns = columns_response.json()
    assert len(columns) == 3
    titles = [c["title"] for c in columns]
    assert "To Do" in titles
    assert "In Progress" in titles
    assert "Done" in titles


@pytest.mark.asyncio
async def test_list_boards(client: AsyncClient, auth_headers):
    await client.post("/api/boards", json={"title": "Board 1"}, headers=auth_headers)
    await client.post("/api/boards", json={"title": "Board 2"}, headers=auth_headers)

    response = await client.get("/api/boards", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["boards"]) == 2


@pytest.mark.asyncio
async def test_list_boards_with_pagination(client: AsyncClient, auth_headers):
    for i in range(5):
        await client.post("/api/boards", json={"title": f"Board {i}"}, headers=auth_headers)

    response = await client.get("/api/boards?skip=0&limit=2", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 5
    assert len(data["boards"]) == 2


@pytest.mark.asyncio
async def test_get_board(client: AsyncClient, auth_headers):
    create_response = await client.post("/api/boards", json={"title": "Get Me"}, headers=auth_headers)
    board_id = create_response.json()["id"]

    response = await client.get(f"/api/boards/{board_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Get Me"


@pytest.mark.asyncio
async def test_get_board_not_found(client: AsyncClient, auth_headers):
    response = await client.get("/api/boards/nonexistent", headers=auth_headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_board(client: AsyncClient, auth_headers):
    create_response = await client.post("/api/boards", json={"title": "Old Title"}, headers=auth_headers)
    board_id = create_response.json()["id"]

    response = await client.put(f"/api/boards/{board_id}", json={
        "title": "New Title",
        "description": "Updated",
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"
    assert response.json()["description"] == "Updated"


@pytest.mark.asyncio
async def test_delete_board(client: AsyncClient, auth_headers):
    create_response = await client.post("/api/boards", json={"title": "Delete Me"}, headers=auth_headers)
    board_id = create_response.json()["id"]

    response = await client.delete(f"/api/boards/{board_id}", headers=auth_headers)
    assert response.status_code == 204

    get_response = await client.get(f"/api/boards/{board_id}", headers=auth_headers)
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_cannot_access_other_user_board(client: AsyncClient, auth_headers, second_auth_headers):
    create_response = await client.post("/api/boards", json={"title": "Private Board"}, headers=auth_headers)
    board_id = create_response.json()["id"]

    response = await client.get(f"/api/boards/{board_id}", headers=second_auth_headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_cannot_delete_other_user_board(client: AsyncClient, auth_headers, second_auth_headers):
    create_response = await client.post("/api/boards", json={"title": "Private Board"}, headers=auth_headers)
    board_id = create_response.json()["id"]

    response = await client.delete(f"/api/boards/{board_id}", headers=second_auth_headers)
    assert response.status_code == 404
