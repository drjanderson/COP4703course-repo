from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Advanced DB Course API")

app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "ok"}