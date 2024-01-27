from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.binance.utils import get_currency_price, get_currency_prices
from src.database import get_async_session

router = APIRouter()

from typing import List, Union

from fastapi import APIRouter, Depends

from src.binance.schemas import CurrencyPairBase, CurrencyPairCreate
from src.binance.service import read_price_by_symbol


@router.get("", response_model=Union[CurrencyPairCreate, List[CurrencyPairBase]])
async def get_price(
    symbol: str = None,
    db: AsyncSession = Depends(get_async_session),
):
    if symbol:
        # проверяем, есть ли закешированный результат
        currency_pair = await read_price_by_symbol(db, symbol=symbol)

        # В ТЗ сказано: Требуются курсы за текущий момент времени
        # То есть абсолютно не логично возвращать курс, сохраненный ранее
        # Ведь он не за текущий момент времени. Можно только сделать точность
        # До какого-то момента в прошлом, чтобы не отправлять запрос
        if currency_pair:
            return currency_pair
        else:
            created_pair = await get_currency_price(symbol)
            return created_pair
    else:
        # Если символ не передан, запрашиваем все

        # аналогично проверить, требуется ли возврат списка из БД

        # получаем свежую цену
        created_pairs = await get_currency_prices()
        return created_pairs
