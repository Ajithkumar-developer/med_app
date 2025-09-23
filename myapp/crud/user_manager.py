from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate
from app.database.base.database_manager import DatabaseManager
from app.exceptions.custom_exceptions import UserNotFoundException, UserAlreadyExistsException
from app.utils.logger import get_logger

logger = get_logger(__name__)

class UserManager:
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager
        self.db: Session = self.database_manager.get_session()

    def create_user(self, user: UserCreate) -> User:
        logger.info(f"Creating user with email: {user.email}")
        try:
            existing_user = self.db.query(User).filter(User.email == user.email).first()
            if existing_user:
                logger.warning(f"User with email {user.email} already exists.")
                raise UserAlreadyExistsException(f"User with email {user.email} already exists.")
            
            db_user = User(**user.dict())
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            logger.info(f"User created successfully: {db_user.id}")
            return db_user
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Integrity error creating user: {e}")
            raise UserAlreadyExistsException("User already exists.")
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.exception("Database error during user creation.")
            raise

    def get_users(self, skip: int = 0, limit: int = 10) -> List[User]:
        logger.info(f"Fetching users: skip={skip}, limit={limit}")
        try:
            return self.db.query(User).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            logger.exception("Error fetching users.")
            raise

    def get_user(self, user_id: int) -> User:
        logger.info(f"Fetching user with ID: {user_id}")
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                logger.warning(f"User ID {user_id} not found.")
                raise UserNotFoundException(f"User ID {user_id} not found.")
            return user
        except SQLAlchemyError as e:
            logger.exception("Error fetching user.")
            raise

    def delete_user(self, user_id: int) -> bool:
        logger.info(f"Deleting user with ID: {user_id}")
        try:
            user = self.get_user(user_id)
            self.db.delete(user)
            self.db.commit()
            logger.info(f"User {user_id} deleted.")
            return True
        except UserNotFoundException:
            raise
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.exception("Error deleting user.")
            raise

    def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        logger.info(f"Updating user with ID: {user_id}")
        try:
            user = self.get_user(user_id)
            update_data = user_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(user, key, value)
            self.db.commit()
            self.db.refresh(user)
            logger.info(f"User {user_id} updated.")
            return user
        except UserNotFoundException:
            raise
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.exception("Error updating user.")
            raise
