from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(
    title="Astrology API",
    description="FastAPI backend for astrology calculations and chart/table generation",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Astrology API is running"}
