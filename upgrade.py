"""
Niva Bupa CRM — Database Upgrade Script — Changed 2026-05-09
=============================================================
Adds new tables and columns to an existing database WITHOUT dropping data.
Works with both SQLite (local) and PostgreSQL (Supabase).
Run this after updating models.py with new features.

Usage:
  python upgrade.py

What it does:
  1. Checks which tables exist
  2. Creates any missing tables
  3. Checks which columns exist in each table
  4. Adds any missing columns
  5. Never drops, deletes, or modifies existing data

Safe to run multiple times — it skips anything that already exists.
"""

import os
from pathlib import Path
from db import engine, DATABASE_URL
from models import Base
from sqlalchemy import inspect, text

IS_POSTGRES = DATABASE_URL.startswith("postgresql")

def upgrade():
    # Connection check
    if not IS_POSTGRES:
        db_path = Path("crm.db")
        if not db_path.exists():
            print("ERROR: crm.db not found. Run migrate.py first for initial setup.")
            return

    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    model_tables = Base.metadata.tables

    db_label = "Supabase (PostgreSQL)" if IS_POSTGRES else f"crm.db ({Path('crm.db').stat().st_size//1024} KB)"

    print("="*50)
    print("  Niva Bupa CRM — Database Upgrade")
    print("="*50)
    print(f"  Database: {db_label}")
    print(f"  Existing tables: {len(existing_tables)}")
    print(f"  Model tables: {len(model_tables)}")
    print()

    changes = 0

    # Step 1: Create missing tables
    for table_name, table in model_tables.items():
        if table_name not in existing_tables:
            print(f"  + Creating table: {table_name}")
            table.create(engine)
            changes += 1
        else:
            # Step 2: Check for missing columns
            existing_cols = {col['name'] for col in inspector.get_columns(table_name)}
            for column in table.columns:
                if column.name not in existing_cols:
                    col_type = str(column.type)
                    nullable = "NULL" if column.nullable else "NOT NULL"
                    default = ""
                    if column.default is not None:
                        try:
                            val = column.default.arg
                            if isinstance(val, bool):
                                default = f" DEFAULT {'true' if IS_POSTGRES else (1 if val else 0)}" if val else f" DEFAULT {'false' if IS_POSTGRES else 0}"
                            elif isinstance(val, (int, float)):
                                default = f" DEFAULT {val}"
                            elif isinstance(val, str):
                                default = f" DEFAULT '{val}'"
                        except:
                            pass

                    # Neither SQLite nor Postgres supports NOT NULL without default on ALTER TABLE for existing rows
                    if nullable == "NOT NULL" and not default:
                        nullable = "NULL"

                    sql = f'ALTER TABLE {table_name} ADD COLUMN {column.name} {col_type} {nullable}{default}'
                    try:
                        with engine.connect() as conn:
                            conn.execute(text(sql))
                            conn.commit()
                        print(f"  + Adding column: {table_name}.{column.name} ({col_type})")
                        changes += 1
                    except Exception as e:
                        err = str(e).lower()
                        # Skip if column already exists (different error messages for SQLite vs Postgres)
                        if "duplicate column" not in err and "already exists" not in err:
                            print(f"  ! Failed to add {table_name}.{column.name}: {e}")

    if changes == 0:
        print("  No changes needed — database is up to date.")
    else:
        print(f"\n  ✓ {changes} changes applied.")

    # Step 3: Summary
    inspector = inspect(engine)
    print(f"\n  Tables now: {len(inspector.get_table_names())}")
    for t in sorted(inspector.get_table_names()):
        cols = len(inspector.get_columns(t))
        print(f"    {t}: {cols} columns")

    print(f"\n  Database: {db_label}")
    print("  Data untouched ✓")
    print("="*50)


if __name__ == "__main__":
    upgrade()