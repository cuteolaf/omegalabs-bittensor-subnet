from validator_api import config
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.schema import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

DB_HOST = config.FOCUS_DB_HOST
DB_NAME = config.FOCUS_DB_NAME
DB_USER = config.FOCUS_DB_USER
DB_PASSWORD = config.FOCUS_DB_PASSWORD
DB_PORT = config.FOCUS_DB_PORT

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = None
if config.FOCUS_DB_NULL_POOL:
    PG_DATABASE_URL_POOLER = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(
        PG_DATABASE_URL_POOLER,
        poolclass=NullPool,
    )
else:
    PG_DATABASE_URL_STANDARD = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(
        PG_DATABASE_URL_STANDARD,
        pool_size=20,  # bumped up from default of 5
        max_overflow=30,  # bumped up from default of 10
        pool_timeout=30,  # default of 30
        pool_pre_ping=True,  # Good practice for most scenarios
        pool_recycle=3600,  # Recycle connections after 1 hour
    )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
metadata = MetaData()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_context():
    return contextmanager(get_db)()
