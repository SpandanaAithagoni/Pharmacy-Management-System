from typing import Dict, List
from dao import customer0_dao as customer_dao

class CustomerError(Exception):
    pass

class CustomerService:
    def __init__(self):
        self.dao = customer_dao.CustomerDAO()

    def create_customer(
        self,
        name: str,
        email: str,
        phone: str,
        city: str | None = None
    ) -> Dict:

        existing = [
            c
            for c in self.dao.list_customers()
            if c["email"] == email
        ]

        if existing:
            raise CustomerError(
                f"Customer with email '{email}' already exists"
            )

        return self.dao.create_customer(
            name,
            email,
            phone,
            city
        )

    def get_customer(
        self,
        cust_id: int
    ) -> Dict:

        customer = self.dao.get_customer_by_id(
            cust_id
        )

        if not customer:
            raise CustomerError(
                "Customer not found"
            )

        return customer

    def update_customer(
        self,
        cust_id: int,
        phone: str | None = None,
        city: str | None = None
    ) -> Dict:

        fields = {}

        if phone:
            fields["phone"] = phone

        if city:
            fields["city"] = city

        if not fields:
            raise CustomerError(
                "No fields to update"
            )

        return self.dao.update_customer(
            cust_id,
            fields
        )

    def delete_customer(
        self,
        cust_id: int
    ) -> Dict:

        customer = self.dao.delete_customer(
            cust_id
        )

        if not customer:
            raise CustomerError(
                "Customer not found or already deleted"
            )

        return customer

    def list_customers(
        self
    ) -> List[Dict]:

        return self.dao.list_customers()
