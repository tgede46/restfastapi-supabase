from sqlmodel import create_engine, Session
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration Supabase
SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")
if not SUPABASE_DB_URL or "your_password" in SUPABASE_DB_URL:
    # Configuration par défaut pour éviter les erreurs au démarrage
    print("⚠️  ATTENTION: Veuillez configurer SUPABASE_DB_URL dans le fichier .env avec vos vraies clés!")
    # URL temporaire qui ne se connecte pas immédiatement
    SUPABASE_DB_URL = "sqlite:///./temp.db"

DATABASE_URL = SUPABASE_DB_URL

# Configuration de l'engine selon le type de base de données
if DATABASE_URL.startswith("postgresql"):
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
else:
    # Pour SQLite temporaire
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def SessionLocal():
    return Session(engine)

Base = declarative_base()