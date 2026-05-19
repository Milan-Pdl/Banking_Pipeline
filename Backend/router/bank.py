from fastapi import APIRouter

bank_router=APIRouter(
    prefix="/bank",
    tags=["Info"]
)


bank_router.get("/transactions")
def get_transactions():
    return {"kai xaina yrr aaila"}