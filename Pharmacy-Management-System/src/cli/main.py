import json

from services.medicine0_service import (
    MedicineService,
    MedicineError
)

from services.customer0_service import (
    CustomerService,
    CustomerError
)

from services.order0_service import (
    OrderService,
    OrderError
)

from services.payment0_service import (
    PaymentService,
    PaymentError
)

from services.report0_service import (
    ReportService
)

from services.supplier0_service import (
    SupplierService,
    SupplierError
)


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
                print("Invalid choice")

    def medicine_menu(self):

        print("\n--- Medicine Menu ---")
        print("1. Add Medicine")
        print("2. List Medicines")

        choice = input("Choose: ")

        if choice == "1":

            try:

                name = input("Name: ")
                sku = input("SKU: ")
                price = float(input("Price: "))
                stock = int(input("Stock: "))
                expiry = input("Expiry: ")
                category = input("Category: ") or None

                medicine = self.medicine.add_medicine(
                    name,
                    sku,
                    price,
                    stock,
                    expiry,
                    category
                )

                print(
                    json.dumps(
                        medicine,
                        indent=2
                    )
                )

            except Exception as e:
                print(e)

        elif choice == "2":

            medicines = self.medicine.list_medicines()

            print(
                json.dumps(
                    medicines,
                    indent=2
                )
            )

    def customer_menu(self):

        print("\n--- Customer Menu ---")
        print("1. Add Customer")
        print("2. List Customers")

        choice = input("Choose: ")

        if choice == "1":

            try:

                customer = self.customer.create_customer(
                    input("Name: "),
                    input("Email: "),
                    input("Phone: "),
                    input("City: ")
                )

                print(
                    json.dumps(
                        customer,
                        indent=2
                    )
                )

            except CustomerError as e:
                print(e)

        elif choice == "2":

            customers = self.customer.list_customers()

            print(
                json.dumps(
                    customers,
                    indent=2
                )
            )

    def order_menu(self):

        print("\n--- Order Menu ---")
        print("1. Create Order")
        print("2. List Orders")

        choice = input("Choose: ")

        if choice == "1":

            try:

                customer_id = int(
                    input("Customer ID: ")
                )

                med_id = int(
                    input("Medicine ID: ")
                )

                quantity = int(
                    input("Quantity: ")
                )

                order = self.order.create_order(
                    customer_id,
                    [
                        {
                            "med_id": med_id,
                            "quantity": quantity
                        }
                    ]
                )

                print(
                    json.dumps(
                        order,
                        indent=2
                    )
                )

            except OrderError as e:
                print(e)

        elif choice == "2":

            orders = self.order.list_orders()

            print(
                json.dumps(
                    orders,
                    indent=2
                )
            )

    def payment_menu(self):

        print("\n--- Payment Menu ---")
        print("1. Make Payment")
        print("2. List Payments")

        choice = input("Choose: ")

        if choice == "1":

            try:

                payment = self.payment.make_payment(
                    int(input("Order ID: ")),
                    input("Method: ")
                )

                print(
                    json.dumps(
                        payment,
                        indent=2
                    )
                )

            except PaymentError as e:
                print(e)

        elif choice == "2":

            payments = self.payment.list_payments()

            print(
                json.dumps(
                    payments,
                    indent=2
                )
            )

    def supplier_menu(self):

        print("\n--- Supplier Menu ---")
        print("1. Add Supplier")
        print("2. List Suppliers")

        choice = input("Choose: ")

        if choice == "1":

            try:

                supplier = self.supplier.add_supplier(
                    input("Name: "),
                    input("Contact: "),
                    input("Address: ")
                )

                print(
                    json.dumps(
                        supplier,
                        indent=2
                    )
                )

            except SupplierError as e:
                print(e)

        elif choice == "2":

            suppliers = self.supplier.list_suppliers()

            print(
                json.dumps(
                    suppliers,
                    indent=2
                )
            )

    def report_menu(self):

        print("\n--- Reports Menu ---")
        print("1. Sales Report")
        print("2. Stock Report")

        choice = input("Choose: ")

        if choice == "1":

            report = (
                self.report.generate_sales_report()
            )

            print(
                json.dumps(
                    report,
                    indent=2
                )
            )

        elif choice == "2":

            report = (
                self.report.generate_stock_report()
            )

            print(
                json.dumps(
                    report,
                    indent=2
                )
            )


if __name__ == "__main__":

    PharmacyCLI().run()
