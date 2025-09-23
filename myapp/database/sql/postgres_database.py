# app/database/sql/postgres_database.py

import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.database.base.idatabase import IDatabase

class PostgresDatabase(IDatabase):
    def __init__(self, db_url: str):
        self.db_url = db_url
        self._engine = None
        self._SessionLocal = None
        self._session = None

    async def connect(self):
        if self._engine is None:
            self._engine = create_engine(self.db_url, pool_pre_ping=True)
            self._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)
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
