from fastapi import FastAPI
from fastapi.responses import RedirectResponse

import uvicorn

app = FastAPI()

# app.include_router(router, prefix="/user")

# @app.on_event("startup")
# def on_startup():
#     db_connect()

# @app.get("/")
# async def home():
#     return RedirectResponse(url="/home/")

if __name__=="__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
