# BP534 - Dosa Restaurant API

A simple backend project for a dosa restaurant, built using **FastAPI** and **SQLite**. This was developed as a final project with the goal of practicing REST API design and relational databases using only the core Python stack.

---

## Features

Full CRUD API for:
- **Customers**  
- **Menu Items**  
- **Orders**

Other highlights:
- SQLite-based backend with primary and foreign key constraints
- Auto-generated `timestamp` for orders
- Swagger UI available at `/docs`
- `/` root route automatically redirects to docs
- Uses only **FastAPI** and **SQLite** as per project requirements

---

##  Setup Instructions

###  Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Final_Project_Dosa_API.git
cd Final_Project_Dosa_API
```
### Step 2: Create and Activate Virtual Environment
```bash
python -m venv venv
```
For Windows:
```bash
venv\Scripts\activate
```
For macOS/Linux:
```bash
source venv/bin/activate
```

### Step 3: Install Required Packages
```bash
pip install -r requirements.txt
```

### Step 4: Initialize SQLite Database
```bash
python init_db.py
```

### Step 5: Run the FastAPI Server
```bash
uvicorn main:app --reload
```

After running the FastAPI Server you will be provided with a link http://127.0.0.1:8000/ to access the Dosa Restaurant API.