from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Query
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from ...schemas.distributor.distributor_invoice_schema import DistributorInvoiceCreateModel, DistributorInvoiceReadModel
from ...crud.distributor.distributor_invoice_manager import DistributorInvoiceManager
from ...utils.get_db_manager import get_distributor_invoice_manager
from ...exceptions.custom_exceptions import NotFoundException

router = APIRouter(prefix="/distributor", tags=["Distributor Invoices"])


# 🧾 Create new distributor invoice
@router.post("/invoice", response_model=DistributorInvoiceReadModel)
async def create_invoice(
    data: DistributorInvoiceCreateModel,
    manager: DistributorInvoiceManager = Depends(get_distributor_invoice_manager),
):
    try:
        return await manager.create_invoice(data)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 🔍 Get invoice by ID
@router.get("/invoice/{invoice_id}", response_model=DistributorInvoiceReadModel)
async def get_invoice(
    invoice_id: int,
    manager: DistributorInvoiceManager = Depends(get_distributor_invoice_manager),
):
    try:
        return await manager.get_invoice_by_id(invoice_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 📋 List invoices (by distributor and optional retailer)
@router.get("/invoices", response_model=List[DistributorInvoiceReadModel])
async def list_invoices(
    distributor_id: int = Query(...),
    retailer_id: Optional[int] = Query(None),
    manager: DistributorInvoiceManager = Depends(get_distributor_invoice_manager),
):
    try:
        return await manager.list_invoices(distributor_id, retailer_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 📄 Upload document for OCR extraction
@router.post("/upload-document")
async def upload_document(
    file: UploadFile = File(...),
    manager: DistributorInvoiceManager = Depends(get_distributor_invoice_manager),
):
    try:
        return await manager.upload_document(file)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")
