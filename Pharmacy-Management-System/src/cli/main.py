# src/cli/main.py
import json
from src.services.medicine0_service import MedicineService, MedicineError
from src.services.customer0_service import CustomerService, CustomerError
from src.services.order0_service import OrderService, OrderError
from src.services.payment0_service import PaymentService, PaymentError
from src.services.report0_service import ReportService
from src.services.supplier0_service import SupplierService, SupplierError


class PharmacyCLI:
    def __init__(self):
        self.medicine = MedicineService()
        self.customer = CustomerService()
        self.order = OrderService()
        self.payment = PaymentService()
        self.report = ReportService()
        self.supplier = SupplierService()

    def run(self):
        while True:
            print("\n--- Pharmacy System ---")
            print("1. Medicines")
            print("2. Customers")
            print("3. Orders")
            print("4. Payments")
            print("5. Suppliers")
            print("6. Reports")
            print("0. Exit")
            choice = input("Choose an option: ")

            if choice == "1":
                self.medicine_menu()
            elif choice == "2":
                self.customer_menu()
            elif choice == "3":
                self.order_menu()
            elif choice == "4":
                self.payment_menu()
            elif choice == "5":
                self.supplier_menu()
            elif choice == "6":
                self.report_menu()
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid choice, try again.")

    # Medicine Menu 
    def medicine_menu(self):
        print("\n--- Medicine Menu ---")
        print("1. Add Medicine")
        print("2. List Medicines")
        print("3. Update Stock")
        print("4. Delete Medicine")
        print("0. Back")
        choice = input("Choose: ")

        if choice == "1":
            name = input("Medicine Name: ")
            sku = input("SKU: ")
            price = float(input("Price: "))
            stock = int(input("Stock: "))
            expiry = input("Expiry Date (YYYY-MM-DD): ")
            category = input("Category (optional): ") or None
            try:
                med = self.medicine.add_medicine(name, sku, price, stock, expiry, category)
                print("Medicine added:")
                print(json.dumps(med, indent=2))
            except MedicineError as e:
                print("Error:", e)

        elif choice == "2":
            category = input("Filter by category (optional): ") or None
            meds = self.medicine.list_medicines(category)
            print(json.dumps(meds, indent=2))

        elif choice == "3":
            med_id = int(input("Medicine ID: "))
            change = int(input("Stock change (+/-): "))
            try:
                med = self.medicine.update_medicine_stock(med_id, change)
                print("Stock updated:")
                print(json.dumps(med, indent=2))
            except MedicineError as e:
                print("Error:", e)

        elif choice == "4":
            med_id = int(input("Medicine ID to delete: "))
            try:
                med = self.medicine.delete_medicine(med_id)
                print("Medicine deleted:")
                print(json.dumps(med, indent=2))
            except MedicineError as e:
                print("Error:", e)

    # Customer Menu 
    def customer_menu(self):
        print("\n--- Customer Menu ---")
        print("1. Add Customer")
        print("2. List Customers")
        print("3. Update Customer")
        print("4. Delete Customer")
        print("0. Back")
        choice = input("Choose: ")

        if choice == "1":
            name = input("Name: ")
            email = input("Email: ")
            phone = input("Phone: ")
            city = input("City (optional): ") or None
            try:
                cust = self.customer.add_customer(name, email, phone, city)
                print("Customer added:")
                print(json.dumps(cust, indent=2))
            except CustomerError as e:
                print("Error:", e)

        elif choice == "2":
            custs = self.customer.list_customers()
            print(json.dumps(custs, indent=2))

        elif choice == "3":
            cust_id = int(input("Customer ID: "))
            phone = input("New Phone (leave blank to skip): ") or None
            city = input("New City (leave blank to skip): ") or None
            try:
                cust = self.customer.update_customer(cust_id, phone, city)
                print("Customer updated:")
                print(json.dumps(cust, indent=2))
            except CustomerError as e:
                print("Error:", e)

        elif choice == "4":
            cust_id = int(input("Customer ID to delete: "))
            try:
                cust = self.customer.delete_customer(cust_id)
                print("Customer deleted:")
                print(json.dumps(cust, indent=2))
            except CustomerError as e:
                print("Error:", e)

    # Order Menu
    def order_menu(self):
        import json
        print("\n--- Order Menu ---")
        print("1. Create Order")
        print("2. Show Order")
        print("3. Cancel Order")
        print("4. Complete Order")
        print("0. Back")
        choice = input("Choose: ")

        if choice == "1":
        # Create Order
            try:
                customer_id = int(input("Customer ID: "))
            except ValueError:
                print("Invalid Customer ID!")
                return

            items = []
            print("Enter items as med_id:qty, one per line. Empty line to finish.")

            while True:
                line = input("Item: ").strip()
                if not line:
                    break
                try:
                    med_id_str, qty_str = line.split(":")
                    med_id = int(med_id_str)
                    quantity = int(qty_str)
                    if quantity <= 0:
                        print("Quantity must be positive!")
                        continue

                    med = self.order.medicine_dao.get_medicine_by_id(med_id)
                    if not med:
                        print(f"Medicine ID {med_id} not found, skipping.")
                        continue
                    if med.get("stock", 0) < quantity:
                        print(f"Not enough stock for {med['name']}, skipping.")
                        continue

                    price = med["price"]
                    items.append({"med_id": med_id, "quantity": quantity, "price": price})

                except ValueError:
                    print("Wrong format! Please enter as med_id:qty")
                    continue

            if not items:
                print("No valid items entered. Order not created.")
                return

            try:
                order = self.order.create_order(customer_id, items)
                print("Order created successfully:")
                print(json.dumps(order, indent=2))
            except OrderError as e:
                print("Error:", e)

        elif choice == "2":
        # Show Order
            try:
                order_id = int(input("Order ID: "))
                order = self.order.get_order(order_id)
                print(json.dumps(order, indent=2))
            except (ValueError, OrderError) as e:
                print("Error:", e)

        elif choice == "3":
        # Cancel Order
            try:
                order_id = int(input("Order ID to cancel: "))
                order = self.order.cancel_order(order_id)
                print("Order cancelled:")
                print(json.dumps(order, indent=2))
            except (ValueError, OrderError) as e:
                print("Error:", e)

        elif choice == "4":
        # Complete Order
            try:
                order_id = int(input("Order ID to complete: "))
                order = self.order.complete_order(order_id)
                print("Order completed:")
                print(json.dumps(order, indent=2))
            except (ValueError, OrderError) as e:
                print("Error:", e)



# Payment Menu
    def payment_menu(self):
        import json
        print("\n--- Payment Menu ---")
        print("1. Process Payment")
        print("2. Refund Payment")
        print("0. Back")
        choice = input("Choose: ")

        if choice == "1":
            try:
                order_id = int(input("Order ID: "))
                method = input("Payment Method (Cash/Card/UPI): ").strip()
                pay = self.payment.make_payment(order_id, method)
                print("Payment done:")
                print(json.dumps(pay, indent=2))
            except (ValueError, PaymentError) as e:
                print("Error:", e)

        elif choice == "2":
            try:
                payment_id = int(input("Payment ID to refund: "))
                pay = self.payment.refund_payment(payment_id)
                print("Payment refunded:")
                print(json.dumps(pay, indent=2))
            except (ValueError, PaymentError) as e:
                print("Error:", e)
            
    # Supplier Menu 
    def supplier_menu(self):
        import json
        print("\n--- Supplier Menu ---")
        print("1. Add Supplier")
        print("2. List Suppliers")
        print("3. Update Supplier")
        print("4. Delete Supplier")
        print("0. Back")
        choice = input("Choose: ")

        if choice == "1":
            name = input("Name: ")
            contact = input("Contact: ") or None
            address = input("Address (optional): ") or None
            try:
                sup = self.supplier.add_supplier(name, contact, address)
                print("Supplier added:")
                print(json.dumps(sup, indent=2))
            except SupplierError as e:
                print("Error:", e)

        elif choice == "2":
            try:
                sups = self.supplier.list_suppliers()
                print(json.dumps(sups, indent=2))
            except SupplierError as e:
                print("Error:", e)

        elif choice == "3":
            try:
                sup_id = int(input("Supplier ID: "))
                name = input("New Name (optional): ") or None
                contact = input("New Contact (optional): ") or None
                address = input("New Address (optional): ") or None
                sup = self.supplier.update_supplier(sup_id, {"name": name, "contact": contact, "address": address})
                print("Supplier updated:")
                print(json.dumps(sup, indent=2))
            except (ValueError, SupplierError) as e:
                print("Error:", e)

        elif choice == "4":
            try:
                sup_id = int(input("Supplier ID to delete: "))
                sup = self.supplier.delete_supplier(sup_id)
                print("Supplier deleted:")
                print(json.dumps(sup, indent=2))
            except (ValueError, SupplierError) as e:
                print("Error:", e)

# Reports Menu 
    def report_menu(self):
        import json
        print("\n--- Reports Menu ---")
        print("1. Generate Sales Report")
        print("2. Generate Stock Report")
        print("3. List All Reports")
        print("0. Back")
        choice = input("Choose: ")

        if choice == "1":
            try:
                report = self.report.generate_sales_report()
                print("Sales Report generated:")
                print(json.dumps(report, indent=2))
            except Exception as e:
                print("Error:", e)

        elif choice == "2":
            try:
                report = self.report.generate_stock_report()
                print("Stock Report generated:")
                print(json.dumps(report, indent=2))
            except Exception as e:
                print("Error:", e)

        elif choice == "3":
            try:
                reports = self.report.list_reports()
                print(json.dumps(reports, indent=2))
            except Exception as e:
                print("Error:", e)


if __name__ == "__main__":
    cli = PharmacyCLI()
    cli.run()
