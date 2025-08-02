from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select
from starlette import status
from app.core.database import SessionLocal
from app.db.models.models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
SECRET_KEY = os.getenv("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class CreateUserResponse(BaseModel):
    message: str
    user_id: str
    user_data: dict

class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    mail: EmailStr
    password: str

class ForgotPasswordRequest(BaseModel):
    mail: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=CreateUserResponse)
def create_user(user: CreateUserRequest, db: db_dependency):
    # Check if user already exists
    statement = select(User).where(User.mail == user.mail)
    existing_user = db.exec(statement).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    hashed_password = bcrypt_context.hash(user.password)
    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        mail=user.mail,
        hashed_password=hashed_password,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        status=1
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return CreateUserResponse(
        message="User created successfully",
        user_id=str(new_user.id),
        user_data={
            "id": str(new_user.id),
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "mail": new_user.mail,
            "created_at": new_user.created_at.isoformat(),
            "updated_at": new_user.updated_at.isoformat(),
            "status": new_user.status
        }
    )


@router.post("/token", response_model=TokenResponse)
async def login(db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends()):
    statement = select(User).where(User.mail == form_data.username)
    user = db.exec(statement).first()
    if not user or not bcrypt_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.mail}, expires_delta=access_token_expires)

    return TokenResponse(access_token=access_token, token_type="bearer")

async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, db: db_dependency):
    statement = select(User).where(User.mail == request.mail)
    user = db.exec(statement).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {"message": "Password reset link sent to your email"}

@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, db: db_dependency):
    try:
        payload = jwt.decode(request.token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    statement = select(User).where(User.mail == username)
    user = db.exec(statement).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.hashed_password = bcrypt_context.hash(request.new_password)
    user.updated_at = datetime.utcnow()
    db.commit()

    return {"message": "Password reset successfully"}