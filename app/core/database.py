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
    """Créer l'engine de base de données avec fallback"""
    
    # Configuration Supabase
    SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")
    
    # Vérifier si on a une configuration Supabase valide
    if SUPABASE_DB_URL and "root@db.invawhmvexgrntocoylv.supabase.co" in SUPABASE_DB_URL:
        try:
            logger.info("🔍 Tentative de connexion à Supabase...")
            # Essayer de créer l'engine Supabase
            engine = create_engine(
                SUPABASE_DB_URL, 
                pool_pre_ping=True,
                connect_args={"connect_timeout": 10}  # Timeout de 10 secondes
            )
            
            # Tester la connexion
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            logger.info("✅ Connexion Supabase réussie!")
            return engine, "postgresql"
            
        except Exception as e:
            logger.warning(f"⚠️  Échec connexion Supabase: {e}")
            logger.info("🔄 Basculement vers SQLite...")
    
    # Fallback vers SQLite
    logger.info("📁 Utilisation de SQLite pour le développement")
    sqlite_url = "sqlite:///./app/core/dev.db"
    engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})
    return engine, "sqlite"

# Créer l'engine
engine, db_type = create_database_engine()

def SessionLocal():
    return Session(engine)

Base = declarative_base()