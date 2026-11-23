import asyncio
import aiohttp
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urljoin


class HTMLParser():
    def __init__(self, logger: logging.Logger):
        if not isinstance(logger, logging.Logger):
            raise ValueError('Wront logger object type)')
        self._logger = logger
        self._html = None
        self._url = None


    async def parse_html(self, html: str, url: str) -> dict:
        ''' — парсинг HTML'''
        if not isinstance(html, str):
            raise TypeError('Wrong html input type')
        if not isinstance(url, str):
            raise TypeError('Wrong url input type')        
        parsed_url = urlparse(url=url)
        if parsed_url.scheme not in ('http', 'https') or not parsed_url.hostname:
            raise ValueError('Invalid url')        
        self._html = html
        self._url = url


    def extract_links(self, soup: BeautifulSoup, base_url: str) -> list[str]:
        ''' — извлечение всех ссылок'''
        if not isinstance(soup, BeautifulSoup):
            raise TypeError('Invalid type of soup object')
        if not isinstance(base_url, str):
            raise TypeError('Wrong url input type')        
        parsed_url = urlparse(url=base_url)
        if parsed_url.scheme not in ('http', 'https') or not parsed_url.hostname:
            raise ValueError('Invalid url')          
        raw_from_soup = soup.find_all("a")
        links = []
        for raw in raw_from_soup:
            prob_link = raw.get('href')
            if prob_link is None or prob_link == '':
                continue
            try:
                joined_url = urljoin(base_url, prob_link)
                parsed_url = urlparse(url=joined_url)                
                if parsed_url.scheme not in ('http', 'https') or not parsed_url.hostname:
                    continue
            except ValueError as e:
                self._logger.error("Wrong link type")
                continue
            links.append(joined_url)

        return links


        

    def extract_text(self, soup: BeautifulSoup, selector: str = None) -> str:
        ''' — извлечение текста'''

    def extract_metadata(self, soup: BeautifulSoup) -> dict:
        '''извлечение мета-тегов (title, description, keywords)'''
        pass





    pass




