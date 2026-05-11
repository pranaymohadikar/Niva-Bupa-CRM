# # """
# # Database connection setup — Changed 2026-05-09
# # ===============================================
# # Reads DATABASE_URL from environment (.env file).
# #   Supabase: postgresql://postgres.[ref]:[pass]@aws-....pooler.supabase.com:6543/postgres
# #   Local:    sqlite:///crm.db  (fallback when no env var set)
# # """

# # import os
# # from dotenv import load_dotenv
# # from sqlalchemy import create_engine
# # from sqlalchemy.orm import sessionmaker, Session

# # load_dotenv()  # Reads .env file automatically

# # DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///crm.db")

# # # pg8000 needs postgresql+pg8000:// prefix instead of postgresql://
# # if DATABASE_URL.startswith("postgresql://"):
# #     DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+pg8000://", 1)

# # # SQLite needs check_same_thread; Postgres needs pool_pre_ping
# # if DATABASE_URL.startswith("sqlite"):
# #     engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# # else:
# #     engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=5)

# # SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# # def get_db():
# #     db = SessionLocal()
# #     try:
# #         yield db
# #     finally:
# #         db.close()



# """
# Database connection setup — Changed 2026-05-09
# ===============================================
# Reads DATABASE_URL from environment (.env file).
#   Supabase: postgresql://postgres.[ref]:[pass]@aws-....pooler.supabase.com:6543/postgres
#   Local:    sqlite:///crm.db  (fallback when no env var set)
# """
# """
# Database connection setup — Changed 2026-05-09
# ===============================================
# Reads DATABASE_URL from environment (.env file).
#   Supabase: postgresql://postgres.[ref]:[pass]@aws-....pooler.supabase.com:6543/postgres
#   Local:    sqlite:///crm.db  (fallback when no env var set)
# """

# # import os
# # from urllib.parse import urlparse, unquote
# # from dotenv import load_dotenv
# # from sqlalchemy import create_engine
# # from sqlalchemy.orm import sessionmaker, Session

# # load_dotenv()

# # DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///crm.db")

# # if DATABASE_URL.startswith("sqlite"):
# #     engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# # else:
# #     # Parse URL manually and pass params directly to pg8000 via creator
# #     # This avoids all URL encoding issues with dots in username and @ in password
# #     parsed = urlparse(DATABASE_URL)
# #     _pg_user = unquote(parsed.username) if parsed.username else "postgres"
# #     _pg_pass = unquote(parsed.password) if parsed.password else ""
# #     _pg_host = parsed.hostname
# #     _pg_port = parsed.port or 5432
# #     _pg_db = parsed.path.lstrip("/") or "postgres"

# #     def _pg8000_creator():
# #         import pg8000
# #         return pg8000.connect(
# #             user=_pg_user,
# #             password=_pg_pass,
# #             host=_pg_host,
# #             port=_pg_port,
# #             database=_pg_db,
# #         )

# #     engine = create_engine("postgresql+pg8000://", creator=_pg8000_creator,
# #                            pool_pre_ping=True, pool_size=5)

# # SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# # def get_db():
# #     db = SessionLocal()
# #     try:
# #         yield db
# #     finally:
# #         db.close()


# """
# Database connection setup — Changed 2026-05-09
# ===============================================
# Reads DATABASE_URL from environment (.env file).
#   Supabase: postgresql://postgres.[ref]:[pass]@aws-....pooler.supabase.com:6543/postgres
#   Local:    sqlite:///crm.db  (fallback when no env var set)
# """

# import os
# import ssl
# from urllib.parse import urlparse, unquote
# from dotenv import load_dotenv
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, Session
# import pg8000

# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///crm.db")

# if DATABASE_URL.startswith("sqlite"):
#     engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# else:
#     # Parse URL and connect via pg8000 with explicit params + SSL
#     parsed = urlparse(DATABASE_URL)
#     _pg_user = unquote(parsed.username) if parsed.username else "postgres"
#     _pg_pass = unquote(parsed.password) if parsed.password else ""
#     _pg_host = parsed.hostname
#     _pg_port = parsed.port or 5432
#     _pg_db = (parsed.path or "/postgres").lstrip("/") or "postgres"

#     # Supabase requires SSL
#     _ssl_context = ssl.create_default_context()
#     _ssl_context.check_hostname = False
#     _ssl_context.verify_mode = ssl.CERT_NONE

#     def _pg8000_creator():
#         #import pg8000
#         return pg8000.connect(
#             user=_pg_user,
#             password=_pg_pass,
#             host=_pg_host,
#             port=_pg_port,
#             database=_pg_db,
#             ssl_context=_ssl_context,
#         )

#     engine = create_engine("postgresql+pg8000://", creator=_pg8000_creator,
#                            pool_pre_ping=True, pool_size=5)

# SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


"""
Database connection setup — Changed 2026-05-09
"""

import os
import ssl
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Supabase direct connection
_pg_user = "postgres.gatmlcmknckaiqdabkae"
_pg_pass = "Sincemybirth@94"
_pg_host = "aws-1-ap-northeast-1.pooler.supabase.com"
_pg_port = 6543
_pg_db = "postgres"

_ssl_context = ssl.create_default_context()
_ssl_context.check_hostname = False
_ssl_context.verify_mode = ssl.CERT_NONE

def _pg8000_creator():
    import pg8000
    return pg8000.connect(
        user=_pg_user,
        password=_pg_pass,
        host=_pg_host,
        port=_pg_port,
        database=_pg_db,
        ssl_context=_ssl_context,
    )

DATABASE_URL = "postgresql+pg8000://"
engine = create_engine(DATABASE_URL, creator=_pg8000_creator,
                       pool_pre_ping=True, pool_size=5)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()