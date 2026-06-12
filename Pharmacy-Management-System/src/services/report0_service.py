from typing import Dict, List

from dao import report0_dao as report_dao
from dao import order0_dao as order_dao
from dao import medicine0_dao as medicine_dao


class ReportError(Exception):
    pass


class ReportService:

    def __init__(self):
        self.dao = report_dao.ReportDAO()
        self.order_dao = order_dao.OrderDAO()
        self.medicine_dao = medicine_dao.MedicineDAO()

    def generate_sales_report(
        self
    ) -> Dict:

        orders = self.order_dao.list_orders()

        total_sales = sum(
            order.get("total_amount", 0)
            for order in orders
        )

        details = {
            "total_sales": total_sales,
            "order_count": len(orders),
            "orders": orders
        }

        return self.dao.create_report(
            "SALES",
            details
        )

    def generate_stock_report(
        self
    ) -> Dict:

        medicines = self.medicine_dao.list_medicines()

        low_stock = [
            medicine
            for medicine in medicines
            if medicine.get("stock", 0) < 10
        ]

        details = {
            "total_medicines": len(medicines),
            "low_stock_count": len(low_stock),
            "low_stock": low_stock
        }

        return self.dao.create_report(
            "STOCK",
            details
        )

    def get_report(
        self,
        report_id: int
    ) -> Dict:

        report = self.dao.get_report(
            report_id
        )

        if not report:
            raise ReportError(
                "Report not found"
            )

        return report

    def list_reports(
        self,
        limit: int = 100
    ) -> List[Dict]:

        return self.dao.list_reports(
            limit
        )

    def delete_report(
        self,
        report_id: int
    ) -> Dict:

        report = self.dao.delete_report(
            report_id
        )

        if not report:
            raise ReportError(
                "Report not found"
            )

        return report
