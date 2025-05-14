import sqlite3
import json

# This connects to SQLite database (creates db.sqlite if it doesn't exist)
conn = sqlite3.connect("db.sqlite")
cur = conn.cursor()

# Create tables
cur.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp INTEGER NOT NULL,
        customer_id INTEGER NOT NULL,
        notes TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        order_id INTEGER,
        item_id INTEGER,
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
        FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
    )
""")

# Load sample data
with open("example_orders.json", "r") as f:
    orders_data = json.load(f)

for entry in orders_data:
    name, phone, timestamp, notes, items = entry["name"], entry["phone"], entry["timestamp"], entry["notes"], entry["items"]

    # Insert or fetch customer
    cur.execute("SELECT id FROM customers WHERE name = ? AND phone = ?", (name, phone))
    result = cur.fetchone()
    customer_id = result[0] if result else cur.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (name, phone)).lastrowid

    # Create order
    order_id = cur.execute("INSERT INTO orders (timestamp, customer_id, notes) VALUES (?, ?, ?)", (timestamp, customer_id, notes)).lastrowid

    # Insert items and associate with order
    for item in items:
        cur.execute("SELECT id FROM items WHERE name = ?", (item["name"],))
        item_row = cur.fetchone()
        item_id = item_row[0] if item_row else cur.execute("INSERT INTO items (name, price) VALUES (?, ?)", (item["name"], item["price"])).lastrowid
        cur.execute("INSERT INTO order_items (order_id, item_id) VALUES (?, ?)", (order_id, item_id))

conn.commit()
conn.close()
