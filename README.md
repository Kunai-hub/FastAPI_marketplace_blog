# FastAPI Marketplace Blog API

API-сервис для блога на основе **FastAPI + SQLAlchemy (async)** с поддержкой:
- JWT-аутентификации (через cookie);
- управления пользователями;
- CRUD-операций с категориями и постами;
- поиска по тексту (PostgreSQL full-text search);
- загрузки изображений через S3 presigned URLs;
- архивации удалённых постов.

---

## Установка и запуск

```
# Настрой переменные окружения
cp .env.example .env
# Укажи DATABASE_URL, S3_ACCESS_KEY, S3_SECRET_KEY и т.д.

# Запусти в Docker
docker-compose up --build

# Открой Swagger UI
http://localhost:8000/docs
```
| Категория      | Эндпоинт             | Метод  | Описание                               | Авторизация |
| -------------- | -------------------- | ------ | -------------------------------------- | ----------- |
| **Auth**       | `/auth/register`     | POST   | Регистрация пользователя               | ❌           |
|                | `/auth/login`        | POST   | Логин, установка access/refresh cookie | ❌           |
|                | `/auth/logout`       | POST   | Выход (очистка cookie)                 | ✅           |
| **Categories** | `/categories/create` | POST   | Создание категории                     | ✅           |
|                | `/categories/`       | GET    | Получение списка категорий             | ❌           |
| **Posts**      | `/posts/create`      | POST   | Создание поста                         | ✅           |
|                | `/posts/`            | GET    | Получение списка постов                | ❌           |
|                | `/posts/{post_id}`   | PUT    | Обновление поста                       | ✅           |
|                | `/posts/{post_id}`   | DELETE | Удаление поста (в архив)               | ✅           |
| **Images**     | `/image/presigned`   | GET    | Получить presigned URL для загрузки    | ✅           |

### Аутентификация

Авторизация реализована через JWT-токены в HTTP-only cookies:

access_token — действует короткое время;

refresh_token — долгоживущий (несколько дней).

Пример cookie-ответа:
```json
{
  "message": "authenticated"
}
```
### Примеры запросов и ответов

#### Регистрация пользователя

POST `/auth/register`
```json
{
  "email": "user@example.com",
  "password": "strongpassword123"
}
```
Ответ:
```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true,
  "created_at": "2025-10-22T12:34:56.789Z"
}
```
#### Вход (login)

POST `/auth/login`
```json
{
  "email": "user@example.com",
  "password": "strongpassword123"
}
```
Ответ:
```json
{
  "message": "authenticated"
}
```
`После успешного входа токены access_token и refresh_token сохраняются в cookies.`
#### Выход (logout)

POST `/auth/logout`
Ответ:
```json
{
  "message": "successfully logged out"
}
```
#### Создание категории

POST `/categories/create`
```json
{
  "name": "Tech News"
}
```
Ответ:
```json
{
  "id": 1,
  "name": "Tech News",
  "slug": "tech-news",
  "created_at": "2025-10-22T12:00:00.000Z"
}
```
#### Получение списка категорий

GET `/categories/`
Ответ:
```json
[
  {
    "id": 1,
    "name": "Tech News",
    "slug": "tech-news",
    "created_at": "2025-10-22T12:00:00.000Z"
  },
  {
    "id": 2,
    "name": "Lifestyle",
    "slug": "lifestyle",
    "created_at": "2025-10-23T08:30:00.000Z"
  }
]
```
#### Создание поста

POST `/posts/create`
```json
{
  "title": "AI Revolution in 2025",
  "text": "Artificial intelligence is changing everything...",
  "category_id": 1,
  "image": "posts/abc123_ai.jpg"
}
```
Ответ:
```json
{
  "id": 1,
  "title": "AI Revolution in 2025",
  "text": "Artificial intelligence is changing everything...",
  "category": {
    "id": 1,
    "name": "Tech News",
    "slug": "tech-news",
    "created_at": "2025-10-22T12:00:00.000Z"
  },
  "image": "posts/abc123_ai.jpg",
  "created_at": "2025-10-23T10:12:00.000Z",
  "updated_at": "2025-10-23T10:12:00.000Z"
}
```
#### Получение постов (с фильтрацией и поиском)

GET `/posts/?search=ai&category_id=1&page_number=1&page_size=10`
Ответ:
```json
[
  {
    "id": 1,
    "title": "AI Revolution in 2025",
    "text": "Artificial intelligence is changing everything...",
    "category": {
      "id": 1,
      "name": "Tech News",
      "slug": "tech-news",
      "created_at": "2025-10-22T12:00:00.000Z"
    },
    "image": "posts/abc123_ai.jpg",
    "created_at": "2025-10-23T10:12:00.000Z",
    "updated_at": "2025-10-23T10:12:00.000Z"
  }
]
```
#### Обновление поста

PUT `/posts/1`
```json
{
  "title": "AI Revolution in 2025 — Updated",
  "text": "Now with even more insight!"
}
```
Ответ:
```json
{
  "id": 1,
  "title": "AI Revolution in 2025 — Updated",
  "text": "Now with even more insight!",
  "category": {
    "id": 1,
    "name": "Tech News",
    "slug": "tech-news",
    "created_at": "2025-10-22T12:00:00.000Z"
  },
  "image": "posts/abc123_ai.jpg",
  "created_at": "2025-10-23T10:12:00.000Z",
  "updated_at": "2025-10-23T11:45:00.000Z"
}
```
#### Удаление поста (перенос в архив)

DELETE `/posts/1`
Ответ:
```json
{
  "id": 1,
  "title": "AI Revolution in 2025 — Updated",
  "text": "Now with even more insight!",
  "category": {
    "id": 1,
    "name": "Tech News",
    "slug": "tech-news",
    "created_at": "2025-10-22T12:00:00.000Z"
  },
  "image": "posts/abc123_ai.jpg",
  "created_at": "2025-10-23T10:12:00.000Z",
  "updated_at": "2025-10-23T11:45:00.000Z"
}
```
`Пост удаляется из основной таблицы и сохраняется в posts_archive.`
#### Получение presigned URL для загрузки изображения

GET `/image/presigned?filename=photo.jpg`
Ответ:
```json
{
  "upload_url": "https://your-bucket.s3.amazonaws.com/...signature...",
  "object_key": "posts/4f1a9b23c5a44b9f9f_photo.jpg",
  "file_url": "posts/4f1a9b23c5a44b9f9f_photo.jpg"
}
```
`Загружай файл напрямую в S3 по upload_url.
Сохраняй file_url как image при создании поста.`
### Tехнологии

🐍 FastAPI

🗄️ PostgreSQL + SQLAlchemy (async)

🔒 JWT Authentication (cookies)

☁️ S3 file storage

⚙️ Celery + RabbitMQ (отправка email)
