import Day_1
import asyncio
import aiohttp
import logging





crawler = Day_1.AsyncCrawler(max_concurrent=1)

asyncio.run(crawler.fetch_url(url='https://www.google.com/'))