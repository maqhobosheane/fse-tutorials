from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from starlette import status
from sqlmodel import Session, SQLModel, create_engine, select
from models import ToDoBase, ToDoDB, ToDoCreate, ToDoUpdate

from db import create_db_and_tables, SessionDep


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/todo/", response_model=ToDoDB, status_code=status.HTTP_201_CREATED)
def create_task(todo: ToDoCreate, session: SessionDep):
    db_todo = ToDoDB.model_validate(todo)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@app.get("/todo/", response_model=list[ToDoDB])
def read_tasks(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    tasks = session.exec(select(ToDoDB).offset(offset).limit(limit)).all()
    return tasks


@app.get("/todo/{task_id}", response_model=ToDoDB)
def read_hero(hero_id: int, session: SessionDep):
    task = session.get(ToDoDB, hero_id)
    if not task:
        raise HTTPException(status_code=404, detail="Hero not found")
    return task


@app.patch("/todo/{task_id}", response_model=ToDoDB)
def update_task(task_id: int, task: ToDoUpdate, session: SessionDep):
    task_db = session.get(ToDoDB, task_id)
    if not task_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    task_data = task.model_dump(exclude_unset=True)
    task_db.sqlmodel_update(task_data)
    session.add(task_db)
    session.commit()
    session.refresh(task_db)
    return task_db


@app.delete("/todo/{task_id}")
def delete_task(task_id: int, session: SessionDep):
    task = session.get(ToDoDB, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(task)
    session.commit()
    return {"ok": True}
