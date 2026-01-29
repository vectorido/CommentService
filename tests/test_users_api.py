from httpx import AsyncClient


async def test_create_user_invalid_email(client: AsyncClient):
    user_data = {
        "email": "invalid-email",
        "name": "Test User"
    }
    response = await client.post("/users/", json=user_data)
    assert response.status_code == 422


async def test_create_user(client: AsyncClient):
    user_data = {
        "email": "test@example.com",
        "name": "Test User"
    }
    response = await client.post("/users/", json=user_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["name"] == user_data["name"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


async def test_create_user_duplicate_email(client: AsyncClient):
    user_data = {
        "email": "duplicate@example.com",
        "name": "Test User"
    }
    
    await client.post("/users/", json=user_data)
    response = await client.post("/users/", json=user_data)
    
    assert response.status_code == 409


async def test_get_user_by_id(client: AsyncClient):
    user_data = {
        "email": "getuser@example.com",
        "name": "Get User"
    }
    create_response = await client.post("/users/", json=user_data)
    user_id = create_response.json()["id"]
    
    response = await client.get(f"/users/{user_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == user_data["email"]
    assert data["name"] == user_data["name"]


async def test_get_user_not_found(client: AsyncClient):
    response = await client.get("/users/999999")
    assert response.status_code == 404


async def test_get_all_users(client: AsyncClient):
    response = await client.get("/users/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)


async def test_update_user(client: AsyncClient):
    user_data = {
        "email": "update@example.com",
        "name": "Original Name"
    }
    create_response = await client.post("/users/", json=user_data)
    user_id = create_response.json()["id"]
    
    update_data = {
        "name": "Updated Name"
    }
    response = await client.put(f"/users/{user_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == update_data["name"]
    assert data["email"] == user_data["email"]


async def test_update_user_not_found(client: AsyncClient):
    update_data = {
        "name": "Updated Name"
    }
    response = await client.put("/users/999999", json=update_data)
    assert response.status_code == 404


async def test_delete_user(client: AsyncClient):
    user_data = {
        "email": "delete@example.com",
        "name": "Delete User"
    }
    create_response = await client.post("/users/", json=user_data)
    user_id = create_response.json()["id"]
    
    response = await client.delete(f"/users/{user_id}")
    assert response.status_code == 204
    
    get_response = await client.get(f"/users/{user_id}")
    assert get_response.status_code == 404


async def test_delete_user_not_found(client: AsyncClient):
    response = await client.delete("/users/999999")
    assert response.status_code == 404

