# src/dao/order0_dao.py
from typing import List, Dict, Optional
from src.config import get_supabase

class OrderDAO:
    def __init__(self):
        self.sb = get_supabase()
        self.orders_table = "order0"
        self.items_table = "order_item0" 

    def create_order(self, cust_id: int, items: List[Dict], total_amount: float) -> Optional[Dict]:
        """
        Create a new order and insert related order items.
        Each item dict must have {"med_id": int, "quantity": int, "price": float}
        """
        if not items:
            print("No items provided for the order.")
            return None

        # Insert order header
        order_payload = {
            "cust_id": cust_id,
            "total_amount": total_amount,
            "status": "PLACED"
        }
        resp = self.sb.table(self.orders_table).insert(order_payload, returning="representation").execute()
        if not resp.data:
            print("Failed to create order header")
            return None

        order = resp.data[0]
        order_id = order.get("order_id")
        if not order_id:
            print("Order ID not found in inserted data:", order)
            return None

        # Insert order items
        valid_items_count = 0
        for item in items:
            if not all(k in item for k in ("med_id", "quantity", "price")):
                print(f"Skipping item with missing keys: {item}")
                continue
            item_payload = {
                "order_id": order_id,
                "med_id": item["med_id"],
                "quantity": item["quantity"],
                "price": item["price"]
            }
            self.sb.table(self.items_table).insert(item_payload).execute()
            valid_items_count += 1

        if valid_items_count == 0:
            self.sb.table(self.orders_table).delete().eq("order_id", order_id).execute()
            print("No valid items to insert; order deleted.")
            return None

        return self.get_order_by_id(order_id)

    def get_order_by_id(self, order_id: int) -> Optional[Dict]:
        resp = self.sb.table(self.orders_table).select("*").eq("order_id", order_id).limit(1).execute()
        if not resp.data:
            return None
        order = resp.data[0]

        # Fetch related items
        items_resp = self.sb.table(self.items_table).select("*").eq("order_id", order_id).execute()
        order["items"] = items_resp.data or []
        return order

    def list_orders(self) -> List[Dict]:
        resp = self.sb.table(self.orders_table).select("*").order("order_id", desc=False).execute()
        orders = resp.data or []

        for order in orders:
            items_resp = self.sb.table(self.items_table).select("*").eq("order_id", order["order_id"]).execute()
            order["items"] = items_resp.data or []

        return orders

    def update_order(self, order_id: int, fields: Dict) -> Optional[Dict]:
        self.sb.table(self.orders_table).update(fields).eq("order_id", order_id).execute()
        return self.get_order_by_id(order_id)

    def delete_order(self, order_id: int) -> Optional[Dict]:
        order = self.get_order_by_id(order_id)
        if not order:
            return None

        self.sb.table(self.items_table).delete().eq("order_id", order_id).execute()
        self.sb.table(self.orders_table).delete().eq("order_id", order_id).execute()
        return order
