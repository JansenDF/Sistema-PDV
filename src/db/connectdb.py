from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from decouple import config

DATABASE_URL = config("DB_URL")

# Cria engine uma vez só
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Cria fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependência para FastAPI
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
