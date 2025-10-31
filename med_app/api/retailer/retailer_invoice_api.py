from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Query
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from ...schemas.retailer.retailer_invoice_schema import RetailerInvoiceCreateModel, RetailerInvoiceReadModel
from ...crud.retailer.retailer_invoice_manager import RetailerInvoiceManager
from ...utils.get_db_manager import get_retailer_invoice_manager
from ...exceptions.custom_exceptions import NotFoundException

router = APIRouter(prefix="/retailer", tags=["Retailer Invoices"])


# 🧾 Create new invoice
@router.post("/invoice")
async def create_invoice(
    data: RetailerInvoiceCreateModel,
    manager: RetailerInvoiceManager = Depends(get_retailer_invoice_manager),
):
    try:
        return await manager.create_invoice(data)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 🔍 Get invoice by ID
@router.get("/invoice/{invoice_id}")
async def get_invoice(
    invoice_id: int,
    manager: RetailerInvoiceManager = Depends(get_retailer_invoice_manager),
):
    try:
        return await manager.get_invoice_by_id(invoice_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 📋 List invoices (by retailer and optional customer)
@router.get("/invoices")
async def list_invoices(
    retailer_id: int = Query(...),
    customer_id: Optional[int] = Query(None),
    manager: RetailerInvoiceManager = Depends(get_retailer_invoice_manager),
):
    try:
        return await manager.list_invoices(retailer_id, customer_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 📄 Upload document for OCR extraction
@router.post("/upload-document")
async def upload_document(
    file: UploadFile = File(...),
    manager: RetailerInvoiceManager = Depends(get_retailer_invoice_manager),
):
    try:
        return await manager.upload_document(file)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")
