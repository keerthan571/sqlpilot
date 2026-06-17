from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.database import router as database_router

app = FastAPI(
    title="SQLPilot API",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(database_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to SQLPilot API 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }