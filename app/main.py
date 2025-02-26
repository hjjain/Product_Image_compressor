from fastapi import FastAPI
from app.routes import upload, status  # Import new API

app = FastAPI()

app.include_router(upload.router)
app.include_router(status.router)  # Register status API


@app.get("/test-log")
async def test_log():
    print("🔥 FastAPI log test: This should appear in the console!")
    return {"message": "Check the terminal for logs!"}
