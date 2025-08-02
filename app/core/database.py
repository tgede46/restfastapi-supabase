from sqlmodel import create_engine, Session
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration Supabase avec fallback vers SQLite
SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")

# Si pas de configuration Supabase valide, utiliser SQLite pour le développement
if not SUPABASE_DB_URL or "your_password" in SUPABASE_DB_URL:
    print("⚠️  Configuration Supabase non trouvée, utilisation de SQLite pour le développement")
    DATABASE_URL = "sqlite:///./app/core/dev.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    print("✅ Utilisation de Supabase PostgreSQL")
    DATABASE_URL = SUPABASE_DB_URL
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def SessionLocal():
    return Session(engine)

Base = declarative_base()