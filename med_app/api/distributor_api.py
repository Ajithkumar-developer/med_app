from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from ..schemas.distributor_schema import (
    DistributorDataCreateModel,
    DistributorDataReadModel,
    DistributorDataUpdateModel,
    DistributorLoginRequest,
    DistributorLoginResponse,
)
from ..crud.distributor_manager import DistributorManager
from ..utils.get_db_manager import get_distributor_manager
from ..exceptions.custom_exceptions import NotFoundException

router = APIRouter(prefix="/distributors", tags=["Distributors"])

@router.post("/", response_model=DistributorDataReadModel)
async def register_distributor(
    distributor: DistributorDataCreateModel,
    manager: DistributorManager = Depends(get_distributor_manager),
):
    try:
        return await manager.create_distributor(distributor)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/login", response_model=DistributorLoginResponse)
async def login_distributor(
    credentials: DistributorLoginRequest,
    manager: DistributorManager = Depends(get_distributor_manager),
):
    try:
        dist = await manager.login(credentials)
        return DistributorLoginResponse(
            distributor_id=dist.distributor_id,
            company_name=dist.company_name,
            email=dist.email,
        )
    except NotFoundException as e:
        raise HTTPException(status_code=401, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")

@router.get("/", response_model=List[DistributorDataReadModel])
async def list_distributors(
    skip: int = 0, limit: int = 10, manager: DistributorManager = Depends(get_distributor_manager)
):
    try:
        return await manager.get_all_distributors(skip, limit)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")

@router.get("/{distributor_id}", response_model=DistributorDataReadModel)
async def get_distributor(
    distributor_id: int, manager: DistributorManager = Depends(get_distributor_manager)
):
    try:
        return await manager.get_distributor_by_id(distributor_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")

@router.put("/{distributor_id}", response_model=DistributorDataReadModel)
async def update_distributor(
    distributor_id: int,
    update_data: DistributorDataUpdateModel,
    manager: DistributorManager = Depends(get_distributor_manager),
):
    try:
        return await manager.update_distributor(distributor_id, update_data)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")

@router.delete("/{distributor_id}")
async def delete_distributor(
    distributor_id: int, manager: DistributorManager = Depends(get_distributor_manager)
):
    try:
        await manager.delete_distributor(distributor_id)
        return {"status": "success", "deleted": True, "distributor_id": distributor_id}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")
