# src/services/medicine_service.py
from typing import List, Dict
import src.dao.medicine0_dao as medicine_dao

class MedicineError(Exception):
    pass

class MedicineService:
    def __init__(self):
        self.dao = medicine_dao.MedicineDAO()

    def add_medicine(self, name: str, sku: str, price: float, stock: int = 0,
                     expiry_date: str | None = None, category: str | None = None) -> Dict:
        if price <= 0:
            raise MedicineError("Price must be greater than 0")
        existing = self.dao.get_medicine_by_sku(sku)
        if existing:
            raise MedicineError(f"Medicine with SKU '{sku}' already exists")
        return self.dao.create_medicine(name, sku, price, stock, expiry_date, category)

    def update_medicine_stock(self, med_id: int, delta: int) -> Dict:
        if delta == 0:
            raise MedicineError("Stock delta cannot be 0")
        med = self.dao.get_medicine_by_id(med_id)
        if not med:
            raise MedicineError("Medicine not found")
        new_stock = (med.get("stock") or 0) + delta
        return self.dao.update_medicine(med_id, {"stock": new_stock})

    def get_medicine(self, med_id: int) -> Dict:
        med = self.dao.get_medicine_by_id(med_id)
        if not med:
            raise MedicineError("Medicine not found")
        return med

    def list_medicines(self, category: str | None = None) -> List[Dict]:
        return self.dao.list_medicines(category=category)

    def delete_medicine(self, med_id: int) -> Dict:
        med = self.dao.delete_medicine(med_id)
        if not med:
            raise MedicineError("Medicine not found or already deleted")
        return med
