# Backend/router/bank.py
from fastapi import APIRouter, Request
from ..utils import limiter  # Import the shared limiter instance
from fastapi import Depends
from ..config import get_db,SCHEMA

bank_router = APIRouter(
    prefix="/bank",
    tags=["Info"]
)

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