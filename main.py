from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import sqlite3
import time

app = FastAPI()

# Safe connection function
def get_db():
    return sqlite3.connect("db.sqlite", check_same_thread=False)

# Models
class Item(BaseModel):
    name: str
    price: float

class Customer(BaseModel):
    name: str
    phone: int

class Order(BaseModel):
    id: int
    customer_id: int
    notes: str

# --------- Item Endpoints ---------

@app.post("/items")
def add_item(item: Item):
    try:
        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO items (name, price) VALUES (?, ?)", (item.name, item.price))
        db.commit()
        return {"id": cur.lastrowid, "name": item.name, "price": item.price}
    except Exception as e:
        print("REAL DB ERROR:", str(e))
        raise HTTPException(status_code=500, detail="Something went wrong while adding the item")
    finally:
        db.close()

@app.get("/items/{item_id}")
def fetch_item(item_id: int):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    row = cur.fetchone()
    db.close()
    if not row:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": row[0], "name": row[1], "price": row[2]}

@app.put("/items/{item_id}")
def modify_item(item_id: int, item: Item):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE items SET name = ?, price = ? WHERE id = ?", (item.name, item.price, item_id))
    db.commit()
    db.close()
    return {"id": item_id, "name": item.name, "price": item.price}

@app.delete("/items/{item_id}")
def remove_item(item_id: int):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM items WHERE id = ?", (item_id,))
    db.commit()
    db.close()
    return {"message": f"Item {item_id} deleted"}

# --------- Customer Endpoints ---------

@app.post("/customer")
def insert_customer(customer: Customer):
    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (customer.name, customer.phone))
    db.commit()
    cust_id = cur.lastrowid
    db.close()
    return {"id": cust_id, "name": customer.name, "phone": customer.phone}

@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
    row = cur.fetchone()
    db.close()
    if not row:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"id": row[0], "name": row[1], "phone": row[2]}

@app.put("/customers/{customer_id}")
def revise_customer(customer_id: int, customer: Customer):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE customers SET name = ?, phone = ? WHERE id = ?", (customer.name, customer.phone, customer_id))
    db.commit()
    db.close()
    return {"id": customer_id, "name": customer.name, "phone": customer.phone}

@app.delete("/customers/{customer_id}")
def drop_customer(customer_id: int):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM orders WHERE customer_id = ?", (customer_id,))
    found = cur.fetchone()
    if found:
        db.close()
        return {"message": "Please delete the entry in orders table."}
    cur.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    db.commit()
    db.close()
    return {"message": "Customer deleted successfully"}

# --------- Order Endpoints ---------

@app.post("/orders/{order_id}")
def create_order(order: Order):
    db = get_db()
    cur = db.cursor()
    timestamp = int(time.time())
    cur.execute("INSERT INTO orders (timestamp, customer_id, notes) VALUES (?, ?, ?)",
                (timestamp, order.customer_id, order.notes))
    db.commit()
    order_id = cur.lastrowid
    db.close()
    return {"id": order_id, "timestamp": timestamp, "customer_id": order.customer_id, "notes": order.notes}

@app.get("/orders/{order_id}")
def read_order(order_id: int):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    order = cur.fetchone()
    db.close()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"id": order[0], "timestamp": order[1], "customer_id": order[2], "notes": order[3]}

@app.put("/orders/{order_id}")
def change_order(order_id: int, order: Order):
    db = get_db()
    cur = db.cursor()
    timestamp = int(time.time())
    cur.execute("UPDATE orders SET timestamp = ?, customer_id = ?, notes = ? WHERE id = ?",
                (timestamp, order.customer_id, order.notes, order_id))
    db.commit()
    db.close()
    return {"id": order_id, "timestamp": timestamp, "customer_id": order.customer_id, "notes": order.notes}

@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    db.commit()
    db.close()
    return {"message": f"Order {order_id} deleted"}

# --------- Redirect Root to /docs ---------

@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs")
