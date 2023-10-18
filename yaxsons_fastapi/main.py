from fastapi import FastAPI

import uvicorn

app = FastAPI()

# app.include_router(_router)

# @app.on_event("startup")
# def on_startup():
#     connect_db()

@app.get("/")
async def home() -> dict:
    return {
        "message": "home"
    }

if __name__=="__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
