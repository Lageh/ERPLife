from fastapi import FastAPI

app = FastAPI(title="ERPLife Identity Service")

@app.get("/health")
def health():
    return {"status": "ok"}
