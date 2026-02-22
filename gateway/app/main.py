from fastapi import FastAPI, HTTPException
import httpx # type: ignore
import os

app = FastAPI(title="ERPLife Gateway")


@app.get("/")
def root():
    return {"service": "gateway", "status": "running"}


@app.get("/health")
def health():
    return {"status": "ok"}


IDENTITY_BASE_URL = os.getenv("IDENTITY_BASE_URL", "http://localhost:8001")
FINANCE_BASE_URL = os.getenv("FINANCE_BASE_URL", "http://localhost:8002")


@app.get("/api/identity/health")
def identity_health():
    try:
        r = httpx.get(f"{IDENTITY_BASE_URL}/health", timeout=5.0)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Identity service unavailable: {e}")


@app.get("/api/finance/health")
def finance_health():
    try:
        r = httpx.get(f"{FINANCE_BASE_URL}/health", timeout=5.0)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Finance service unavailable: {e}")
