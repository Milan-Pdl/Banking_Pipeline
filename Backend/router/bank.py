# Backend/router/bank.py
from fastapi import APIRouter, Request
from ..utils import limiter  # Import the shared limiter instance
from fastapi import Depends
from ..config import get_db,SCHEMA

bank_router = APIRouter(
    prefix="/bank",
    tags=["Info"]
)

# --- ACCOUNT ENDPOINT ---
@bank_router.get("/accounts")
@limiter.limit("2/minute")  
def get_accounts(request: Request, db: Depends = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM {SCHEMA}.account;")
    accounts = cursor.fetchall()
    cursor.close()
    return {"accounts": accounts}

# --- BRANCH ENDPOINT ---
@bank_router.get("/branches")
@limiter.limit("2/minute")  
def get_branches(request: Request, db: Depends = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM {SCHEMA}.branch;")
    branches = cursor.fetchall()
    cursor.close()
    return {"branches": branches}

# --- CARD ENDPOINT ---
@bank_router.get("/cards")
@limiter.limit("2/minute")  
def get_cards(request: Request, db: Depends = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM {SCHEMA}.card;")
    cards = cursor.fetchall()
    cursor.close()
    return {"cards": cards}

# --- CUSTOMER ENDPOINT ---
@bank_router.get("/customers")
@limiter.limit("2/minute")  
def get_customers(request: Request, db: Depends = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM {SCHEMA}.customer;")
    customers = cursor.fetchall()
    cursor.close()
    return {"customers": customers}

# --- PRODUCT ENDPOINT ---
@bank_router.get("/products")
@limiter.limit("2/minute")  
def get_products(request: Request, db: Depends = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM {SCHEMA}.product;")
    products = cursor.fetchall()
    cursor.close()
    return {"products": products}

@bank_router.get("/transactions")
@limiter.limit("2/minute")  
def get_transactions(request: Request, db: Depends = Depends(get_db)):

    cursor = db.cursor()
    # 2. Execute the query
    cursor.execute(f"SELECT * FROM {SCHEMA}.transaction;")
    
    # 3. Fetch the rows out of the database memory
    transactions = cursor.fetchall()
    
    # 4. Close the cursor so you don't leak connections
    cursor.close()
    
    return {"transactions": transactions}



@bank_router.get("/check-request")
@limiter.limit("5/minute")
def check_my_request(request: Request):
    # Manually look at where the request came from
    user_ip = request.client.host
    browser = request.headers.get("user-agent")
    
    return {
        "your_ip": user_ip,
        "your_browser": browser,
        "url_visited": str(request.url)
    }