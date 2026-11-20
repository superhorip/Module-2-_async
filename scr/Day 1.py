import asyncio
import aiohttp
import logging






class AsyncCrawler():
    def __init__(self, max_concurrent: int = 10):
        self._max_concurrent = max_concurrent
        self._semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_url(self, url: str) -> str:
        pass

    async def fetch_urls(self, urls: list[str]) -> dict[str, str]:
        ''' parallel loading of urls '''
        pass

    async def close(self):
        '''sesion close method'''
        pass







#Обрабатывать следующие исключения:
#- ❌ aiohttp.ClientError — сетевые ошибки
#- ⏰ asyncio.TimeoutError — таймауты
#- 🚫 aiohttp.ClientResponseError — HTTP ошибки (404, 500 и т.д.)
#Важен порядок обработки
#aiohttp.ClientResponseError наследуется от aiohttp.ClientError.
#Поэтому сначала нужно перехватывать ClientResponseError, а потом ClientError.
#Иначе более общий обработчик перехватит HTTP-ошибку раньше специального.
#В чём отличие от банковского проекта?
#В банковском проекте ты создавал собственные исключения для бизнес-логики, например когда клиент пытается снять больше денег, чем есть на счёте.
#В краулере ты работаешь с готовой библиотекой, которая уже предоставляет подходящие классы исключений.
#Моя рекомендация: обрабатывай все три типа исключений непосредственно в fetch_url(), логируй их и определяй, что должен вернуть метод при неудачной загрузке. Отдельные классы и обработчики пока не нужны.



