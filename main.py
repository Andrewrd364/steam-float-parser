from fake_useragent import UserAgent
import re
import asyncio
from aiohttp import ClientSession
import time

from config_manager import load_config, load_proxies, get_next_proxy, block_proxy, load_steam_cookies
from fetcher import fetch_hrefs
from float_checker import fetch_floatvalue
from buyer import buy_listing
import logger

ua = UserAgent()

async def main():
    logger.setup_logger()
    
    cookies = load_steam_cookies()
    sessionid = re.search(r'sessionid=([^;]+)', cookies).group(1)
    config = load_config('config.json')
    proxies = load_proxies('proxies.txt')
    proxy_index = 0

    urls = config.get('urls', [])

    async with ClientSession() as session:
        while True:
            for url in urls:
                while True:
                    proxy_index = get_next_proxy(proxies, proxy_index)
                    proxy = proxies[proxy_index]

                    hrefs = await fetch_hrefs(url, proxy, user_agent=ua.random)
                    paintseeds = urls[url].get('paintseeds', [])
                    float_value = urls[url].get('float', [])

                    if hrefs and not hrefs == 429:
                        for href in hrefs:
                            if await fetch_floatvalue(href, paintseeds, float_value, user_agent=ua.random):
                                await buy_listing(href, ua.random, cookies, sessionid)
                        await asyncio.sleep(1)
                        break
                    if hrefs == 429:
                        block_proxy(proxy)
                    continue

if __name__ == "__main__":
    asyncio.run(main())