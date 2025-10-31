from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from ...crud.distributor.distributor_report_manager import DistributorReportManager
from ...utils.get_db_manager import get_distributor_report_manager
from ...exceptions.custom_exceptions import NotFoundException

router = APIRouter(prefix="/distributor-dashboard", tags=["Distributor Dashboard & Reports"])


# 🏠 Dashboard Summary
@router.get("/summary")
async def get_dashboard_summary(
    distributor_id: int = Query(..., description="Distributor ID to fetch dashboard summary for"),
    manager: DistributorReportManager = Depends(get_distributor_report_manager),
):
    try:
        return await manager.get_dashboard_summary(distributor_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 💰 Sales Analytics (daily/monthly)
@router.get("/reports/sales")
async def get_sales_report(
    distributor_id: int = Query(..., description="Distributor ID"),
    period: str = Query("daily", description="Report period: 'daily' or 'monthly'"),
    manager: DistributorReportManager = Depends(get_distributor_report_manager),
):
    try:
        return await manager.get_sales_report(distributor_id, period)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 📦 Orders Analytics
@router.get("/reports/orders")
async def get_orders_report(
    distributor_id: int = Query(..., description="Distributor ID"),
    manager: DistributorReportManager = Depends(get_distributor_report_manager),
):
    try:
        return await manager.get_orders_report(distributor_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 💊 Product Performance
@router.get("/reports/products")
async def get_product_report(
    distributor_id: int = Query(..., description="Distributor ID"),
    manager: DistributorReportManager = Depends(get_distributor_report_manager),
):
    try:
        return await manager.get_product_report(distributor_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 📁 Exportable Reports (CSV/PDF)
@router.get("/reports/export")
async def export_report(
    distributor_id: int = Query(..., description="Distributor ID"),
    report_type: str = Query("sales", description="Type of report: sales, orders, or products"),
    format: str = Query("csv", description="Export format: csv or pdf"),
    manager: DistributorReportManager = Depends(get_distributor_report_manager),
):
    try:
        result = await manager.export_report(distributor_id, report_type, format)
        return result
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")
