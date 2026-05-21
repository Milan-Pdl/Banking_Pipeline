# Backend/router/bank.py
from fastapi import APIRouter, Request
from ..utils import limiter  # Import the shared limiter instance
from fastapi import Depends
from ..config import get_db,SCHEMA
from ..utils import fetch_table_as_json

bank_router = APIRouter(
    prefix="/bank",
    tags=["Info"]
)

# --- ACCOUNT ENDPOINT ---
@bank_router.get("/accounts")
@limiter.limit("2/minute")
def get_accounts(request: Request, db: Depends = Depends(get_db)):

    accounts = fetch_table_as_json(
        db=db,
        schema=SCHEMA,
        table_name="account"
    )

    return {"accounts": accounts}

# --- BRANCH ENDPOINT ---
@bank_router.get("/branches")
@limiter.limit("2/minute")
def get_branches(request: Request, db: Depends = Depends(get_db)):

    branches = fetch_table_as_json(
        db=db,
        schema=SCHEMA,
        table_name="branch"
    )

    return {"branches": branches}

# --- CARD ENDPOINT ---
@bank_router.get("/cards")
@limiter.limit("2/minute")
def get_cards(request: Request, db: Depends = Depends(get_db)):

    cards = fetch_table_as_json(
        db=db,
        schema=SCHEMA,
        table_name="card"
    )
    return {"cards":cards}

# --- CUSTOMER ENDPOINT ---
@bank_router.get("/customers")
@limiter.limit("2/minute")
def get_customers(request: Request, db: Depends = Depends(get_db)):

    customers = fetch_table_as_json(
        db=db,
        schema=SCHEMA,
        table_name="customer"
    )

    return {"customers": customers}

# --- PRODUCT ENDPOINT ---
@bank_router.get("/products")
@limiter.limit("2/minute")
def get_products(request: Request, db: Depends = Depends(get_db)):

    products = fetch_table_as_json(
        db=db,
        schema=SCHEMA,
        table_name="product"
    )

    return {"products": products}

#transactions endpoint 

@bank_router.get("/transactions")
@limiter.limit("2/minute")
def get_transactions(request: Request, db: Depends = Depends(get_db)):

    transactions = fetch_table_as_json(
        db=db,
        schema=SCHEMA,
        table_name="transaction"
    )

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