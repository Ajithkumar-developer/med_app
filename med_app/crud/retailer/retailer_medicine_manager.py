from typing import List, Optional
from sqlalchemy import select
from ...models.retailer.retailer_medicine_model import RetailerMedicineDbModel
from ...schemas.retailer.retailer_medicine_schema import (
    RetailerMedicineCreateModel,
    RetailerMedicineUpdateModel,
)
from ...db.base.database_manager import DatabaseManager
from ...exceptions.custom_exceptions import NotFoundException
from ...utils.logger import get_logger

logger = get_logger(__name__)


class RetailerMedicineManager:
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager

    # 🧾 Create new product
    async def create_product(self, data: RetailerMedicineCreateModel) -> RetailerMedicineDbModel:
        logger.info(f"Creating new retailer medicine for retailer {data.retailer_id}")
        try:
            created = await self.database_manager.create(RetailerMedicineDbModel, data.dict())
            logger.info(f"Product created successfully (ID: {created.retailer_medicine_id})")
            return created
        except Exception:
            logger.exception("Error creating retailer product.")
            raise

    # 📋 List products with optional search, filter, sort, and by retailer
    async def list_products(
        self,
        retailer_id: int,
        search: Optional[str] = None,
        category: Optional[str] = None,
        sort_by: Optional[str] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> List[RetailerMedicineDbModel]:
        logger.info(f"Fetching products for retailer {retailer_id}")
        try:
            filters = {"retailer_id": retailer_id}
            if category:
                filters["category"] = category

            products = await self.database_manager.read(RetailerMedicineDbModel, filters=filters)

            # Apply search filter
            if search:
                products = [p for p in products if search.lower() in p.name.lower()]

            # Apply sorting
            if sort_by == "price":
                products.sort(key=lambda x: x.price)
            elif sort_by == "expiry":
                products.sort(key=lambda x: x.expiry_date)

            return products[skip: skip + limit]
        except Exception:
            logger.exception("Error fetching products list.")
            raise

    # 🔍 Get product by ID (ensure it belongs to retailer)
    async def get_product_by_id(self, retailer_id: int, product_id: int) -> RetailerMedicineDbModel:
        logger.info(f"Fetching retailer {retailer_id} product ID: {product_id}")
        result = await self.database_manager.read(
            RetailerMedicineDbModel,
            filters={"retailer_medicine_id": product_id, "retailer_id": retailer_id},
        )
        if not result:
            raise NotFoundException(f"Product ID {product_id} not found for this retailer.")
        return result[0]

    # ✏️ Update product details
    async def update_product(
        self, retailer_id: int, product_id: int, update_data: RetailerMedicineUpdateModel
    ) -> RetailerMedicineDbModel:
        logger.info(f"Updating product ID: {product_id} for retailer {retailer_id}")
        updates = update_data.dict(exclude_unset=True)
        await self.get_product_by_id(retailer_id, product_id)
        await self.database_manager.update(
            RetailerMedicineDbModel,
            filters={"retailer_medicine_id": product_id, "retailer_id": retailer_id},
            updates=updates,
        )
        return await self.get_product_by_id(retailer_id, product_id)

    # 🗑️ Delete product
    async def delete_product(self, retailer_id: int, product_id: int) -> bool:
        logger.info(f"Deleting product ID: {product_id} for retailer {retailer_id}")
        await self.get_product_by_id(retailer_id, product_id)
        await self.database_manager.delete(
            RetailerMedicineDbModel, filters={"retailer_medicine_id": product_id, "retailer_id": retailer_id}
        )
        return True

    # 📦 Update stock quantity
    async def update_stock(self, retailer_id: int, product_id: int, quantity: int) -> RetailerMedicineDbModel:
        logger.info(f"Updating stock for product ID: {product_id}, retailer {retailer_id}")
        await self.get_product_by_id(retailer_id, product_id)
        await self.database_manager.update(
            RetailerMedicineDbModel,
            filters={"retailer_medicine_id": product_id, "retailer_id": retailer_id},
            updates={"quantity": quantity},
        )
        return await self.get_product_by_id(retailer_id, product_id)

    # ⚠️ Low stock products
    async def get_low_stock_products(self, retailer_id: int, threshold: int = 10):
        products = await self.database_manager.read(
            RetailerMedicineDbModel, filters={"retailer_id": retailer_id}
        )
        return [p for p in products if hasattr(p, "quantity") and 0 < p.quantity < threshold]

    # ❌ No stock products
    async def get_no_stock_products(self, retailer_id: int):
        products = await self.database_manager.read(
            RetailerMedicineDbModel, filters={"retailer_id": retailer_id}
        )
        return [p for p in products if hasattr(p, "quantity") and p.quantity == 0]
