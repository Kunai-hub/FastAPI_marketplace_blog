import pytest


@pytest.mark.asyncio
async def test_image(client):
    await client.post(
        "/auth/register", json={"email": "u1@example.com", "password": "pass123"}
    )

    r = await client.post(
        "/auth/login", json={"email": "u1@example.com", "password": "pass123"}
    )
    assert r.status_code == 200

    r2 = await client.get("/image/presigned?filename=test.png")
    assert r2.status_code == 200

    data = r2.json()
    assert "upload_url" in data
    assert "upload_url" in data
    assert "object_key" in data
