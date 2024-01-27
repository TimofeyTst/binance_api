import asyncio
import json
from datetime import datetime

import aiohttp

from src.binance.constants import BASE_API, BASE_TICKER_PATH, HEADERS
from src.binance.schemas import CurrencyPairBase, CurrencyPairCreate
from src.exceptions import HTTPException


async def get_currency_price(symbol):
    url = f"{BASE_API}/{BASE_TICKER_PATH}?symbol={symbol}"

    async with aiohttp.ClientSession() as session:
        resp = await fetch_url(session, url)
        resp_dict = json.loads(resp)
        resp_dict["timestamp"] = datetime.now()
        return CurrencyPairCreate.parse_obj(resp_dict)


async def get_currency_prices():
    url = f"{BASE_API}/{BASE_TICKER_PATH}"

    async with aiohttp.ClientSession() as session:
        resp = await fetch_url(session, url)
        resp_list = json.loads(resp)

        # Парсим каждый элемент в списке
        parsed_resp_list = [CurrencyPairBase.parse_obj(item) for item in resp_list]

        return parsed_resp_list


async def fetch_url(session, url):
    try:
        async with session.get(url, headers=HEADERS) as response:
            return await response.text()
    except aiohttp.client_exceptions.ClientConnectorError as e:
        raise HTTPException(status_code=503, detail=f"Error connecting to {url}: {e}")
    except aiohttp.client_exceptions.ClientResponseError as e:
        if e.status == 404:
            raise HTTPException(
                status_code=404,
                detail=f"Not Found: The requested URL '{url}' was not found.",
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Internal Server Error: Failed to retrieve the URL '{url}': {e}",
            )
    except asyncio.TimeoutError as e:
        raise HTTPException(
            status_code=504,
            detail=f"Gateway Timeout: Timeout while connecting to {url}: {e}",
        )
