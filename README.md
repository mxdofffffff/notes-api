# 📝 Notes API

REST API для управления заметками с авторизацией, категориями и фильтрацией.

## Стек

- **FastAPI** — веб-фреймворк
- **PostgreSQL** — база данных
- **SQLAlchemy** — ORM
- **Alembic** — миграции
- **JWT** — аутентификация (access + refresh токены)
- **Docker / docker-compose** — контейнеризация

## Запуск

### Через Docker (рекомендуется)

1. Клонируй репозиторий:
```bash
git clone https://github.com/mxdofffffff/notes-api.git
cd notes-api
```

2. Создай `.env` файл:
```env
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://postgres:postgres@db:5432/notes_db
```

3. Запусти:
```bash
docker-compose up --build
```

4. Примени миграции:
```bash
docker-compose exec web alembic upgrade head
```

5. API доступно по адресу: `http://localhost:8000`
6. Swagger документация: `http://localhost:8000/docs`

## Эндпоинты

### Аутентификация
| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/register` | Регистрация |
| POST | `/token` | Логин, получение access + refresh токенов |
| POST | `/refresh` | Обновление access токена |
| POST | `/logout` | Выход |

### Заметки
| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/notes` | Создать заметку |
| GET | `/notes` | Получить список заметок |
| GET | `/notes/{id}` | Получить заметку по ID |
| PATCH | `/notes/{id}` | Редактировать заметку |
| DELETE | `/notes/{id}` | Удалить заметку (soft delete) |
| POST | `/notes/{id}/restore` | Восстановить удалённую заметку |
| GET | `/notes/deleted` | Список удалённых заметок |

### Категории
| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/categories` | Создать категорию |
| GET | `/categories` | Список категорий |
| GET | `/categories/{id}` | Получить категорию по ID |
| GET | `/categories/{id}/notes` | Заметки внутри категории |
| DELETE | `/categories/{id}` | Удалить категорию |

## Фильтрация заметок

`GET /notes` поддерживает параметры:

| Параметр | Тип | Описание |
|----------|-----|----------|
| `limit` | int | Кол-во заметок (1-100, default: 10) |
| `skip` | int | Смещение для пагинации |
| `search` | string | Поиск по заголовку |
| `sort` | string | Сортировка: `asc` / `desc` |
| `is_favorite` | bool | Только избранные |
| `date_from` | datetime | Фильтр по дате создания (от) |
| `date_to` | datetime | Фильтр по дате создания (до) |

## Тесты

```bash
pytest
```

## Деплой

Проект задеплоен на Railway.

- **API:** https://notes-api-production-066e.up.railway.app
- **Swagger документация:** https://notes-api-production-066e.up.railway.app/docs
- **Telegram бот:** @APINotes_bot

## Архитектура

Проект состоит из трёх сервисов задеплоенных на Railway:

- **notes-api** — FastAPI бэкенд
- **bot** — Telegram бот на aiogram 3.x
- **PostgreSQL** — база данных