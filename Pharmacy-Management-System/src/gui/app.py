# app.py

import streamlit as st
import pandas as pd

from src.services.medicine0_service import MedicineService
from src.services.customer0_service import CustomerService
from src.services.order0_service import OrderService
from src.services.payment0_service import PaymentService
from src.services.supplier0_service import SupplierService
from src.services.report0_service import ReportService

# -----------------------------

# PAGE CONFIG

# -----------------------------

st.set_page_config(
page_title="Pharmacy Management System",
page_icon="💊",
layout="wide"
)

# -----------------------------

# SERVICES

# -----------------------------

medicine_service = MedicineService()
customer_service = CustomerService()
order_service = OrderService()
payment_service = PaymentService()
supplier_service = SupplierService()
report_service = ReportService()

# -----------------------------

# SIDEBAR

# -----------------------------

st.sidebar.title("💊 Pharmacy Management")

menu = st.sidebar.radio(
"Navigation",
[
"Dashboard",
"Medicines",
"Customers",
"Orders",
"Payments",
"Suppliers",
"Reports"
]
)

# -----------------------------

# DASHBOARD

# -----------------------------

if menu == "Dashboard":

```
st.title("📊 Dashboard")

medicines = medicine_service.list_medicines()
customers = customer_service.list_customers()
orders = order_service.list_orders()
payments = payment_service.list_payments()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Medicines", len(medicines))
col2.metric("Customers", len(customers))
col3.metric("Orders", len(orders))
col4.metric("Payments", len(payments))

st.subheader("Low Stock Medicines")

low_stock = [
    m for m in medicines
    if m.get("stock", 0) < 10
]

st.dataframe(low_stock)
```

# -----------------------------

# MEDICINES

# -----------------------------

elif menu == "Medicines":

```
st.title("💊 Medicines")

with st.form("medicine_form"):

    name = st.text_input("Medicine Name")
    sku = st.text_input("SKU")
    price = st.number_input("Price", min_value=0.0)
    stock = st.number_input("Stock", min_value=0)
    expiry = st.text_input("Expiry Date")
    category = st.text_input("Category")

    submit = st.form_submit_button(
        "Add Medicine"
    )

    if submit:

        try:

            medicine_service.add_medicine(
                name,
                sku,
                price,
                stock,
                expiry,
                category
            )

            st.success("Medicine Added")

        except Exception as e:

            st.error(str(e))

st.subheader("Medicine Inventory")

medicines = medicine_service.list_medicines()

st.dataframe(pd.DataFrame(medicines))
```

# -----------------------------

# CUSTOMERS

# -----------------------------

elif menu == "Customers":

```
st.title("👥 Customers")

with st.form("customer_form"):

    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    city = st.text_input("City")

    submit = st.form_submit_button(
        "Add Customer"
    )

    if submit:

        try:

            customer_service.create_customer(
                name,
                email,
                phone,
                city
            )

            st.success("Customer Added")

        except Exception as e:

            st.error(str(e))

st.dataframe(
    pd.DataFrame(
        customer_service.list_customers()
    )
)
```

# -----------------------------

# ORDERS

# -----------------------------

elif menu == "Orders":

```
st.title("📦 Orders")

customers = customer_service.list_customers()
medicines = medicine_service.list_medicines()

customer_id = st.number_input(
    "Customer ID",
    min_value=1
)

med_id = st.number_input(
    "Medicine ID",
    min_value=1
)

qty = st.number_input(
    "Quantity",
    min_value=1
)

if st.button("Create Order"):

    try:

        order_service.create_order(
            customer_id,
            [
                {
                    "med_id": med_id,
                    "quantity": qty
                }
            ]
        )

        st.success("Order Created")

    except Exception as e:

        st.error(str(e))

st.dataframe(
    pd.DataFrame(
        order_service.list_orders()
    )
)
```

# -----------------------------

# PAYMENTS

# -----------------------------

elif menu == "Payments":

```
st.title("💳 Payments")

order_id = st.number_input(
    "Order ID",
    min_value=1
)

method = st.selectbox(
    "Method",
    [
        "CASH",
        "CARD",
        "UPI"
    ]
)

if st.button("Make Payment"):

    try:

        payment_service.make_payment(
            order_id,
            method
        )

        st.success("Payment Completed")

    except Exception as e:

        st.error(str(e))

st.dataframe(
    pd.DataFrame(
        payment_service.list_payments()
    )
)
```

# -----------------------------

# SUPPLIERS

# -----------------------------

elif menu == "Suppliers":

```
st.title("🚚 Suppliers")

with st.form("supplier_form"):

    name = st.text_input("Supplier Name")
    contact = st.text_input("Contact")
    address = st.text_area("Address")

    submit = st.form_submit_button(
        "Add Supplier"
    )

    if submit:

        try:

            supplier_service.add_supplier(
                name,
                contact,
                address
            )

            st.success("Supplier Added")

        except Exception as e:

            st.error(str(e))

st.dataframe(
    pd.DataFrame(
        supplier_service.list_suppliers()
    )
)
```

# -----------------------------

# REPORTS

# -----------------------------

elif menu == "Reports":

```
st.title("📈 Reports")

if st.button("Generate Sales Report"):

    report = report_service.generate_sales_report()

    st.json(report)

if st.button("Generate Stock Report"):

    report = report_service.generate_stock_report()

    st.json(report)
```
