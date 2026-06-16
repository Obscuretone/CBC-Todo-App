# CBC Todo API

Sanic API for the CBC Todo prototype. It currently contains email/password JWT auth, task CRUD, and Tortoise ORM models backed by MariaDB.

## Local Development

From the repository root:

```bash
cp backend/.env.example backend/.env
docker compose up --build backend database redis
```

Or run it directly:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app/app.py
```

The API listens on `http://localhost:8000`.

## Endpoints

- `POST /auth/register`
- `POST /auth`
- `GET /tasks`
- `POST /tasks`
- `DELETE /tasks/<task_id>`
