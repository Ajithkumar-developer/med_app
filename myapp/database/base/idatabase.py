# app/database/base/idatabase.py

from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

class IDatabase(ABC):
    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass

    @abstractmethod
    def get_session(self) -> Session:
        pass
