```markdown
# 🚀 Blueprint Service

Production-ready FastAPI microservice blueprint using Service Repository Pattern.

## Features

- FastAPI
- Async SQLAlchemy
- PostgreSQL
- Repository Pattern
- Service Pattern
- Dependency Injection
- Pydantic Settings
- Health Check
- Request ID (Coming Soon)
- Structured Logger (Coming Soon)
- Generic Response (Coming Soon)
- Docker Ready (Coming Soon)

---

## Tech Stack

- Python 3.12+ (Compatible with Python 3.14)
- FastAPI
- SQLAlchemy Async
- PostgreSQL
- Pydantic v2
- Alembic
- Uvicorn
- Poetry (Dependency Management)

---

## Project Structure


```

app
├── api
├── config
├── dependencies
├── exceptions
├── middleware
├── models
├── repositories
├── responses
├── schemas
├── services
├── utils
└── main.py

```

---

## Installation

Clone repository

```bash
git clone <repository-url>

cd Blueprint-Service

```

Install dependencies using Poetry

```bash
poetry install

```

*(Opsional: Jika Anda ingin agar folder virtual environment otomatis terbuat di dalam direktori proyek, jalankan `poetry config virtualenvs.in-project true` sebelum melakukan instalasi).*

---

## Environment

Copy

```bash
cp .env.example .env

```

Example

```env
APP_NAME=YearBook Service
APP_DEBUG=true
APP_VERSION=1.0.0

DB_HOST=localhost
DB_PORT=5432
DB_NAME=blueprint_service_db
DB_USER=postgres
DB_PASSWORD=lerd

SECRET_KEY="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

```

---

## Database Migration & Seeding

Jalankan migrasi database menggunakan Alembic:

```bash
poetry run alembic upgrade head

```

Masukkan data awal (*seeding*) ke database:

```bash
poetry run python -m app.scripts.seed

```

---

## Running

Development

```bash
poetry run uvicorn app.main:app --reload

```

Open Swagger

```
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

```

---

## Health Check

```
GET /api/v1/health

```

Response

```json
{
    "status": "UP",
    "database": "UP"
}

```

---

## Architecture

```
Client

↓

Router

↓

Service

↓

Repository

↓

PostgreSQL

```

---

## Coding Rules

### Router

* Handle HTTP Request
* Validation
* Call Service

### Service

* Business Logic

### Repository

* Database Query

### Model

* SQLAlchemy ORM

### Schema

* Request & Response

---

## Roadmap

* [x] FastAPI
* [x] Async SQLAlchemy
* [x] Repository Pattern
* [x] Service Pattern
* [x] Dependency Injection
* [x] Health Check

### Next

* [ ] Structured Logger
* [ ] Request ID Middleware
* [ ] Generic Response
* [ ] Global Exception
* [ ] Base Repository
* [ ] Base Service
* [ ] JWT Authentication
* [ ] Redis
* [ ] Docker
* [ ] GitHub Actions

---

## License

MIT

```

```
