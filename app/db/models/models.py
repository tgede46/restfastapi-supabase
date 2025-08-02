from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from uuid import UUID, uuid4

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    first_name: str
    last_name: str
    mail: str 
    hashed_password: str = Field(max_length=200)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    status: int = Field(default=1, ge=0, le=1)

    todos: List["Todo"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "select"}
    )


class Todo(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=500)
    is_done: bool = Field(default=False)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    status: int = Field(default=1, ge=0, le=1)

    user: User = Relationship(
        back_populates="todos",
        sa_relationship_kwargs={"lazy": "select"}
    )