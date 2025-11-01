import pytest


@pytest.mark.asyncio
async def test_tokens(client):
    r = await client.post(
        "/auth/register", json={"email": "tokenuser@example.com", "password": "pass123"}
    )
    assert r.status_code == 200

    r2 = await client.post(
        "/auth/login", json={"email": "tokenuser@example.com", "password": "pass123"}
    )
    assert r2.status_code == 200
    assert "access_token" in r2.cookies
    assert "refresh_token" in r2.cookies

    access = r2.cookies.get("access_token")
    refresh = r2.cookies.get("refresh_token")
    headers = {"cookie": f"refresh_token={refresh}; access_token={access}"}
    r3 = await client.get("/posts/", headers=headers)
    assert r3.status_code == 200
