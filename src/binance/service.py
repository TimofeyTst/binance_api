from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.binance.schemas import CurrencyPairRead
from src.models import CurrencyPair


async def read_price_by_symbol(
    db: AsyncSession, symbol: str
) -> CurrencyPairRead | list[CurrencyPairRead]:
    query = select(CurrencyPair).where(CurrencyPair.symbol == symbol)
    result = await db.scalar(query)
    return result
