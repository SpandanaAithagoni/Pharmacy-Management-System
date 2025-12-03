# src/dao/medicine_dao.py
from typing import Optional, List, Dict
from src.config import get_supabase

class MedicineDAO:
    def __init__(self):
        self.sb = get_supabase()

    def create_medicine(self, name: str, sku: str, price: float, stock: int = 0,
                        expiry_date: str | None = None, category: str | None = None) -> Optional[Dict]:
        payload = {
            "name": name,
            "sku": sku,
            "price": price,
            "stock": stock
        }
        if expiry_date:
            payload["expiry_date"] = expiry_date
        if category:
            payload["category"] = category

        self.sb.table("medicine0").insert(payload).execute()
        resp = self.sb.table("medicine0").select("*").eq("sku", sku).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_medicine_by_id(self, med_id: int) -> Optional[Dict]:
        resp = self.sb.table("medicine0").select("*").eq("med_id", med_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_medicine_by_sku(self, sku: str) -> Optional[Dict]:
        resp = self.sb.table("medicine0").select("*").eq("sku", sku).limit(1).execute()
        return resp.data[0] if resp.data else None

    def update_medicine(self, med_id: int, fields: Dict) -> Optional[Dict]:
        self.sb.table("medicine0").update(fields).eq("med_id", med_id).execute()
        resp = self.sb.table("medicine0").select("*").eq("med_id", med_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def delete_medicine(self, med_id: int) -> Optional[Dict]:
        resp_before = self.sb.table("medicine0").select("*").eq("med_id", med_id).limit(1).execute()
        row = resp_before.data[0] if resp_before.data else None
        if row:
            self.sb.table("medicine0").delete().eq("med_id", med_id).execute()
        return row

    def list_medicines(self, limit: int = 100, category: str | None = None) -> List[Dict]:
        q = self.sb.table("medicine0").select("*").order("med_id", desc=False).limit(limit)
        if category:
            q = q.eq("category", category)
        resp = q.execute()
        return resp.data or []
