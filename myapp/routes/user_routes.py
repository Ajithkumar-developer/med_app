from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.user_schema import UserCreate, UserRead, UserUpdate
from app.crud.user_manager import UserManager
from app.utils.user_manager import get_user_manager
from app.exceptions.custom_exceptions import UserAlreadyExistsException, UserNotFoundException

router = APIRouter()

@router.post("/users", response_model=UserRead)
def create_user(user: UserCreate, user_manager: UserManager = Depends(get_user_manager)):
    try:
        return user_manager.create_user(user)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/users", response_model=list[UserRead])
def list_users(skip: int = 0, limit: int = 10, user_manager: UserManager = Depends(get_user_manager)):
    try:
        return user_manager.get_users(skip, limit)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, user_manager: UserManager = Depends(get_user_manager)):
    try:
        return user_manager.get_user(user_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_update: UserUpdate, user_manager: UserManager = Depends(get_user_manager)):
    try:
        return user_manager.update_user(user_id, user_update)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/users/{user_id}")
def delete_user(user_id: int, user_manager: UserManager = Depends(get_user_manager)):
    try:
        user_manager.delete_user(user_id)
        return {"deleted": True}
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
