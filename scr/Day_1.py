import asyncio
import aiohttp
import logging
import Day_2_html_parser as parser






class AsyncCrawler():
    def __init__(self, max_concurrent: int = 20):
        self._max_concurrent = max_concurrent
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._session = aiohttp.ClientSession(timeout = aiohttp.ClientTimeout(total=5, connect=5, sock_read=2))
        self._logger = logging.getLogger(f'{__name__}.{self.__class__.__name__} ')
        

        



    async def fetch_url(self, url: str) -> str | None:
        if not isinstance(url, str):
            raise TypeError('Wrong type')
        try:
            async with self._semaphore:
                self._logger.info('Starting response to %s', url)
                async with self._session.get(url=url) as response:
                    self._logger.info('Making response to %s', url)
                    response.raise_for_status()
                    html = await response.text()
                    self._logger.info('Response recieved from %s', url)
                    return html
        except aiohttp.ClientResponseError as e:
            self._logger.error("HTTP ошибка %s: %s", e.status, url)
            return None
        
        except asyncio.TimeoutError:
            self._logger.error("Превышено время ожидания: %s", url)
            return None            

        except aiohttp.ClientError as e:
            self._logger.error("Сетевая ошибка %s: %s", url, e)
            return None



        

    async def fetch_urls(self, urls: list[str]) -> dict[str, str]:
        ''' async loading of urls '''
        if not isinstance(urls, list):
            raise TypeError('Wrong type')
        result_dict: dict[str, str] = dict()
        corutines_list = []
        for url in urls:
            corutines_list.append(self.fetch_url(url=url))
        results = await asyncio.gather(*corutines_list)
        result_dict = {url:result for url, result in zip(urls, results) if result is not None}
        return result_dict

    async def fetch_and_parse(self, url: str) -> dict | None:
        if not isinstance(url, str):
            raise TypeError('Wrong type')
        html = await self.fetch_url(url=url)
        if html is None:
            return None
        parser_obj = parser.HTMLParser(logger=self._logger)
        parsed_results = await parser_obj.parse_html(html=html, url=url)
        return parsed_results




            






    async def close(self):
        '''sesion close method'''
        await self._session.close()










