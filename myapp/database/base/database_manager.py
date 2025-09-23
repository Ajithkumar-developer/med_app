# app/database/base/database_manager.py

from ..base.database_factory import get_database
from ..base.idatabase import IDatabase
from sqlalchemy.orm import Session

class DatabaseManager:
    def __init__(self, db_type: str):
        self.db: IDatabase = get_database(db_type)
        self._session: Session = None

    async def connect(self):
        await self.db.connect()
        self._session = self.db.get_session()  # Should return SQLAlchemy Session

    async def disconnect(self):
        await self.db.disconnect()
        self._session = None

    def get_session(self) -> Session:
        if not self._session:
            raise RuntimeError("Database session not initialized. Did you forget to connect?")
        return self._session
