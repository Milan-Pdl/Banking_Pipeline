# Backend/router/bank.py
from fastapi import APIRouter, Request
from ..utils import limiter  # Import the shared limiter instance

bank_router = APIRouter(
    prefix="/bank",
    tags=["Info"]
)

@bank_router.get("/transactions")
@limiter.limit("2/minute")  
def get_transactions(request: Request):
    return {"kai xaina yrr aaila"}


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