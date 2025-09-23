# app/utils/user_manager.py

from app.crud.user_manager import UserManager
from app.database.base.database_manager import DatabaseManager
from app.config import settings

async def get_user_manager() -> UserManager: # type: ignore
    db_manager = DatabaseManager(settings.dp_type)
    await db_manager.connect()
    try:
        yield UserManager(db_manager)
    finally:
        await db_manager.disconnect()
