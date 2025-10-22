import pytest


@pytest.mark.asyncio
async def test_categories_create_success(client):
    await client.post(
        "/auth/register", json={"email": "cat@user.ru", "password": "cat123"}
    )
    r = await client.post(
        "/auth/login", json={"email": "cat@user.ru", "password": "cat123"}
    )
    assert r.status_code == 200

    r2 = await client.post("/categories/create", json={"name": "cat1", "slug": "cat-1"})
    assert r2.status_code == 200

    answer = r2.json()
    assert answer["name"] == "cat1"
    assert answer["slug"] == "cat-1"


@pytest.mark.asyncio
async def test_categories_create_with_some_slug(client):
    await client.post(
        "/auth/register", json={"email": "cat@user.ru", "password": "cat123"}
    )
    r = await client.post(
        "/auth/login", json={"email": "cat@user.ru", "password": "cat123"}
    )
    assert r.status_code == 200

    r2 = await client.post("/categories/create", json={"name": "cat1", "slug": "cat-1"})
    assert r2.status_code == 200

    r3 = await client.post("/categories/create", json={"name": "cat1", "slug": "cat-1"})
    assert r3.status_code == 409

    answer = r3.json()
    assert answer == {"detail": "Category already exists"}


@pytest.mark.asyncio
async def test_categories_get_list(client):
    await client.post(
        "/auth/register", json={"email": "cat@user.ru", "password": "cat123"}
    )
    r = await client.post(
        "/auth/login", json={"email": "cat@user.ru", "password": "cat123"}
    )
    assert r.status_code == 200

    r2 = await client.post("/categories/create", json={"name": "cat1", "slug": "cat-1"})
    assert r2.status_code == 200

    r3 = await client.post("/categories/create", json={"name": "cat2", "slug": "cat-2"})
    assert r3.status_code == 200

    r4 = await client.get("/categories/")
    assert r4.status_code == 200

    answer = r4.json()
    assert len(answer) == 2
    assert answer[0]["name"] == "cat2"
    assert answer[1]["name"] == "cat1"
    assert answer[0]["slug"] == "cat-2"
    assert answer[1]["slug"] == "cat-1"
