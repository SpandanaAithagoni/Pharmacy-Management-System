from typing import Optional, List, Dict
from config import get_supabase


class MedicineDAO:

    def __init__(self):
        self.sb = get_supabase()
        self.table = "medicine0"

    def create_medicine(
        self,
        name: str,
        sku: str,
        price: float,
        stock: int = 0,
        expiry_date: Optional[str] = None,
        category: Optional[str] = None
    ) -> Optional[Dict]:

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

        self.sb.table(self.table).insert(
            payload
        ).execute()

        resp = (
            self.sb.table(self.table)
            .select("*")
            .eq("sku", sku)
            .limit(1)
            .execute()
        )

        return resp.data[0] if resp.data else None

    def get_medicine_by_id(
        self,
        med_id: int
    ) -> Optional[Dict]:

        resp = (
            self.sb.table(self.table)
            .select("*")
            .eq("med_id", med_id)
            .limit(1)
            .execute()
        )

        return resp.data[0] if resp.data else None

    def get_medicine_by_sku(
        self,
        sku: str
    ) -> Optional[Dict]:

        resp = (
            self.sb.table(self.table)
            .select("*")
            .eq("sku", sku)
            .limit(1)
            .execute()
        )

        return resp.data[0] if resp.data else None

    def update_medicine(
        self,
        med_id: int,
        fields: Dict
    ) -> Optional[Dict]:

        self.sb.table(self.table).update(
            fields
        ).eq(
            "med_id",
            med_id
        ).execute()

        return self.get_medicine_by_id(
            med_id
        )

    def delete_medicine(
        self,
        med_id: int
    ) -> Optional[Dict]:

        medicine = self.get_medicine_by_id(
            med_id
        )

        if not medicine:
            return None

        self.sb.table(self.table).delete().eq(
            "med_id",
            med_id
        ).execute()

        return medicine

    def list_medicines(
        self,
        limit: int = 100,
        category: Optional[str] = None
    ) -> List[Dict]:

        query = (
            self.sb.table(self.table)
            .select("*")
            .order("med_id")
            .limit(limit)
        )

        if category:
            query = query.eq(
                "category",
                category
            )

        resp = query.execute()

        return resp.data or []
