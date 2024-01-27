from sqlalchemy import Column, DateTime, Integer, String

from src.database import Base


class CurrencyPair(Base):
    __tablename__ = "currency_pair"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    timestamp = Column(DateTime)
