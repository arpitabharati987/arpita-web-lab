from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pathlib import Path
import os

import models
import schema
from database import engine, get_db

# Resolve the frontend directory relative to this file
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"

# Create all tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lab 6 API")

# ── CORS ──────────────────────────────────────────────────────────────────────
# Allow the React dev server (and file:// origins during development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Frontend ──────────────────────────────────────────────────────────────────
# Serve index.html at "/" so the whole app runs from one server
@app.get("/", response_class=FileResponse)
def serve_frontend():
    index = FRONTEND_DIR / "index.html"
    if not index.exists():
        raise HTTPException(status_code=404, detail="Frontend not found.")
    return FileResponse(str(index))

# Serve static assets from the frontend folder
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


# ── Auth Routes ───────────────────────────────────────────────────────────────

@app.post("/register", response_model=schema.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: schema.UserCreate, db: Session = Depends(get_db)):
    """Register a new user (plain-text password for lab purposes)."""
    existing = db.query(models.User).filter(models.User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")

    new_user = models.User(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/login", response_model=schema.LoginResponse)
def login(credentials: schema.UserLogin, db: Session = Depends(get_db)):
    """Authenticate and return user_id so the frontend can scope todo calls."""
    user = db.query(models.User).filter(models.User.username == credentials.username).first()
    if not user or user.password != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return schema.LoginResponse(
        message="Login successful",
        user_id=user.id,
        username=user.username,
    )


# ── Todo Routes ───────────────────────────────────────────────────────────────

@app.get("/todos/{user_id}", response_model=list[schema.TodoResponse])
def get_todos(user_id: int, db: Session = Depends(get_db)):
    """Fetch all todos belonging to a specific user."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return db.query(models.Todo).filter(models.Todo.user_id == user_id).all()


@app.post("/todos/{user_id}", response_model=schema.TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(user_id: int, todo: schema.TodoCreate, db: Session = Depends(get_db)):
    """Add a new todo linked to the given user."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_todo = models.Todo(text=todo.text, completed=False, user_id=user_id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


@app.put("/todos/{todo_id}", response_model=schema.TodoResponse)
def update_todo(todo_id: int, updates: schema.TodoUpdate, db: Session = Depends(get_db)):
    """Toggle completion status and/or edit the text of a todo."""
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    if updates.text is not None:
        todo.text = updates.text
    if updates.completed is not None:
        todo.completed = updates.completed

    db.commit()
    db.refresh(todo)
    return todo


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Remove a todo by its ID."""
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()
