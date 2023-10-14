from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def hi() -> dict:
    return {
        "message": "Hi hi~2"
    }