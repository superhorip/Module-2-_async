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
        soup = BeautifulSoup(self._html, 'lxml')
        links = self.extract_links(soup=soup, base_url=self._url)
        text = self.extract_text(soup=soup, selector=None)
        metadata = self.extract_metadata(soup=soup)
        images = self.extract_images(soup=soup, base_url=self._url)
        headings = self.extract_heading(soup=soup)
        tables = self.extract_tables(soup=soup)
        lists = self.extract_lists(soup=soup)
        return {"url" : self._url,
                "title" : metadata['title'],
                "text" : text,
                "links" : links,
                "images" : images,
                "heading" : headings,
                "tables" : tables,
                "lists" : lists,
                "metadata" : metadata
                }



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
        if not isinstance(soup, BeautifulSoup):
            raise TypeError('Invalid type of soup object')        
        if selector is not None:
            if not isinstance(selector, str):
                raise TypeError('Wrong type for selector')            
            element = soup.select_one(selector=selector)
            if element is not None:
                text = element.get_text(separator=" ", strip=True)
                return text
            if element is None:
                return ""
        text = soup.get_text(separator=" ", strip=True)
        return text




    def extract_metadata(self, soup: BeautifulSoup) -> dict:
        '''извлечение мета-тегов (title, description, keywords)'''
        if not isinstance(soup, BeautifulSoup):
            raise TypeError('Invalid type of soup object')
        title_tag = soup.find("title")
        if title_tag is None:
            title = None
        else:
            title = title_tag.get_text(strip=True)
        description_tag = soup.find("meta", attrs={"name": "description"})
        if description_tag is None:
            description = None
        else:
            description = description_tag.get("content")
        keywords_tag = soup.find("meta", attrs={"name": "keywords"})
        if keywords_tag is None:
            keywords = None
        else:
            keywords = keywords_tag.get("content")

        return {"title" : title, "description" : description, "keywords" : keywords}

    def extract_images(self, soup: BeautifulSoup, base_url: str) -> list[dict[str, str | None]]:
        if not isinstance(soup, BeautifulSoup):
            raise TypeError('Invalid type of soup object')
        if not isinstance(base_url, str):
            raise TypeError('Wrong url input type')     
        parsed_url = urlparse(url=base_url)
        if parsed_url.scheme not in ('http', 'https') or not parsed_url.hostname:
            raise ValueError('Invalid url')                    
        images = soup.find_all("img")
        images_list = []
        for image in images:
            src = image.get('src')
            if src is None or src == "":
                continue
            try:
                joined_url = urljoin(base_url, src)
                parced_url = urlparse(url=joined_url)
                if parced_url.scheme not in ('http', 'https') or not parced_url.hostname:
                    continue
            except ValueError as e:
                self._logger.error("Wrong link type")
                continue
            
            alt = image.get('alt')
            images_list.append({"src": joined_url, "alt": alt})
        return images_list






    

    
    def extract_heading(self, soup: BeautifulSoup) -> list[dict[str, str]]:
        if not isinstance(soup, BeautifulSoup):
            raise TypeError('Invalid type of soup object')        
        heading_tags = soup.find_all(["h1", "h2", "h3"])
        headings = []
        for heading in heading_tags:
            headings.append({"level" : heading.name ,"text" : heading.get_text(strip=True)})
        return headings


    def extract_tables(self, soup: BeautifulSoup) -> list[list[list[str]]]:
        """Извлечение всех HTML-таблиц."""
        if not isinstance(soup, BeautifulSoup):
            raise TypeError("Invalid type of soup object")

        tables = []

        for table in soup.find_all("table"):
            rows = []

            for row in table.find_all("tr"):
                cells = []

                for cell in row.find_all(["th", "td"]):
                    cells.append(cell.get_text(strip=True))

                rows.append(cells)

            tables.append(rows)

        return tables



        
    def extract_lists(self, soup: BeautifulSoup) -> list[dict]:
        """Извлечение маркированных и нумерованных списков."""
        if not isinstance(soup, BeautifulSoup):
            raise TypeError("Invalid type of soup object")

        result = []

        for list_tag in soup.find_all(["ul", "ol"]):
            items = []

            for item in list_tag.find_all("li"):
                items.append(item.get_text(strip=True))

            result.append({
                "type": list_tag.name,
                "items": items
            })

        return result





  




