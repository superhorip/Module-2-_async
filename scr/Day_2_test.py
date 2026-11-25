import asyncio
import aiohttp
import logging
from bs4 import BeautifulSoup



import Day_1
import asyncio
import aiohttp
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

urls_list = [
    "https://www.google.com",
    "https://www.python.org",
    "https://www.wikipedia.org",
    "https://www.github.com",
    "https://www.stackoverflow.com",
    "https://www.microsoft.com",
    "https://www.example.com",
    "https://this-site-does-not-exist-928374.com",  # Нерабочий URL
    "https://www.apple.com",
    "https://www.mozilla.org",
    "https://www.reddit.com",
    "https://invalid-domain-739281.com",  # Нерабочий URL
    "https://www.cloudflare.com",
    "https://www.bbc.com",
    "https://www.nasa.gov",
    "https://httpbin.org/delay/9"
]











async def main():
    crawler = Day_1.AsyncCrawler(max_concurrent=10)
    results = await asyncio.gather(*(crawler.fetch_and_parse(url) for url in urls_list))
    parsing_results = []
    for result in results:
        if result is None:
            continue

        report = {
            "url": result["url"],
            "title": result["title"],
            "text_length": len(result["text"]),
            "links_count": len(result["links"]),
            "links": result["links"],
            "images_count": len(result["images"])
        }

        parsing_results.append(report)
        print(report)


    await crawler.close()



start = time.perf_counter()
asyncio.run(main())
end = time.perf_counter()

duration = end - start
print (f'Длительность {duration:.3f} сек') 

