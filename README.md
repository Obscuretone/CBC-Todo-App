# CBC Todo App

CBC Todo App is an experimental enterprise-style task manager. It combines a React frontend, a Sanic API, MariaDB storage, Redis cache plumbing, Azure AD sign-in experiments, and architecture notes for a larger Azure deployment.

## Repository Layout

- `frontend/` - React app created with Create React App.
- `backend/` - Sanic API using Tortoise ORM and JWT auth.
- `database/` - MariaDB Docker image seed/init SQL.
- `swagger/` - OpenAPI draft.
- `docs/architecture/` - original CBC requirements, Draw.io diagrams, and sequence notes.
- `.github/workflows/` - Azure container build/deploy workflow draft.

## Local Setup

Copy the environment templates:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

Start the stack:

```bash
docker compose up --build
```

Default local URLs:

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- MariaDB: `127.0.0.1:3307`
- Redis: `127.0.0.1:6380`

## Current State

The app currently supports the basic skeleton for auth and task CRUD, but auth is not fully reconciled: the frontend uses Azure/MSAL while the backend currently expects app-issued JWTs. Treat this repo as a prototype plus architecture archive, not production-ready software.
