# PythonDjangoFlash

Django + Flashcard API — a JSON CRUD API for flashcards, backed by SQLite.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET    | `/api/flash/cards/`            | List all cards |
| GET    | `/api/flash/cards/<id>/`       | Get one card |
| POST   | `/api/flash/cards/create/`      | Create card (`{"question": "...", "answer": "..."}`) |
| PUT    | `/api/flash/cards/<id>/update/` | Update card |
| DELETE | `/api/flash/cards/<id>/update/` | Delete card |

## Run locally

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver 0.0.0.0:8000
```

## Run with Docker

```bash
docker build -t pythondjangoflash .
docker run -p 8000:8000 pythondjangoflash
```

## Tests

```bash
.venv/bin/python manage.py test
```
