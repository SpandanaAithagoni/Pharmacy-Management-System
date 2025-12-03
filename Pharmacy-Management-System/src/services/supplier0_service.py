from typing import List, Dict, Optional
from src.dao.supplier0_dao import SupplierDAO

class SupplierError(Exception):
    pass

class SupplierService:
    def __init__(self):
        self.dao = SupplierDAO()

    def add_supplier(self, name: str, contact: Optional[str] = None, address: Optional[str] = None) -> Dict:
        if not name.strip():
            raise SupplierError("Supplier name is required")
        return self.dao.create_supplier(name, contact, address)

    def get_supplier(self, supplier_id: int) -> Dict:
        supplier = self.dao.get_supplier(supplier_id)
        if not supplier:
            raise SupplierError("Supplier not found")
        return supplier

    def list_suppliers(self) -> List[Dict]:
        return self.dao.list_suppliers()

    def update_supplier(self, supplier_id: int, fields: Dict) -> Dict:
        supplier = self.dao.update_supplier(supplier_id, fields)
        if not supplier:
            raise SupplierError("Supplier not found or update failed")
        return supplier

    def delete_supplier(self, supplier_id: int) -> Dict:
        supplier = self.dao.delete_supplier(supplier_id)
        if not supplier:
            raise SupplierError("Supplier not found")
        return supplier
