# CBC Todo App

CBC Todo App is an experimental full-stack task manager. It combines a React frontend, a Sanic API, MariaDB persistence, Redis-ready configuration, JWT authentication, and architecture notes for a larger cloud deployment.

## Repository Layout

- `frontend/` - React app built with Vite.
- `backend/` - Sanic API using Tortoise ORM and JWT auth.
- `database/` - MariaDB Docker image init hook.
- `swagger/` - OpenAPI draft.
- `docs/architecture/` - original CBC requirements, Draw.io diagrams, sequence notes, and archived Azure deployment drafts.

## Local Setup

Start the full stack:

```bash
docker compose up --build
```

Default local URLs:

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- MariaDB: `127.0.0.1:3307`
- Redis: `127.0.0.1:6380`

The UI lets you create an account, log in, create tasks, list tasks, and complete tasks. The backend stores users and tasks in MariaDB.

If port 3000 is already in use, start the frontend on another host port:

```bash
FRONTEND_PORT=3002 docker compose up --build
```

## Direct Backend Setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app/app.py
```

## API Endpoints

- `GET /`
- `POST /auth/register`
- `POST /auth`
- `GET /tasks`
- `POST /tasks`
- `DELETE /tasks/<task_id>`

## Notes

The app is intentionally small, but it should be runnable from a fresh clone. The architecture folder preserves the larger cloud design ideas separately from the working local implementation.

## Continuous integration

CI builds the frontend from its lockfile, checks backend dependency compatibility,
and tests authentication, task CRUD, and cross-user isolation over the real HTTP
API with a temporary MariaDB service. It also validates the local Compose config.
It does not deploy to Azure or require cloud credentials; the old deployment
workflow remains an archived design draft under `docs/architecture/`.

Run the API integration tests locally with an isolated in-memory SQLite database:

```bash
python -m pip install -r backend/requirements.txt
python -m unittest discover -s backend/tests -v
```

Set `TEST_DATABASE_URL` only to a disposable test database to exercise MariaDB
locally. The tests create users and tasks; they do not use the app's normal
`DATABASE_URL`.
