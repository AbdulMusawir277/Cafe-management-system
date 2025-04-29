# database.py

import sqlite3
from datetime import datetime

DB_NAME = "cafe.db"

def connect_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        
        c.execute("""
            CREATE TABLE IF NOT EXISTS menu (
                item_name TEXT PRIMARY KEY,
                price REAL NOT NULL
            )
        """)
        
        c.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL
            )
        """)
        
        c.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                order_id INTEGER,
                item_name TEXT,
                quantity INTEGER,
                total_price REAL,
                FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
            )
        """)
        conn.commit()

def add_menu_item(item_name, price):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO menu (item_name, price) VALUES (?, ?)", (item_name, price))
            conn.commit()
    except Exception as e:
        print("Error adding menu item:", e)

def get_menu():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT item_name, price FROM menu")
        return dict(c.fetchall())

def add_order(order_items):
    """ order_items: list of tuples (item_name, quantity, total_price) """
    try:
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO orders (timestamp) VALUES (?)", (datetime.now().isoformat(),))
            order_id = c.lastrowid
            for item_name, quantity, total_price in order_items:
                c.execute(
                    "INSERT INTO order_items (order_id, item_name, quantity, total_price) VALUES (?, ?, ?, ?)",
                    (order_id, item_name, quantity, total_price)
                )
            conn.commit()
            return order_id
    except Exception as e:
        print("Error placing order:", e)
        return None

def get_orders():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("""
            SELECT o.order_id, o.timestamp, i.item_name, i.quantity, i.total_price
            FROM orders o
            JOIN order_items i ON o.order_id = i.order_id
            ORDER BY o.order_id
        """)
        return c.fetchall()
