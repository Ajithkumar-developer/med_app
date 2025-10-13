from contextlib import asynccontextmanager
from ..db.base.database_manager import DatabaseManager
from ..config import settings

# Generic manager factory
@asynccontextmanager
async def get_manager(manager_class):
    db_manager = DatabaseManager(settings.dp_type)
    await db_manager.connect()
    try:
        yield manager_class(db_manager)
    finally:
        await db_manager.disconnect()
