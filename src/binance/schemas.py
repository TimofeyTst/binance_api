from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class CurrencyPairBase(BaseModel):
    symbol: str
    price: Decimal


class CurrencyPairCreate(CurrencyPairBase):
    pass


class CurrencyPairRead(CurrencyPairBase):
    id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
