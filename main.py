import uvicorn
from fastapi import FastAPI
# from fastapi.responses import RedirectResponse
from os import getenv as cfg
from settings import config_settings
from dbms.mariadb import create_db, db_test
from services.users import users_router

app = FastAPI()

app.include_router(users_router, prefix="/users")

@app.on_event("startup")
async def on_startup():
    await create_db()
    # await db_test()

# # @app.get("/")
# # async def home():
# #     return RedirectResponse(url="/home/")

@app.get("/")
async def test():
    return {"test": "test ok!"}


if __name__=="__main__":
    config_settings()
    uvicorn.run("main:app", host=cfg("HOST_IP"), port=int(cfg("PORT")), reload=cfg("DEBUG"))
