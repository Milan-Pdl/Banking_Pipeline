from fastapi import FastAPI,Request
from .router import bank_router
from .utils import limiter
from slowapi.util import get_remote_address #user ko ip address lina
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
# from contextlib import asynccontextmanager

app=FastAPI()

# creating the limiter object
 #   takes the ip addess and keeps the time record of people when they visit the api endpoint


app.state.limiter=limiter # now we can access this limiter object 

app.add_middleware(SlowAPIMiddleware)

# adding a async decorator ratelimitexcedded

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request :Request, exe: RateLimitExceeded):
      return JSONResponse(
            status_code=429,
            content={"message":"too many request"}
      )


@app.get("/")
def read_root():
    return {"message":"Hello World"}    

routers=[bank_router]
for router in routers:
    app.include_router(router=router,prefix="/api")


