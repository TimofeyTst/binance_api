from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.binance.utils import get_currency_price, get_currency_prices
from src.database import get_async_session

router = APIRouter()

from typing import List, Union

from fastapi import APIRouter, Depends

from src.binance.schemas import CurrencyPairBase


@router.get("/price", response_model=Union[CurrencyPairBase, List[CurrencyPairBase]])
async def get_price(
    symbol: str = None,
    db: AsyncSession = Depends(get_async_session),
):
    if symbol:
        created_pair = await get_currency_price(symbol)
        return created_pair
    else:
        # Если символ не передан, запрашиваем все
        created_pairs = await get_currency_prices()
        return created_pairs
