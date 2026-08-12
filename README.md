# Task Manager - Python + PostgreSQL

A small Task Manager API demonstrating database integration, schema design, and CRUD.

## Features

- PostgreSQL-backed `users` and `tasks`
- One-to-many relationship: one user → many tasks
- Full CRUD REST API with FastAPI
- Parameterized queries via SQLAlchemy
- Schema constraints: `NOT NULL`, `UNIQUE`, `CHECK`

## Setup

1. Create a virtual environment.
2. Install dependencies.
3. Create a PostgreSQL database and set `DATABASE_URL` in `.env`.
4. Run `python migrate.py`.
5. Start the API with `uvicorn main:app --reload`.
