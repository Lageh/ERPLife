from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class TransactionCreate(BaseModel):
    description: str
    amount: Decimal
    transaction_type: str


class TransactionRead(BaseModel):
    id: int
    description: str
    amount: Decimal
    transaction_type: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)