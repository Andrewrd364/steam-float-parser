import time
from random import uniform
from fake_useragent import UserAgent

from config_manager import load_config, load_proxies, get_next_proxy
from fetcher import fetch_hrefs
from float_checker import fetch_floatvalue

ua = UserAgent()

if __name__ == "__main__":
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
                fetch_floatvalue(hrefs, paintseeds, float, user_agent=ua.random)

            time.sleep(uniform(2, 3)) 