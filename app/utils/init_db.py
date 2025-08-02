from app.core.database import engine, SessionLocal, Base
from sqlmodel import SQLModel

def create_table():
    SQLModel.metadata.create_all(bind=engine)