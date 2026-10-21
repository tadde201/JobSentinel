# AGENTS.md

## Project overview

JobSentinel is a FastAPI-based job tracking platform with a PostgreSQL-backed backend. The current implementation is centered in the backend package, with schema definitions and database setup under the repository root.

- Product overview: [README.md](README.md)
- Backend package: [backend/app](backend/app)
- Database schema: [database/postgres_schema.sql](database/postgres_schema.sql)
- Environment template: [.env.example](.env.example)

## Repository map

- `backend/app/main.py` is the main FastAPI app and the entry point for API endpoints.
- `backend/app/config.py` loads settings from `.env` using `pydantic-settings`.
- `backend/app/database.py` creates the SQLAlchemy engine and `get_db()` dependency.
- `database/postgres_schema.sql` is the canonical schema reference for the project’s relational model.
- `backend/requirements.txt` lists the installed backend dependencies.
- The frontend directory currently appears empty; do not assume a full frontend stack exists unless a new app is added.

## Working conventions

- Prefer editing within the existing FastAPI + SQLAlchemy structure instead of introducing a different framework.
- Keep business logic in `backend/app` and separate it cleanly into models, schemas, CRUD, and auth utilities.
- `Base.metadata.create_all()` is triggered on app startup in `backend/app/main.py`, so database schema changes should be reflected in both the Python model layer and the SQL schema file when applicable.
- `get_db()` is the standard dependency injection pattern. Preserve it for database access.
- Authentication already uses JWTs and password hashing in the backend auth utilities; follow that pattern when adding authenticated endpoints.
- When environment values are required locally, copy `.env.example` to `.env` and update the database connection values.

## Local development

Run the backend from the repository root or within `backend/`:

```bash
cd backend
python -m pip install -r requirements.txt
python run.py
```

For local debugging, the app can also be started with Uvicorn directly:

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Guidance for AI agents

- Keep changes minimal and consistent with the repo’s existing structure.
- Do not add new frameworks or patterns unless the task explicitly requires them.
- If a task changes data model behavior, check both the SQLAlchemy layer and the schema script before finalizing.
- If the project is extended with frontend or testing code, prefer adding docs and routes that fit the current backend-first architecture.
- When in doubt, use the user-facing project intent in [README.md](README.md) and the backend code in [backend/app/main.py](backend/app/main.py) as the primary source of truth.
