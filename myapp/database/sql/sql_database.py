# app/database/sql/sqlite_database.py

import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.database.base.idatabase import IDatabase
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SQLiteDatabase(IDatabase):
    def __init__(self, db_url: str):
        self.db_url = db_url
        self._engine = None
        self._SessionLocal = None
        self._session = None

    async def connect(self):
        # For SQLite sync driver, connect is immediate (no async connection required)
        # But to keep interface consistent, make it async
        if self._engine is None:
            self._engine = create_engine(self.db_url, connect_args={"check_same_thread": False})
            self._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

            # Automatically create tables when connecting
            Base.metadata.create_all(bind=self._engine)
            
        # Create a session instance
        self._session = self._SessionLocal()

    async def disconnect(self):
        if self._session:
            self._session.close()
            self._session = None
        if self._engine:
            self._engine.dispose()
            self._engine = None

    def get_session(self) -> Session:
        if not self._session:
            raise RuntimeError("Session not initialized, call connect() first")
        return self._session
