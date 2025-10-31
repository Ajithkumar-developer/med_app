from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional, Dict
from ...crud.retailer.retailer_report_manager import RetailerReportManager
from ...utils.get_db_manager import get_retailer_report_manager
from ...exceptions.custom_exceptions import NotFoundException

router = APIRouter(prefix="/dashboard", tags=["Retailer Dashboard & Reports"])


# 🏠 Dashboard Summary
@router.get("/summary")
async def get_dashboard_summary(
    retailer_id: int = Query(..., description="Retailer ID to fetch dashboard summary for"),
    manager: RetailerReportManager = Depends(get_retailer_report_manager),
):
    """
    Fetch retailer dashboard summary:
    - Total Sales
    - Total Orders
    - Sales Change %
    """
    try:
        return await manager.get_dashboard_summary(retailer_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 💰 Sales Analytics (daily/monthly)
@router.get("/reports/sales")
async def get_sales_report(
    retailer_id: int = Query(..., description="Retailer ID"),
    period: str = Query("daily", description="Report period: 'daily' or 'monthly'"),
    manager: RetailerReportManager = Depends(get_retailer_report_manager),
):
    """
    Get sales analytics for a retailer.
    Example: /reports/sales?retailer_id=1&period=monthly
    """
    try:
        return await manager.get_sales_report(retailer_id, period)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 📦 Orders Analytics
@router.get("/reports/orders")
async def get_orders_report(
    retailer_id: int = Query(..., description="Retailer ID"),
    manager: RetailerReportManager = Depends(get_retailer_report_manager),
):
    """
    Get order analytics for a retailer.
    Includes completion rate, cancellation rate, and status breakdown.
    """
    try:
        return await manager.get_orders_report(retailer_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 💊 Product Performance Trends
@router.get("/reports/products")
async def get_product_report(
    retailer_id: int = Query(..., description="Retailer ID"),
    manager: RetailerReportManager = Depends(get_retailer_report_manager),
):
    """
    Get top-performing products for a retailer based on sales and quantity.
    """
    try:
        return await manager.get_product_report(retailer_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 📁 Exportable Reports (CSV or PDF)
@router.get("/reports/export")
async def export_report(
    retailer_id: int = Query(..., description="Retailer ID"),
    report_type: str = Query("sales", description="Type of report: sales, orders, or products"),
    format: str = Query("csv", description="Export format: csv or pdf"),
    manager: RetailerReportManager = Depends(get_retailer_report_manager),
):
    """
    Export retailer reports as CSV or PDF.
    Example:
    /reports/export?retailer_id=1&report_type=sales&format=csv
    """
    try:
        result = await manager.export_report(retailer_id, report_type, format)
        return result
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")
