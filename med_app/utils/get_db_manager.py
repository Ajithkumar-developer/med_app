# from fastapi import Depends
# from med_backend.app.dependencies import get_manager

# from med_backend.app.crud.auth_manager import AuthManager
# from med_backend.app.crud.cart_manager import CartManager
# from med_backend.app.crud.distributor_order_manager import DistributorOrderManager
# from med_backend.app.crud.inventory_manager import InventoryManager
# from med_backend.app.crud.medicine_manager import MedicineManager
# from med_backend.app.crud.order_manager import OrderManager
# from med_backend.app.crud.retailer_order_manager import RetailerOrderManager


# async def get_auth_manager():
#     async with get_manager(AuthManager) as manager:
#         yield manager

# async def get_cart_manager():
#     async with get_manager(CartManager) as manager:
#         yield manager

# async def get_distributor_order_manager():
#     async with get_manager(DistributorOrderManager) as manager:
#         yield manager

# async def get_inventory_manager():
#     async with get_manager(InventoryManager) as manager:
#         yield manager

# async def get_medicine_manager():
#     async with get_manager(MedicineManager) as manager:
#         yield manager

# async def get_order_manager():
#     async with get_manager(OrderManager) as manager:
#         yield manager

# async def get_retailer_order_manager():
#     async with get_manager(RetailerOrderManager) as manager:
#         yield manager


from ..db.base.database_manager import DatabaseManager
from ..config import settings
from ..crud.customer.customer_manager import CustomerManager
from ..crud.retailer.retailer_manager import RetailerManager
from ..crud.distributor.distributor_manager import DistributorManager
from ..crud.customer.medicine_manager import MedicineManager
from ..crud.customer.order_manager import OrderManager
from ..crud.retailer.retailer_medicine_manager import RetailerMedicineManager
from ..crud.distributor.distributor_stock_manager import DistributorStockManager
from ..crud.distributor.distributor_order_manager import DistributorOrderManager
from ..crud.retailer.retailer_order_manager import RetailerOrderManager
from ..crud.retailer.retailer_report_manager import RetailerReportManager
from ..crud.retailer.retailer_invoice_manager import RetailerInvoiceManager
from ..crud.distributor.distributor_report_manager import DistributorReportManager
from ..crud.distributor.distributor_invoice_manager import DistributorInvoiceManager

async def get_customer_manager() -> CustomerManager:  # type: ignore
    db_manager = DatabaseManager(settings.dp_type)
    await db_manager.connect()
    try:
        yield CustomerManager(db_manager)
    finally:
        await db_manager.disconnect()

async def get_retailer_manager() -> RetailerManager:  # type: ignore
    db_manager = DatabaseManager(settings.dp_type)
    await db_manager.connect()
    try:
        yield RetailerManager(db_manager)
    finally:
        await db_manager.disconnect()


async def get_distributor_manager() -> DistributorManager:  # type: ignore
    db_manager = DatabaseManager(settings.dp_type)
    await db_manager.connect()
    try:
        yield DistributorManager(db_manager)
    finally:
        await db_manager.disconnect()


async def get_medicine_manager() -> MedicineManager:  # type: ignore
    db_manager = DatabaseManager(settings.dp_type)
    await db_manager.connect()
    try:
        yield MedicineManager(db_manager)
    finally:
        await db_manager.disconnect()


async def get_order_manager() -> OrderManager:  # type: ignore
    db_manager = DatabaseManager(settings.dp_type)
    await db_manager.connect()
    try:
        yield OrderManager(db_manager)
    finally:
        await db_manager.disconnect()


async def get_retailer_medicine_manager() -> RetailerMedicineManager:  # type: ignore
    db_manager = DatabaseManager(settings.dp_type)
    await db_manager.connect()
    try:
        yield RetailerMedicineManager(db_manager)
    finally:
        await db_manager.disconnect()


async def get_distributor_stock_manager() -> DistributorStockManager:  # type: ignore
    db_manager = DatabaseManager(settings.dp_type)
    await db_manager.connect()
    try:
        yield DistributorStockManager(db_manager)
    finally:
        await db_manager.disconnect()


async def get_distributor_order_manager() -> DistributorOrderManager:  # type: ignore
    db_manager = DatabaseManager(settings.dp_type)
    await db_manager.connect()
    try:
        yield DistributorOrderManager(db_manager)
    finally:
        await db_manager.disconnect()

async def get_retailer_order_manager() -> RetailerOrderManager:  # type: ignore
    db_manager = DatabaseManager(settings.dp_type)
    await db_manager.connect()
    try:
        yield RetailerOrderManager(db_manager)
    finally:
        await db_manager.disconnect()

async def get_retailer_report_manager() -> RetailerReportManager:  # type: ignore
    db_manager = DatabaseManager(settings.dp_type)
    await db_manager.connect()
    try:
        yield RetailerReportManager(db_manager)
    finally:
        await db_manager.disconnect()
        
async def get_distributor_report_manager() -> DistributorReportManager:  # type: ignore
    db_manager = DatabaseManager(settings.dp_type)
    await db_manager.connect()
    try:
        yield DistributorReportManager(db_manager)
    finally:
        await db_manager.disconnect()

async def get_retailer_invoice_manager() -> RetailerInvoiceManager:  # type: ignore
    db_manager = DatabaseManager(settings.dp_type)
    await db_manager.connect()
    try:
        yield RetailerInvoiceManager(db_manager)
    finally:
        await db_manager.disconnect()

async def get_distributor_invoice_manager() -> DistributorInvoiceManager:  # type: ignore
    db_manager = DatabaseManager(settings.dp_type)
    await db_manager.connect()
    try:
        yield DistributorInvoiceManager(db_manager)
    finally:
        await db_manager.disconnect()