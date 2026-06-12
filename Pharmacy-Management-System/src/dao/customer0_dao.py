from typing import Optional, Dict, List
from config import get_supabase


class CustomerDAO:

    def __init__(self):
        self.sb = get_supabase()
        self.table = "customer0"

    def create_customer(
        self,
        name: str,
        email: str,
        phone: str,
        city: Optional[str] = None
    ) -> Optional[Dict]:

        payload = {
            "name": name,
            "email": email,
            "phone": phone
        }

        if city:
            payload["city"] = city

        self.sb.table(self.table).insert(
            payload
        ).execute()

        resp = (
            self.sb.table(self.table)
            .select("*")
            .eq("email", email)
            .limit(1)
            .execute()
        )

        return resp.data[0] if resp.data else None

    def get_customer_by_id(
        self,
        cust_id: int
    ) -> Optional[Dict]:

        resp = (
            self.sb.table(self.table)
            .select("*")
            .eq("cust_id", cust_id)
            .limit(1)
            .execute()
        )

        return resp.data[0] if resp.data else None

    def update_customer(
        self,
        cust_id: int,
        fields: Dict
    ) -> Optional[Dict]:

        self.sb.table(self.table).update(
            fields
        ).eq(
            "cust_id",
            cust_id
        ).execute()

        return self.get_customer_by_id(
            cust_id
        )

    def delete_customer(
        self,
        cust_id: int
    ) -> Optional[Dict]:

        customer = self.get_customer_by_id(
            cust_id
        )

        if not customer:
            return None

        self.sb.table(self.table).delete().eq(
            "cust_id",
            cust_id
        ).execute()

        return customer

    def list_customers(
        self,
        limit: int = 100
    ) -> List[Dict]:

        resp = (
            self.sb.table(self.table)
            .select("*")
            .order("cust_id")
            .limit(limit)
            .execute()
        )

        return resp.data or []
