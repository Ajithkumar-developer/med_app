from datetime import datetime, timedelta
from typing import Dict, List
import csv
import io
from ...models.retailer.retailer_order_model import RetailerOrderDbModel, RetailerOrderItemDbModel
from ...db.base.database_manager import DatabaseManager
from ...exceptions.custom_exceptions import NotFoundException
from ...utils.logger import get_logger

logger = get_logger(__name__)


class DistributorReportManager:
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager

    # 🏠 Dashboard Summary (Distributor-based)
    async def get_dashboard_summary(self, distributor_id: int) -> Dict:
        logger.info(f"Generating dashboard summary for distributor {distributor_id}...")
        orders = await self.database_manager.read(RetailerOrderDbModel, filters={"distributor_id": distributor_id})

        total_orders = len(orders)
        total_sales = sum(float(o.total_amount or 0) for o in orders)

        # Sales comparison (today vs yesterday)
        today = datetime.utcnow().date()
        yesterday = today - timedelta(days=1)

        today_sales = sum(float(o.total_amount or 0) for o in orders if o.order_date.date() == today)
        yesterday_sales = sum(float(o.total_amount or 0) for o in orders if o.order_date.date() == yesterday)
        sales_change = ((today_sales - yesterday_sales) / yesterday_sales * 100) if yesterday_sales > 0 else 0

        return {
            "distributor_id": distributor_id,
            "total_sales": round(total_sales, 2),
            "total_orders": total_orders,
            "sales_change_percentage": round(sales_change, 2),
        }

    # 💰 Sales Analytics (Distributor-based)
    async def get_sales_report(self, distributor_id: int, period: str = "daily") -> List[Dict]:
        logger.info(f"Generating {period} sales report for distributor {distributor_id}...")
        orders = await self.database_manager.read(RetailerOrderDbModel, filters={"distributor_id": distributor_id})
        report = {}

        for o in orders:
            key = o.order_date.strftime("%Y-%m-%d") if period == "daily" else o.order_date.strftime("%Y-%m")
            report.setdefault(key, 0)
            report[key] += float(o.total_amount or 0)

        return [{"period": k, "sales": round(v, 2)} for k, v in sorted(report.items())]

    # 📦 Orders Analytics (Distributor-based)
    async def get_orders_report(self, distributor_id: int) -> Dict:
        logger.info(f"Generating order analytics for distributor {distributor_id}...")
        orders = await self.database_manager.read(RetailerOrderDbModel, filters={"distributor_id": distributor_id})
        status_count = {}

        for o in orders:
            status_count[o.status.value] = status_count.get(o.status.value, 0) + 1

        total_orders = len(orders)
        completed = status_count.get("Delivered", 0)
        cancelled = status_count.get("Cancelled", 0)

        return {
            "distributor_id": distributor_id,
            "total_orders": total_orders,
            "status_breakdown": status_count,
            "completion_rate": round((completed / total_orders * 100), 2) if total_orders else 0,
            "cancellation_rate": round((cancelled / total_orders * 100), 2) if total_orders else 0,
        }

    # 💊 Product Performance (Distributor-based)
    async def get_product_report(self, distributor_id: int) -> List[Dict]:
        logger.info(f"Generating product performance for distributor {distributor_id}...")

        # Get all orders for this distributor
        orders = await self.database_manager.read(RetailerOrderDbModel, filters={"distributor_id": distributor_id})
        order_ids = [o.order_id for o in orders]
        if not order_ids:
            return []

        # Fetch all order items belonging to these orders
        all_items = []
        for oid in order_ids:
            items = await self.database_manager.read(RetailerOrderItemDbModel, filters={"order_id": oid})
            all_items.extend(items)

        performance = {}
        for item in all_items:
            med_id = item.medicine_id
            if med_id not in performance:
                performance[med_id] = {"medicine_id": med_id, "total_quantity": 0, "total_revenue": 0.0}
            performance[med_id]["total_quantity"] += item.quantity
            performance[med_id]["total_revenue"] += float(item.price or 0) * item.quantity

        return sorted(performance.values(), key=lambda x: x["total_revenue"], reverse=True)

    # 📁 Export Reports (Distributor-based)
    async def export_report(self, distributor_id: int, report_type: str = "sales", format: str = "csv") -> Dict:
        logger.info(f"Exporting {report_type} report for distributor {distributor_id} as {format}")

        if report_type == "sales":
            data = await self.get_sales_report(distributor_id)
        elif report_type == "orders":
            data = await self.get_orders_report(distributor_id)
        elif report_type == "products":
            data = await self.get_product_report(distributor_id)
        else:
            raise NotFoundException("Invalid report type")

        if format == "csv":
            output = io.StringIO()
            if isinstance(data, list) and len(data) > 0:
                keys = data[0].keys()
                writer = csv.DictWriter(output, fieldnames=keys)
                writer.writeheader()
                writer.writerows(data)
            elif isinstance(data, dict):
                writer = csv.writer(output)
                for k, v in data.items():
                    writer.writerow([k, v])
            return {
                "filename": f"{report_type}_report_distributor_{distributor_id}.csv",
                "content": output.getvalue(),
            }

        elif format == "pdf":
            return {
                "filename": f"{report_type}_report_distributor_{distributor_id}.pdf",
                "content": f"PDF report for distributor {distributor_id}",
            }

        else:
            raise NotFoundException("Unsupported export format")
