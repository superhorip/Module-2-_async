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
    print ('main 1')
    crawler = Day_1.AsyncCrawler(max_concurrent=10)
    for url in urls_list:
        html = await crawler.fetch_url(url=url)
        
    await crawler.close()
start = time.perf_counter()
asyncio.run(main())
end = time.perf_counter()

duration = end - start
print (f'Длительность {duration:.3f} сек') 

async def main():
    print ('main 2')
    crawler = Day_1.AsyncCrawler(max_concurrent=10)

    result_dict = await crawler.fetch_urls(urls=urls_list)
    print (f'Len of result dict {len(result_dict)}')
    await crawler.close()

start = time.perf_counter()

asyncio.run(main())
end = time.perf_counter()

duration = end - start
print (f'Длительность {duration:.3f} сек') 