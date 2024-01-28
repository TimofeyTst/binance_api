import asyncio
import json

import aiohttp

from src.binance.config import binance_config
from src.binance.constants import BASE_API, BASE_TICKER_PATH, HEADERS
from src.exceptions import HTTPException
from src.redis import RedisData, get_by_key, set_redis_key


async def get_currency_price(symbol):
    url = f"{BASE_API}/{BASE_TICKER_PATH}?symbol={symbol}"
    cache_key = f"currency_price:{symbol}"
    result = await cached_fetch(url, cache_key)
    return result


async def get_currency_prices():
    url = f"{BASE_API}/{BASE_TICKER_PATH}"
    cache_key = f"all_currency_prices"
    result = await cached_fetch(url, cache_key)
    return result


async def cached_fetch(url, cache_key):
    cached_result = await get_by_key(cache_key)
    if cached_result:
        return json.loads(cached_result)

    # получаем свежую цену
    async with aiohttp.ClientSession() as session:
        resp = await fetch_url(session, url)

    await set_redis_key(
        RedisData(key=cache_key, value=resp, ttl=binance_config.CACHE_TTL)
    )
    return json.loads(resp)


async def fetch_url(session, url):
    try:
        async with session.get(url, headers=HEADERS) as response:
            if response.status == 400:
                raise HTTPException(
                    status_code=400,
                    detail=f"Bad Request: Invalid symbol. URL: {url}",
                )
            elif response.status == 404:
                raise HTTPException(
                    status_code=404,
                    detail=f"Not Found: The requested URL '{url}' was not found.",
                )
            return await response.text()

    except aiohttp.client_exceptions.ClientConnectorError as e:
        raise HTTPException(status_code=503, detail=f"Error connecting to {url}: {e}")
    except asyncio.TimeoutError as e:
        raise HTTPException(
            status_code=504,
            detail=f"Gateway Timeout: Timeout while connecting to {url}: {e}",
        )
