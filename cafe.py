# app.py

import streamlit as st
import database as db

# --- Streamlit Setup ---
st.set_page_config(page_title="Cafe Management", page_icon="☕")
st.title("☕ Cafe Management System")

# --- Initialize Database ---
db.connect_db()
menu = db.get_menu()

if not menu:
    st.warning("Menu is empty! Please add items in the 'Manage Menu' tab.")

tab1, tab2, tab3 = st.tabs(["Place Order", "View Orders", "Manage Menu"])

# --- Place Order ---
with tab1:
    st.header("🛒 Place Your Order")
    order = []

    for item in menu:
        quantity = st.number_input(f"{item} (${menu[item]:.2f} each)", min_value=0, step=1, key=f"order_{item}")
        if quantity > 0:
            item_total = menu[item] * quantity
            order.append((item, quantity, item_total))

    if st.button("Place Order"):
        if order:
            order_id = db.add_order(order)
            total = sum(item[2] for item in order)
            if order_id:
                st.success(f"Order #{order_id} placed! Total: ${total:.2f}")
                st.rerun()
            else:
                st.error("There was an error placing your order.")
        else:
            st.error("Please select at least one item.")

# --- View Orders ---
with tab2:
    st.header("📜 Order History")
    orders = db.get_orders()
    if orders:
        last_id = None
        for order_id, timestamp, item, qty, price in orders:
            if order_id != last_id:
                if last_id is not None:
                    st.write("---")
                st.subheader(f"Order #{order_id}")
                st.write(f"Timestamp: {timestamp}")
                last_id = order_id
            st.write(f"- {item}: {qty} × = ${price:.2f}")
    else:
        st.info("No orders placed yet.")

# --- Manage Menu ---
with tab3:
    st.header("📝 Manage Menu")

    with st.form("Add new item"):
        new_item = st.text_input("Item name")
        new_price = st.number_input("Price", min_value=0.0, format="%.2f")
        submit = st.form_submit_button("Add Item")

        if submit:
            if new_item.strip() and new_price > 0:
                db.add_menu_item(new_item.strip(), new_price)
                st.success(f"Added {new_item.strip()} for ${new_price:.2f}!")
                st.rerun()
            else:
                st.error("Please enter a valid item name and price.")

    st.subheader("📋 Current Menu")
    menu = db.get_menu()
    if menu:
        for item, price in menu.items():
            st.write(f"{item}: ${price:.2f}")
    else:
        st.info("Menu is empty! Add some items.")
