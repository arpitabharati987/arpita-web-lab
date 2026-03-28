# Lab 6 — Backend (FastAPI + SQLAlchemy ORM)

## Project structure

```
backend/
├── app.py          # FastAPI app & all route handlers
├── models.py       # SQLAlchemy ORM models  (users + todos tables)
├── schema.py       # Pydantic request / response models
├── database.py     # Engine, session factory, Base, get_db dependency
└── requirements.txt
```

## Setup & run

```bash
cd lab-6/backend

# 1. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server (auto-creates lab6.db on first run)
uvicorn app:app --reload --port 8000
```

Interactive docs → http://localhost:8000/docs

---

## API Reference

### Auth

| Method | Path        | Body                          | Returns                              |
|--------|-------------|-------------------------------|--------------------------------------|
| POST   | /register   | `{username, password}`        | `{id, username}`                     |
| POST   | /login      | `{username, password}`        | `{message, user_id, username}`       |

### Todos

| Method | Path                   | Body                              | Returns                    |
|--------|------------------------|-----------------------------------|----------------------------|
| GET    | /todos/{user_id}       | —                                 | `[TodoResponse, ...]`      |
| POST   | /todos/{user_id}       | `{text}`                          | `TodoResponse`             |
| PUT    | /todos/{todo_id}       | `{text?, completed?}`             | `TodoResponse`             |
| DELETE | /todos/{todo_id}       | —                                 | 204 No Content             |

---

## Notes
- SQLite database file (`lab6.db`) is created automatically in the `backend/` folder.
- Passwords are stored in plain text — acceptable for a lab, not for production.
- CORS is open (`allow_origins=["*"]`) so your React/HTML frontend can call the API from any origin during development.
