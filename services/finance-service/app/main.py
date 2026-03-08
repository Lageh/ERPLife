from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db_dep import get_db
from app import models, schemas
from app.db_dep import get_db

app = FastAPI(title="ERPLife Finance Service")


@app.get("/")
def root():
    return {"service": "finance-service", "status": "running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/transactions", response_model=schemas.TransactionRead)
def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db)
):
    db_transaction = models.Transaction(
        description=transaction.description,
        amount=transaction.amount,
        transaction_type=transaction.transaction_type
    )

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return db_transaction

@app.get("/transactions", response_model=list[schemas.TransactionRead])
def list_transactions(db: Session = Depends(get_db)):
    transactions = db.query(models.Transaction).all()
    return transactions