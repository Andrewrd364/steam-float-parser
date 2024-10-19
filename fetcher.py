import requests
from bs4 import BeautifulSoup
import re
import json

def fetch_hrefs(url, proxies=[], proxy_index=0, user_agent=None):
    headers = {
        'User-Agent': user_agent,
        'Range': 'bytes=-20000',
    }
    proxy = proxies[proxy_index] if proxies else 'localhost'

    try:
        url += '/render?start=0&count=10&currency=1&format=json'
        response = requests.get(url, headers=headers, proxies=proxy, timeout=3) if proxies else requests.get(url, headers=headers, timeout=3)
        response.raise_for_status()

        data_size = len(response.content)
        print(f"Загружено {data_size / (1024):.2f} KB данных")
        data = response.json()
        hrefs = []
        for listing in data["listinginfo"].values():
            listingid = listing["listingid"]
            assetid = listing["asset"]["id"]
            link_template = listing["asset"]["market_actions"][0]["link"]
            link = link_template.replace("%listingid%", listingid).replace("%assetid%", assetid)
            print(link)
            hrefs.append(link)

        print(f"Successfully fetched with proxy: {proxy}")
        return hrefs, proxy_index

    except requests.exceptions.RequestException as e:
        print(f"Error fetching page with proxy {proxy}: {e}")
        proxy_index = (proxy_index + 1) % len(proxies) if proxies else proxy_index
        return [], proxy_index