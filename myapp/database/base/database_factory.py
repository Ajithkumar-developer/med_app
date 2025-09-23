# app/database/base/database_factory.py

from app.config import settings
from app.database.sql.postgres_database import PostgresDatabase
from app.database.sql.mysql_database import MySQLDatabase
from app.database.sql.sql_database import SQLiteDatabase
from app.database.base.idatabase import IDatabase


def get_database(db_type: str) -> IDatabase:
    db_type = db_type.lower()
    if db_type == "postgresql":
        return PostgresDatabase(settings.postgresql_url)
    elif db_type == "mysql":
        return MySQLDatabase(settings.mysql_url)
    elif db_type == "sqlite":
        return SQLiteDatabase(settings.sqlite_url)
    else:
        raise ValueError(f"Unsupported database type: {db_type}")




