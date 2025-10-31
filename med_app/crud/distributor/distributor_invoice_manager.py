import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import UploadFile
from ...models.distributor.distributor_invoice_model import DistributorInvoiceDbModel, DistributorInvoiceItemDbModel
from ...schemas.distributor.distributor_invoice_schema import DistributorInvoiceCreateModel
from ...db.base.database_manager import DatabaseManager
from ...exceptions.custom_exceptions import NotFoundException
from ...utils.logger import get_logger

logger = get_logger(__name__)


class DistributorInvoiceManager:
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager

    # 🧾 Create new distributor invoice
    async def create_invoice(self, data: DistributorInvoiceCreateModel):
        logger.info(f"Creating distributor invoice for distributor {data.distributor_id}")
        invoice_number = f"DINV-{uuid.uuid4().hex[:8].upper()}"
        invoice_dict = data.dict(exclude={"items"})
        invoice_dict.update({
            "invoice_number": invoice_number,
            "created_at": datetime.utcnow(),
        })

        invoice = await self.database_manager.create(DistributorInvoiceDbModel, invoice_dict)

        # Create invoice items
        for item in data.items:
            item_dict = item.dict()
            item_dict["invoice_id"] = invoice.invoice_id
            await self.database_manager.create(DistributorInvoiceItemDbModel, item_dict)

        return await self.get_invoice_by_id(invoice.invoice_id)

    # 🔍 Get invoice by ID
    async def get_invoice_by_id(self, invoice_id: int):
        invoice_list = await self.database_manager.read(DistributorInvoiceDbModel, filters={"invoice_id": invoice_id})
        if not invoice_list:
            raise NotFoundException(f"Invoice ID {invoice_id} not found")

        invoice = invoice_list[0]
        items = await self.database_manager.read(DistributorInvoiceItemDbModel, filters={"invoice_id": invoice_id})
        invoice.items = items
        return invoice

    # 📋 List all invoices (with filters)
    async def list_invoices(
        self,
        distributor_id: int,
        retailer_id: Optional[int] = None,
    ) -> List[DistributorInvoiceDbModel]:
        filters = {"distributor_id": distributor_id}
        if retailer_id:
            filters["retailer_id"] = retailer_id

        invoices = await self.database_manager.read(DistributorInvoiceDbModel, filters=filters)
        return invoices

    # 📤 Upload document for OCR extraction
    async def upload_document(self, file: UploadFile):
        logger.info(f"Processing uploaded document for OCR: {file.filename}")
        # Placeholder for OCR extraction
        content = await file.read()
        extracted_text = "Mock OCR extracted text from document"
        return {"filename": file.filename, "extracted_text": extracted_text}
