import pytest


@pytest.mark.asyncio
async def test_not_auth(client):
    r = await client.get("/posts/")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_success_auth(client):
    await client.post(
        "/auth/register", json={"email": "u1@example.com", "password": "pass123"}
    )

    r = await client.post(
        "/auth/login", json={"email": "u1@example.com", "password": "pass123"}
    )
    assert r.status_code == 200

    answer = r.json()
    assert answer == {"message": "authenticated"}

    cookies = r.cookies
    r2 = await client.get("/posts/", cookies=cookies)
    assert r2.status_code == 200


@pytest.mark.asyncio
async def test_logout(client):
    await client.post(
        "/auth/register", json={"email": "u1@example.com", "password": "pass123"}
    )

    r = await client.post(
        "/auth/login", json={"email": "u1@example.com", "password": "pass123"}
    )
    assert r.status_code == 200

    r2 = await client.post("/auth/logout")
    assert r2.status_code == 200

    answer = r2.json()
    assert answer == {"message": "successfully logged out"}


@pytest.mark.asyncio
async def test_register_with_some_email(client):
    await client.post(
        "/auth/register", json={"email": "u1@example.com", "password": "pass123"}
    )
    r = await client.post(
        "/auth/register", json={"email": "u1@example.com", "password": "pass123"}
    )
    assert r.status_code == 409

    answer = r.json()
    assert answer == {"detail": "Email already exists"}
