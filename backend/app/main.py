from fastapi import FastAPI

app = FastAPI(
    title="SQLPilot API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "Welcome to SQLPilot API 🚀"}


@app.get("/health")
def health():
    return {"status": "healthy"}