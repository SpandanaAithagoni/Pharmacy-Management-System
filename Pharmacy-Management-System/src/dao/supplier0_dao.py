from typing import Optional, Dict, List
from config import get_supabase


class SupplierDAO:

    def __init__(self):
        self.sb = get_supabase()
        self.table = "supplier0"

    def create_supplier(
        self,
        name: str,
        contact: Optional[str] = None,
        address: Optional[str] = None
    ) -> Dict:

        payload = {
            "name": name,
            "contact": contact,
            "address": address
        }

        resp = (
            self.sb.table(self.table)
            .insert(payload)
            .execute()
        )

        return resp.data[0] if resp.data else {}

    def get_supplier(
        self,
        supplier_id: int
    ) -> Optional[Dict]:

        resp = (
            self.sb.table(self.table)
            .select("*")
            .eq("supplier_id", supplier_id)
            .limit(1)
            .execute()
        )

        return resp.data[0] if resp.data else None

    def list_suppliers(
        self
    ) -> List[Dict]:

        resp = (
            self.sb.table(self.table)
            .select("*")
            .order("supplier_id")
            .execute()
        )

        return resp.data or []

    def update_supplier(
        self,
        supplier_id: int,
        fields: Dict
    ) -> Optional[Dict]:

        fields = {
            k: v
            for k, v in fields.items()
            if v is not None
        }

        if not fields:
            return self.get_supplier(
                supplier_id
            )

        self.sb.table(
            self.table
        ).update(
            fields
        ).eq(
            "supplier_id",
            supplier_id
        ).execute()

        return self.get_supplier(
            supplier_id
        )

    def delete_supplier(
        self,
        supplier_id: int
    ) -> Optional[Dict]:

        supplier = self.get_supplier(
            supplier_id
        )

        if not supplier:
            return None

        self.sb.table(
            self.table
        ).delete().eq(
            "supplier_id",
            supplier_id
        ).execute()

        return supplier
