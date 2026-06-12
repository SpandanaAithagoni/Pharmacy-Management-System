from typing import List, Dict, Optional

from dao import order0_dao as order_dao
from dao import medicine0_dao as medicine_dao


class OrderError(Exception):
    pass


class OrderService:

    def __init__(self):
        self.order_dao = order_dao.OrderDAO()
        self.medicine_dao = medicine_dao.MedicineDAO()

    def create_order(
        self,
        cust_id: int,
        items: List[Dict]
    ) -> Optional[Dict]:

        if not items:
            raise OrderError(
                "No items provided for the order."
            )

        order_items = []
        total_amount = 0

        for item in items:

            if (
                not isinstance(item, dict)
                or "med_id" not in item
                or "quantity" not in item
            ):
                continue

            med_id = item["med_id"]
            qty = item["quantity"]

            med = self.medicine_dao.get_medicine_by_id(
                med_id
            )

            if not med:
                raise OrderError(
                    f"Medicine ID {med_id} not found"
                )

            if med.get("stock", 0) < qty:
                raise OrderError(
                    f"Not enough stock for {med['name']}"
                )

            price = med["price"]

            total_amount += price * qty

            order_items.append(
                {
                    "med_id": med_id,
                    "quantity": qty,
                    "price": price
                }
            )

        if not order_items:
            raise OrderError(
                "No valid items to create order."
            )

        for item in order_items:

            med = self.medicine_dao.get_medicine_by_id(
                item["med_id"]
            )

            new_stock = (
                med.get("stock", 0)
                - item["quantity"]
            )

            self.medicine_dao.update_medicine(
                item["med_id"],
                {"stock": new_stock}
            )

        return self.order_dao.create_order(
            cust_id,
            order_items,
            total_amount
        )

    def get_order(
        self,
        order_id: int
    ) -> Dict:

        order = self.order_dao.get_order_by_id(
            order_id
        )

        if not order:
            raise OrderError(
                "Order not found"
            )

        return order

    def cancel_order(
        self,
        order_id: int
    ) -> Dict:

        order = self.get_order(
            order_id
        )

        if order.get("status") != "PLACED":
            raise OrderError(
                "Only PLACED orders can be cancelled"
            )

        for item in order.get("items", []):

            med = self.medicine_dao.get_medicine_by_id(
                item["med_id"]
            )

            new_stock = (
                med.get("stock", 0)
                + item["quantity"]
            )

            self.medicine_dao.update_medicine(
                item["med_id"],
                {"stock": new_stock}
            )

        return self.order_dao.update_order(
            order_id,
            {"status": "CANCELLED"}
        )

    def complete_order(
        self,
        order_id: int
    ) -> Dict:

        order = self.get_order(
            order_id
        )

        if order.get("status") != "PLACED":
            raise OrderError(
                "Only PLACED orders can be completed"
            )

        return self.order_dao.update_order(
            order_id,
            {"status": "COMPLETED"}
        )

    def list_orders(
        self
    ) -> List[Dict]:

        return self.order_dao.list_orders()
