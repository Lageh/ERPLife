from fastapi import FastAPI

app = FastAPI(title="ERPLife Identity Service")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"service": "identity-service", "status": "running"}