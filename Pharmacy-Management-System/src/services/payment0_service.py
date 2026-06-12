from typing import Dict, List

from dao import payment0_dao as payment_dao
from dao import order0_dao as order_dao


class PaymentError(Exception):
    pass


class PaymentService:

    def __init__(self):
        self.dao = payment_dao.PaymentDAO()
        self.order_dao = order_dao.OrderDAO()

    def make_payment(
        self,
        order_id: int,
        method: str = "CASH"
    ) -> Dict:

        order = self.order_dao.get_order_by_id(
            order_id
        )

        if not order:
            raise PaymentError(
                "Order not found"
            )

        if order.get("status") != "PLACED":
            raise PaymentError(
                "Payment can only be made for PLACED orders"
            )

        payment = self.dao.create_payment(
            order_id,
            order["total_amount"],
            method
        )

        self.order_dao.update_order(
            order_id,
            {"status": "COMPLETED"}
        )

        return payment

    def refund_payment(
        self,
        payment_id: int
    ) -> Dict:

        payment = self.dao.get_payment(
            payment_id
        )

        if not payment:
            raise PaymentError(
                "Payment not found"
            )

        if payment.get("status") != "PAID":
            raise PaymentError(
                "Only PAID payments can be refunded"
            )

        refunded = self.dao.refund_payment(
            payment_id
        )

        order_id = refunded.get(
            "order_id"
        )

        self.order_dao.update_order(
            order_id,
            {"status": "CANCELLED"}
        )

        return refunded

    def get_payment(
        self,
        payment_id: int
    ) -> Dict:

        payment = self.dao.get_payment(
            payment_id
        )

        if not payment:
            raise PaymentError(
                "Payment not found"
            )

        return payment

    def list_payments(
        self
    ) -> List[Dict]:

        return self.dao.list_payments()
