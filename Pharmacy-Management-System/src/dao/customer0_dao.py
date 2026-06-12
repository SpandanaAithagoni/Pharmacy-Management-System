# src/dao/customer0_dao.py
from typing import Optional, Dict, List
from config import get_supabase

class CustomerDAO:
    def __init__(self):
        self.sb = get_supabase()

    def create_customer(self, name: str, email: str, phone: str, city: str | None = None) -> Optional[Dict]:
        payload = {"name": name, "email": email, "phone": phone}
        if city:
            payload["city"] = city

        self.sb.table("customer0").insert(payload).execute()

        resp = self.sb.table("customer0").select("*").eq("email", email).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_customer_by_id(self, cust_id: int) -> Optional[Dict]:
        resp = self.sb.table("customer0").select("*").eq("cust_id", cust_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def update_customer(self, cust_id: int, fields: Dict) -> Optional[Dict]:
        self.sb.table("customer0").update(fields).eq("cust_id", cust_id).execute()
        resp = self.sb.table("customer0").select("*").eq("cust_id", cust_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def delete_customer(self, cust_id: int) -> Optional[Dict]:
        resp_before = self.sb.table("customer0").select("*").eq("cust_id", cust_id).limit(1).execute()
        row = resp_before.data[0] if resp_before.data else None
        self.sb.table("customer0").delete().eq("cust_id", cust_id).execute()
        return row

    def list_customers(self, limit: int = 100) -> List[Dict]:
        resp = self.sb.table("customer0").select("*").order("cust_id", desc=False).limit(limit).execute()
        return resp.data or []
