from sqlmodel import Field, Session, SQLModel, create_engine, select

class ToDoBase(SQLModel):
    task_title: str = Field(index=True)
    completed: bool = Field(default=False, index=True)


class ToDoDB(ToDoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class ToDoCreate(ToDoBase):
    pass
    

class ToDoUpdate(ToDoBase):
    task_title: str | None = None
    completed: bool | None = None
    