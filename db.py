"""
Database connection setup — Changed 2026-05-09
===============================================
Reads DATABASE_URL from environment (.env file).
  Supabase: postgresql://postgres.[ref]:[pass]@aws-....pooler.supabase.com:6543/postgres
  Local:    sqlite:///crm.db  (fallback when no env var set)
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

load_dotenv()  # Reads .env file automatically

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///crm.db")

# pg8000 needs postgresql+pg8000:// prefix instead of postgresql://
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+pg8000://", 1)

# SQLite needs check_same_thread; Postgres needs pool_pre_ping
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=5)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()