from fastapi import FastAPI

app = FastAPI(
    title="SQLPilot API",
    description="AI Powered Database Copilot",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "name": "SQLPilot",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }