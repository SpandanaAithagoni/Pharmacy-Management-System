import tkinter as tk
from tkinter import ttk, messagebox
import json

# Import your existing services
from src.services.medicine0_service import MedicineService, MedicineError
from src.services.customer0_service import CustomerService, CustomerError
from src.services.order0_service import OrderService, OrderError
from src.services.payment0_service import PaymentService, PaymentError
from src.services.report0_service import ReportService
from src.services.supplier0_service import SupplierService, SupplierError


class PharmacyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Pharmacy Management System")
        self.geometry("1000x650")

        # Initialize Services
        self.medicine = MedicineService()
        self.customer = CustomerService()
        self.order = OrderService()
        self.payment = PaymentService()
        self.report = ReportService()
        self.supplier = SupplierService()

        # Create notebook (tabs)
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        # Tabs
        self.tab_med = ttk.Frame(notebook)
        self.tab_cust = ttk.Frame(notebook)
        self.tab_order = ttk.Frame(notebook)
        self.tab_pay = ttk.Frame(notebook)
        self.tab_sup = ttk.Frame(notebook)
        self.tab_rep = ttk.Frame(notebook)

        notebook.add(self.tab_med, text="Medicines")
        notebook.add(self.tab_cust, text="Customers")
        notebook.add(self.tab_order, text="Orders")
        notebook.add(self.tab_pay, text="Payments")
        notebook.add(self.tab_sup, text="Suppliers")
        notebook.add(self.tab_rep, text="Reports")

        # Build each screen
        self.build_medicine_tab()
        self.build_customer_tab()
        self.build_order_tab()
        self.build_payment_tab()
        self.build_supplier_tab()
        self.build_report_tab()

    # ---------------------------------------------------------
    # MEDICINES TAB
    # ---------------------------------------------------------
    def build_medicine_tab(self):
        frame = self.tab_med

        # Input form
        form = ttk.LabelFrame(frame, text="Add Medicine")
        form.pack(fill="x", padx=10, pady=10)

        self.m_name = tk.StringVar()
        self.m_sku = tk.StringVar()
        self.m_price = tk.StringVar()
        self.m_stock = tk.StringVar()
        self.m_expiry = tk.StringVar()
        self.m_cat = tk.StringVar()

        ttk.Label(form, text="Name").grid(row=0, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.m_name).grid(row=0, column=1)

        ttk.Label(form, text="SKU").grid(row=0, column=2, sticky="w")
        ttk.Entry(form, textvariable=self.m_sku).grid(row=0, column=3)

        ttk.Label(form, text="Price").grid(row=1, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.m_price).grid(row=1, column=1)

        ttk.Label(form, text="Stock").grid(row=1, column=2, sticky="w")
        ttk.Entry(form, textvariable=self.m_stock).grid(row=1, column=3)

        ttk.Label(form, text="Expiry").grid(row=2, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.m_expiry).grid(row=2, column=1)

        ttk.Label(form, text="Category").grid(row=2, column=2, sticky="w")
        ttk.Entry(form, textvariable=self.m_cat).grid(row=2, column=3)

        ttk.Button(form, text="Add Medicine", command=self.add_medicine).grid(row=3, column=0, pady=10)
        ttk.Button(form, text="Refresh", command=self.load_medicines).grid(row=3, column=1, pady=10)

        # List
        columns = ("ID", "Name", "SKU", "Price", "Stock", "Expiry", "Category")
        self.m_table = ttk.Treeview(frame, columns=columns, show="headings", height=12)

        for col in columns:
            self.m_table.heading(col, text=col)
            self.m_table.column(col, width=120)

        self.m_table.pack(fill="both", expand=True, padx=10, pady=10)
        self.load_medicines()

    def add_medicine(self):
        try:
            result = self.medicine.add_medicine(
                self.m_name.get(),
                self.m_sku.get(),
                float(self.m_price.get()),
                int(self.m_stock.get()),
                self.m_expiry.get(),
                self.m_cat.get() or None
            )
            messagebox.showinfo("Success", json.dumps(result, indent=2))
            self.load_medicines()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_medicines(self):
        for row in self.m_table.get_children():
            self.m_table.delete(row)

        try:
            meds = self.medicine.list_medicines()
            for m in meds:
                self.m_table.insert("", "end",
                                    values=(
                                        m["med_id"], m["name"], m["sku"], m["price"],
                                        m["stock"], m.get("expiry_date"), m.get("category")
                                    ))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------------------------------------------------
    # CUSTOMERS TAB
    # ---------------------------------------------------------
    def build_customer_tab(self):
        frame = self.tab_cust

        form = ttk.LabelFrame(frame, text="Add Customer")
        form.pack(fill="x", padx=10, pady=10)

        self.c_name = tk.StringVar()
        self.c_email = tk.StringVar()
        self.c_phone = tk.StringVar()
        self.c_city = tk.StringVar()

        ttk.Label(form, text="Name").grid(row=0, column=0)
        ttk.Entry(form, textvariable=self.c_name).grid(row=0, column=1)

        ttk.Label(form, text="Email").grid(row=0, column=2)
        ttk.Entry(form, textvariable=self.c_email).grid(row=0, column=3)

        ttk.Label(form, text="Phone").grid(row=1, column=0)
        ttk.Entry(form, textvariable=self.c_phone).grid(row=1, column=1)

        ttk.Label(form, text="City").grid(row=1, column=2)
        ttk.Entry(form, textvariable=self.c_city).grid(row=1, column=3)

        ttk.Button(form, text="Add Customer", command=self.add_customer).grid(row=2, column=0, pady=10)
        ttk.Button(form, text="Refresh", command=self.load_customers).grid(row=2, column=1, pady=10)

        columns = ("ID", "Name", "Email", "Phone", "City")
        self.c_table = ttk.Treeview(frame, columns=columns, show="headings", height=12)

        for col in columns:
            self.c_table.heading(col, text=col)
            self.c_table.column(col, width=150)

        self.c_table.pack(fill="both", expand=True, padx=10, pady=10)
        self.load_customers()

    def add_customer(self):
        try:
            result = self.customer.create_customer(
                self.c_name.get(), self.c_email.get(),
                self.c_phone.get(), self.c_city.get() or None
            )
            messagebox.showinfo("Success", json.dumps(result, indent=2))
            self.load_customers()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_customers(self):
        for row in self.c_table.get_children():
            self.c_table.delete(row)

        try:
            customers = self.customer.list_customers()
            for c in customers:
                self.c_table.insert("", "end",
                                    values=(c["cust_id"], c["name"], c["email"], c["phone"], c.get("city")))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------------------------------------------------
    # ORDERS TAB
    # ---------------------------------------------------------
    def build_order_tab(self):
        frame = self.tab_order

        form = ttk.LabelFrame(frame, text="Create Order")
        form.pack(fill="x", padx=10, pady=10)

        self.o_cust_id = tk.StringVar()
        self.o_items = tk.StringVar()

        ttk.Label(form, text="Customer ID").grid(row=0, column=0)
        ttk.Entry(form, textvariable=self.o_cust_id).grid(row=0, column=1)

        ttk.Label(form, text="Items (med_id:qty, comma separated)").grid(row=1, column=0)
        ttk.Entry(form, textvariable=self.o_items, width=50).grid(row=1, column=1)

        ttk.Button(form, text="Create Order", command=self.create_order).grid(row=2, column=0, pady=10)
        ttk.Button(form, text="Refresh", command=self.load_orders).grid(row=2, column=1, pady=10)

        columns = ("ID", "Customer", "Amount", "Status")
        self.o_table = ttk.Treeview(frame, columns=columns, show="headings", height=12)

        for col in columns:
            self.o_table.heading(col, text=col)
            self.o_table.column(col, width=150)

        self.o_table.pack(fill="both", expand=True, padx=10, pady=10)
        self.load_orders()

    def create_order(self):
        try:
            customer_id = int(self.o_cust_id.get())
            items_str = self.o_items.get()

            items = []
            for pair in items_str.split(","):
                med, qty = pair.strip().split(":")
                items.append({"med_id": int(med), "quantity": int(qty)})

            result = self.order.create_order(customer_id, items)
            messagebox.showinfo("Success", json.dumps(result, indent=2))
            self.load_orders()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_orders(self):
        for row in self.o_table.get_children():
            self.o_table.delete(row)

        try:
            orders = self.order.list_orders()
            for o in orders:
                self.o_table.insert("",
                                    "end",
                                    values=(o["order_id"], o["cust_id"], o["total_amount"], o["status"]))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------------------------------------------------
    # PAYMENTS TAB
    # ---------------------------------------------------------
    def build_payment_tab(self):
        frame = self.tab_pay

        form = ttk.LabelFrame(frame, text="Payments")
        form.pack(fill="x", padx=10, pady=10)

        self.p_order_id = tk.StringVar()
        self.p_method = tk.StringVar(value="CASH")
        self.p_payment_id = tk.StringVar()

        ttk.Label(form, text="Order ID").grid(row=0, column=0)
        ttk.Entry(form, textvariable=self.p_order_id).grid(row=0, column=1)

        ttk.Label(form, text="Method").grid(row=1, column=0)
        ttk.Entry(form, textvariable=self.p_method).grid(row=1, column=1)

        ttk.Button(form, text="Make Payment", command=self.make_payment).grid(row=2, column=0, pady=10)

        ttk.Label(form, text="Payment ID").grid(row=3, column=0)
        ttk.Entry(form, textvariable=self.p_payment_id).grid(row=3, column=1)

        ttk.Button(form, text="Refund", command=self.refund_payment).grid(row=4, column=0, pady=10)

        columns = ("ID", "Order", "Amount", "Method", "Status")
        self.p_table = ttk.Treeview(frame, columns=columns, show="headings", height=12)

        for col in columns:
            self.p_table.heading(col, text=col)
            self.p_table.column(col, width=150)

        self.p_table.pack(fill="both", expand=True, padx=10, pady=10)
        self.load_payments()

    def make_payment(self):
        try:
            result = self.payment.make_payment(int(self.p_order_id.get()), self.p_method.get())
            messagebox.showinfo("Success", json.dumps(result, indent=2))
            self.load_payments()
            self.load_orders()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refund_payment(self):
        try:
            result = self.payment.refund_payment(int(self.p_payment_id.get()))
            messagebox.showinfo("Refunded", json.dumps(result, indent=2))
            self.load_payments()
            self.load_orders()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_payments(self):
        for row in self.p_table.get_children():
            self.p_table.delete(row)

        try:
            pays = self.payment.list_payments()
            for p in pays:
                self.p_table.insert("",
                                    "end",
                                    values=(p["payment_id"], p["order_id"], p["amount"],
                                            p["method"], p["status"]))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------------------------------------------------
    # SUPPLIERS TAB
    # ---------------------------------------------------------
    def build_supplier_tab(self):
        frame = self.tab_sup

        form = ttk.LabelFrame(frame, text="Add Supplier")
        form.pack(fill="x", padx=10, pady=10)

        self.s_name = tk.StringVar()
        self.s_contact = tk.StringVar()
        self.s_address = tk.StringVar()

        ttk.Label(form, text="Name").grid(row=0, column=0)
        ttk.Entry(form, textvariable=self.s_name).grid(row=0, column=1)

        ttk.Label(form, text="Contact").grid(row=1, column=0)
        ttk.Entry(form, textvariable=self.s_contact).grid(row=1, column=1)

        ttk.Label(form, text="Address").grid(row=2, column=0)
        ttk.Entry(form, textvariable=self.s_address).grid(row=2, column=1)

        ttk.Button(form, text="Add Supplier", command=self.add_supplier).grid(row=3, column=0, pady=10)
        ttk.Button(form, text="Refresh", command=self.load_suppliers).grid(row=3, column=1, pady=10)

        columns = ("ID", "Name", "Contact", "Address")
        self.s_table = ttk.Treeview(frame, columns=columns, show="headings", height=12)
        for col in columns:
            self.s_table.heading(col, text=col)
            self.s_table.column(col, width=150)

        self.s_table.pack(fill="both", expand=True, padx=10, pady=10)
        self.load_suppliers()

    def add_supplier(self):
        try:
            result = self.supplier.add_supplier(
                self.s_name.get(), self.s_contact.get() or None, self.s_address.get() or None
            )
            messagebox.showinfo("Success", json.dumps(result, indent=2))
            self.load_suppliers()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_suppliers(self):
        for row in self.s_table.get_children():
            self.s_table.delete(row)
        try:
            sups = self.supplier.list_suppliers()
            for s in sups:
                self.s_table.insert("", "end",
                                    values=(s["supplier_id"], s["name"], s["contact"], s["address"]))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------------------------------------------------
    # REPORTS TAB
    # ---------------------------------------------------------
    def build_report_tab(self):
        frame = self.tab_rep

        ttk.Button(frame, text="Sales Report", command=self.sales_report).pack(pady=5)
        ttk.Button(frame, text="Stock Report", command=self.stock_report).pack(pady=5)
        ttk.Button(frame, text="List Reports", command=self.list_reports).pack(pady=5)

        self.report_text = tk.Text(frame, wrap="word", height=25)
        self.report_text.pack(fill="both", expand=True, padx=10, pady=10)

    def sales_report(self):
        try:
            r = self.report.generate_sales_report()
            self.report_text.delete("1.0", "end")
            self.report_text.insert("1.0", json.dumps(r, indent=2))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def stock_report(self):
        try:
            r = self.report.generate_stock_report()
            self.report_text.delete("1.0", "end")
            self.report_text.insert("1.0", json.dumps(r, indent=2))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def list_reports(self):
        try:
            r = self.report.list_reports()
            self.report_text.delete("1.0", "end")
            self.report_text.insert("1.0", json.dumps(r, indent=2))
        except Exception as e:
            messagebox.showerror("Error", str(e))


# -------------------------------------------------------------
# RUN APPLICATION
# -------------------------------------------------------------
if __name__ == "__main__":
    app = PharmacyApp()
    app.mainloop()
