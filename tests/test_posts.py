import pytest


@pytest.mark.asyncio
async def test_posts_create_success(client):
    await client.post(
        "/auth/register", json={"email": "post@user.ru", "password": "post123"}
    )
    r = await client.post(
        "/auth/login", json={"email": "post@user.ru", "password": "post123"}
    )
    assert r.status_code == 200

    r2 = await client.post("/categories/create", json={"name": "cat1", "slug": "cat-1"})
    assert r2.status_code == 200

    cat = r2.json()["id"]
    r3 = await client.post(
        "/posts/create",
        json={"title": "Название", "text": "Описание", "category_id": cat},
    )
    assert r3.status_code == 200

    answer = r3.json()
    assert answer["title"] == "Название"
    assert answer["text"] == "Описание"
    assert answer["category"]["name"] == "cat1"
    assert answer["category"]["slug"] == "cat-1"


@pytest.mark.asyncio
async def test_posts_create_with_not_exist_category(client):
    await client.post(
        "/auth/register", json={"email": "post@user.ru", "password": "post123"}
    )
    r = await client.post(
        "/auth/login", json={"email": "post@user.ru", "password": "post123"}
    )
    assert r.status_code == 200

    r2 = await client.post("/categories/create", json={"name": "cat1", "slug": "cat-1"})
    assert r2.status_code == 200

    cat = r2.json()["id"]
    r3 = await client.post(
        "/posts/create",
        json={"title": "Название", "text": "Описание", "category_id": cat + 1},
    )
    assert r3.status_code == 400

    answer = r3.json()
    assert answer == {"detail": "Category does not exist"}


@pytest.mark.asyncio
async def test_posts_get_list(client):
    await client.post(
        "/auth/register", json={"email": "post@user.ru", "password": "post123"}
    )
    r = await client.post(
        "/auth/login", json={"email": "post@user.ru", "password": "post123"}
    )
    assert r.status_code == 200

    r2 = await client.post("/categories/create", json={"name": "cat1", "slug": "cat-1"})
    assert r2.status_code == 200

    cat1 = r2.json()["id"]
    r3 = await client.post(
        "/posts/create",
        json={"title": "Название1", "text": "Описание1", "category_id": cat1},
    )
    assert r3.status_code == 200

    r4 = await client.post("/categories/create", json={"name": "cat2", "slug": "cat-2"})
    assert r4.status_code == 200

    cat2 = r4.json()["id"]
    r5 = await client.post(
        "/posts/create",
        json={"title": "Название2", "text": "Описание2", "category_id": cat2},
    )
    assert r5.status_code == 200

    r6 = await client.get("/posts/")
    assert r6.status_code == 200

    answer = r6.json()
    assert len(answer) == 2

    post1 = answer[1]
    assert post1["title"] == "Название1"
    assert post1["text"] == "Описание1"
    assert post1["category"]["name"] == "cat1"
    assert post1["category"]["slug"] == "cat-1"

    post2 = answer[0]
    assert post2["title"] == "Название2"
    assert post2["text"] == "Описание2"
    assert post2["category"]["name"] == "cat2"
    assert post2["category"]["slug"] == "cat-2"


@pytest.mark.asyncio
async def test_posts_update_success(client):
    await client.post(
        "/auth/register", json={"email": "post@user.ru", "password": "post123"}
    )
    r = await client.post(
        "/auth/login", json={"email": "post@user.ru", "password": "post123"}
    )
    assert r.status_code == 200

    r2 = await client.post("/categories/create", json={"name": "cat1", "slug": "cat-1"})
    assert r2.status_code == 200

    cat = r2.json()["id"]
    r3 = await client.post(
        "/posts/create",
        json={"title": "Название", "text": "Описание", "category_id": cat},
    )
    assert r3.status_code == 200

    post = r3.json()
    assert post["title"] == "Название"
    assert post["text"] == "Описание"

    r4 = await client.put(
        f"/posts/{post['id']}",
        json={"title": "Новое название", "text": "Новое описание"},
    )
    assert r4.status_code == 200

    answer = r4.json()
    assert answer["title"] == "Новое название"
    assert answer["text"] == "Новое описание"


@pytest.mark.asyncio
async def test_posts_update_with_unknown_id(client):
    await client.post(
        "/auth/register", json={"email": "post@user.ru", "password": "post123"}
    )
    r = await client.post(
        "/auth/login", json={"email": "post@user.ru", "password": "post123"}
    )
    assert r.status_code == 200

    r2 = await client.post("/categories/create", json={"name": "cat1", "slug": "cat-1"})
    assert r2.status_code == 200

    cat = r2.json()["id"]
    r3 = await client.post(
        "/posts/create",
        json={"title": "Название", "text": "Описание", "category_id": cat},
    )
    assert r3.status_code == 200

    post = r3.json()
    assert post["title"] == "Название"
    assert post["text"] == "Описание"

    r4 = await client.put(
        f"/posts/{post['id'] + 1}",
        json={"title": "Новое название", "text": "Новое описание"},
    )
    assert r4.status_code == 404

    answer = r4.json()
    assert answer == {"detail": "Post not found"}


@pytest.mark.asyncio
async def test_posts_delete_success(client):
    await client.post(
        "/auth/register", json={"email": "post@user.ru", "password": "post123"}
    )
    r = await client.post(
        "/auth/login", json={"email": "post@user.ru", "password": "post123"}
    )
    assert r.status_code == 200

    r2 = await client.post("/categories/create", json={"name": "cat1", "slug": "cat-1"})
    assert r2.status_code == 200

    cat = r2.json()["id"]
    r3 = await client.post(
        "/posts/create",
        json={"title": "Название", "text": "Описание", "category_id": cat},
    )
    assert r3.status_code == 200

    post = r3.json()
    assert post["title"] == "Название"
    assert post["text"] == "Описание"

    r4 = await client.delete(f"/posts/{post['id']}")
    assert r4.status_code == 200

    answer = r4.json()
    assert answer["title"] == "Название"
    assert answer["text"] == "Описание"
    assert answer["category"]["name"] == "cat1"
    assert answer["category"]["slug"] == "cat-1"


@pytest.mark.asyncio
async def test_posts_delete_with_unknown_id(client):
    await client.post(
        "/auth/register", json={"email": "post@user.ru", "password": "post123"}
    )
    r = await client.post(
        "/auth/login", json={"email": "post@user.ru", "password": "post123"}
    )
    assert r.status_code == 200

    r2 = await client.post("/categories/create", json={"name": "cat1", "slug": "cat-1"})
    assert r2.status_code == 200

    cat = r2.json()["id"]
    r3 = await client.post(
        "/posts/create",
        json={"title": "Название", "text": "Описание", "category_id": cat},
    )
    assert r3.status_code == 200

    post = r3.json()
    assert post["title"] == "Название"
    assert post["text"] == "Описание"

    r4 = await client.delete(f"/posts/{post['id'] + 1}")
    assert r4.status_code == 404

    answer = r4.json()
    assert answer == {"detail": "Post not found"}
