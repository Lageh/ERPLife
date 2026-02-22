from fastapi import FastAPI

app = FastAPI(title="ERPLife Finance Service")


@app.get("/")
def root():
    return {"service": "finance-service", "status": "running"}


@app.get("/health")
def health():
    return {"status": "ok"}
