from fastapi import FastAPI
# from fastapi.responses import RedirectResponse
from settings import LoadSettings
import uvicorn

config = LoadSettings()()
app = FastAPI()

# app.include_router(router, prefix="/user")

# @app.on_event("startup")
# def on_startup():
#     db_connect()

# @app.get("/")
# async def home():
#     return RedirectResponse(url="/home/")

@app.get("/")
async def test():
    return {"test": "test ok!"}

if __name__=="__main__":
    uvicorn.run("main:app", host=config.HOST_IP, port=config.PORT, reload=config.DEBUG)
