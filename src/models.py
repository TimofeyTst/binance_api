from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, Numeric, String

from src.database import Base


class CurrencyPair(Base):
    __tablename__ = "currency_pair"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, nullable=False)
    price = Column(Numeric, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
