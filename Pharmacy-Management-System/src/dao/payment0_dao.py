from typing import Optional, Dict, List
from config import get_supabase


class PaymentDAO:

    def __init__(self):
        self.sb = get_supabase()
        self.table = "payment0"

    def create_payment(
        self,
        order_id: int,
        amount: float,
        method: str = "CASH"
    ) -> Optional[Dict]:

        payload = {
            "order_id": order_id,
            "amount": amount,
            "method": method,
            "status": "PAID"
        }

        resp = (
            self.sb.table(self.table)
            .insert(payload)
            .execute()
        )

        return resp.data[0] if resp.data else None

    def refund_payment(
        self,
        payment_id: int
    ) -> Optional[Dict]:

        self.sb.table(
            self.table
        ).update(
            {"status": "REFUNDED"}
        ).eq(
            "payment_id",
            payment_id
        ).execute()

        return self.get_payment(
            payment_id
        )

    def get_payment(
        self,
        payment_id: int
    ) -> Optional[Dict]:

        resp = (
            self.sb.table(self.table)
            .select("*")
            .eq("payment_id", payment_id)
            .limit(1)
            .execute()
        )

        return resp.data[0] if resp.data else None

    def list_payments(
        self,
        limit: int = 100
    ) -> List[Dict]:

        resp = (
            self.sb.table(self.table)
            .select("*")
            .order("payment_id")
            .limit(limit)
            .execute()
        )

        return resp.data or []
