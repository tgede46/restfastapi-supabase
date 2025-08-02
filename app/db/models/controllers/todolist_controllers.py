from datetime import datetime
from typing import Annotated, List
from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
from sqlmodel import Session, select
from starlette import status
from app.core.database import SessionLocal
from app.db.models.models import User, Todo
from uuid import UUID

router = APIRouter()

class TodoCreate(BaseModel):
    title: str
    description: str = None
    user_id: str  # Add user_id to the request body

class TodoUpdate(BaseModel):
    title: str = None
    description: str = None
    is_done: bool = None

class TodoResponse(BaseModel):
    id: str
    title: str
    description: str = None
    is_done: bool
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TodoCreateResponse(BaseModel):
    message: str
    todo_data: TodoResponse
    request_data: dict

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post('/todolists', status_code=status.HTTP_201_CREATED, response_model=TodoCreateResponse)
def create_todolist(
    todo_data: TodoCreate, 
    db: db_dependency
):
    # Parse user_id from string to UUID
    try:
        user_id = UUID(todo_data.user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user_id format"
        )
    
    # Verify user exists
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    new_todo = Todo(
        title=todo_data.title,
        description=todo_data.description,
        user_id=user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    todo_response = TodoResponse(
        id=str(new_todo.id),
        title=new_todo.title,
        description=new_todo.description,
        is_done=new_todo.is_done,
        user_id=str(new_todo.user_id),
        created_at=new_todo.created_at,
        updated_at=new_todo.updated_at
    )

    return TodoCreateResponse(
        message="Todo created successfully",
        todo_data=todo_response,
        request_data={
            "sent_title": todo_data.title,
            "sent_description": todo_data.description,
            "sent_user_id": todo_data.user_id,
            "user_info": {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.mail
            }
        }
    )

@router.get('/todolists', response_model=List[TodoResponse])
def get_todos(db: db_dependency):
    statement = select(Todo)
    todos = db.exec(statement).all()
    return [
        TodoResponse(
            id=str(todo.id),
            title=todo.title,
            description=todo.description,
            is_done=todo.is_done,
            user_id=str(todo.user_id),
            created_at=todo.created_at,
            updated_at=todo.updated_at
        ) for todo in todos
    ]

@router.get('/todolists/{user_id}', response_model=List[TodoResponse])
def get_user_todos(user_id: UUID, db: db_dependency):
    # Verify user exists
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    statement = select(Todo).where(Todo.user_id == user_id)
    todos = db.exec(statement).all()
    
    return [
        TodoResponse(
            id=str(todo.id),
            title=todo.title,
            description=todo.description,
            is_done=todo.is_done,
            created_at=todo.created_at,
            updated_at=todo.updated_at
        ) for todo in todos
    ]

@router.put('/todolists/{todo_id}', response_model=TodoResponse)
def update_todo(
    todo_id: UUID,
    todo_update: TodoUpdate,
    db: db_dependency
):
    todo = db.get(Todo, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    if todo_update.title is not None:
        todo.title = todo_update.title
    if todo_update.description is not None:
        todo.description = todo_update.description
    if todo_update.is_done is not None:
        todo.is_done = todo_update.is_done
    
    todo.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(todo)
    
    return TodoResponse(
        id=str(todo.id),
        title=todo.title,
        description=todo.description,
        is_done=todo.is_done,
        created_at=todo.created_at,
        updated_at=todo.updated_at
    )

@router.delete('/todolists/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: UUID, db: db_dependency):
    todo = db.get(Todo, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}