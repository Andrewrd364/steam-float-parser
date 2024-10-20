import time
from random import uniform
from fake_useragent import UserAgent
import re

from config_manager import load_config, load_proxies, get_next_proxy
from fetcher import fetch_hrefs
from float_checker import fetch_floatvalue
from buyer import buy_listing
import logger

ua = UserAgent()

if __name__ == "__main__":
    logger.setup_logger()
    
    cookies = "ActListPageSize=10; undefined=true; sessionid=323b16a3ae29daa1fa7ad87b; timezoneOffset=18000,0; steamCurrencyId=5; extproviders_730=steam; browserid=3306290583273882712; strInventoryLastContext=730_2; app_impressions=578080@2_100100_100101_100102|730@2_100100_100101_100106; steamCountry=RU%7C6ac8734510766ae9db42e52a04f18dea; steamLoginSecure=76561198304489230%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MTAxQ18yNTM5RUMzMF85NjRFQSIsICJzdWIiOiAiNzY1NjExOTgzMDQ0ODkyMzAiLCAiYXVkIjogWyAid2ViOmNvbW11bml0eSIgXSwgImV4cCI6IDE3Mjk1MjE4MDAsICJuYmYiOiAxNzIwNzkzODg0LCAiaWF0IjogMTcyOTQzMzg4NCwgImp0aSI6ICIxMDJDXzI1MzlFQ0M5XzdDOTMxIiwgIm9hdCI6IDE3Mjk0MzM4ODQsICJydF9leHAiOiAxNzQ3NTQ5MTUyLCAicGVyIjogMCwgImlwX3N1YmplY3QiOiAiMzEuMTYyLjI3LjE5NyIsICJpcF9jb25maXJtZXIiOiAiMzEuMTYyLjI3LjE5NyIgfQ.pE0sGruIlIcZnYcL-k-nPSL93k9GM8e8BVuPmEpsp9znMTcQiMm_udK9Un4n9yDzA9TSijUkpR8YtEsSjk7hBg; webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days%22%3A15%2C%22new_device_cooldown_days%22%3A0%2C%22time_checked%22%3A1729433888%7D"
    sessionid = re.search(r'sessionid=([^;]+)', cookies).group(1)
    config = load_config('config.json')
    proxies = load_proxies('proxies.txt') 
    proxy_index = 0
    fetch_counter = 0

    urls = config.get('urls', [])

    while True: 
        for url in urls:
            if fetch_counter == 20:
                proxy_index = get_next_proxy(proxies, proxy_index)
                fetch_counter = 0
            hrefs, proxy_index = fetch_hrefs(url, proxies, proxy_index, user_agent=ua.random)
            fetch_counter += 1
            paintseeds = urls[url].get('paintseeds', [])
            float = urls[url].get('float', [])

            if hrefs:
                for href in hrefs:
                    if fetch_floatvalue(href, paintseeds, float, user_agent=ua.random):
                        buy_listing(href, ua.random, cookies, sessionid)

            time.sleep(uniform(2, 3)) 