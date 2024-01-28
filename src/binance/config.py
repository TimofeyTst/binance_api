from pydantic_settings import BaseSettings


class BinanceConfig(BaseSettings):
    # В ТЗ сказано: Требуются курсы за текущий момент времени
    # То есть логично всегда возвращать курс, именно от api binance
    # Можно только кешировать в течение какого-то малого
    # промежутка времени. Для кеширования очень удобно подойдет Redis
    CACHE_TTL: int = 3  # 3 seconds


binance_config = BinanceConfig()
