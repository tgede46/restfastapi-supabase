from fastapi import FastAPI
from contextlib import asynccontextmanager
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.utils.init_db import create_table
from app.routes.router import router as v1_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application starting up...")
    try:
        create_table()
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")
    yield
    print("Application shutting down...")


app = FastAPI(
    title="TODOList API",
    description="API for managing TODO lists avec Supabase",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(v1_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)