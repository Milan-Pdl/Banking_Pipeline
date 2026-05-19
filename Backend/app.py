from fastapi import FastAPI
from router import bank_router

app=FastAPI()

@app.get("/")
def read_root():
    return {"message":"Hello World"}    

routers=[bank_router]
for router in routers:
    app.include_router(router=router,prefix="/api")