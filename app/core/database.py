from sqlmodel import create_engine, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text
import os
from dotenv import load_dotenv
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Charger les variables d'environnement
load_dotenv()

def create_database_engine():
    """Créer l'engine de base de données Supabase uniquement"""
    SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")
    if not SUPABASE_DB_URL:
        raise RuntimeError("SUPABASE_DB_URL n'est pas défini dans l'environnement !")
    logger.info("🔍 Tentative de connexion à Supabase...")
    engine = create_engine(
        SUPABASE_DB_URL,
        pool_pre_ping=True,
        connect_args={"connect_timeout": 10}
    )
    # Tester la connexion
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    logger.info("✅ Connexion Supabase réussie!")
    return engine, "postgresql"

# Créer l'engine
engine, db_type = create_database_engine()

def SessionLocal():
    return Session(engine)

Base = declarative_base()