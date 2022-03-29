
from fastapi import FastAPI, Depends
from routers import store_apis
from utils.tools import validate_request

app = FastAPI()

app.include_router(store_apis.router, tags=['Admin'],)
# dependencies=[Depends(validate_request)])