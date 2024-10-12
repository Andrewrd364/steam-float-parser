import requests
from bs4 import BeautifulSoup
import re
import json
import winsound
import time
from fake_useragent import UserAgent
from random import uniform

ua = UserAgent()

def load_config(config_file):
    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
        return config
    except Exception as e:
        print(f"Error loading config: {e}")
        return None

def load_proxies(proxy_file):
    try:
        with open(proxy_file, 'r') as file:
            proxies = file.readlines()
        
        proxy_list = []
        for proxy in proxies:
            proxy = proxy.strip()
            if proxy:
                proxy_dict = {
                    "http": f"socks5://{proxy}",
                    "https": f"socks5://{proxy}"
                }
                proxy_list.append(proxy_dict)
        
        return proxy_list
    except Exception as e:
        print(f"Error loading proxies: {e}")
        return []

def get_next_proxy(proxies, proxy_index):
    if proxies:
        proxy_index = (proxy_index + 1) % len(proxies) 
        return proxy_index 
    return proxy_index

def fetch_hrefs(url, proxies, proxy_index):
    headers = {'User-Agent': ua.random}
    proxy = proxies[proxy_index]
    try:
        response = requests.get(url, headers=headers, proxies=proxy) 
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script')

        hrefs = []
        for script in scripts:
            if 'g_rgAssets' in script.text:
                assets_match = re.search(r'g_rgAssets\s*=\s*(\{.*?\});', script.text)
                if assets_match:
                    assets_data = json.loads(assets_match.group(1))
                    for app_id, contexts in assets_data.items():
                        for context_id, items in contexts.items():
                            for asset_id, item_data in items.items():
                                if 'actions' in item_data:
                                    for action in item_data['actions']:
                                        if 'link' in action:
                                            link = action['link'].replace('%assetid%', asset_id)
                                            print(link)
                                            hrefs.append(link)
        print(f"Successfully fetched with proxy: {proxy}")
        return hrefs, proxy_index

    except requests.exceptions.RequestException as e:
        print(f"Error fetching page with proxy {proxy}: {e}")
        proxy_index = get_next_proxy(proxies, proxy_index)
        return [], proxy_index

def fetch_floatvalue(hrefs, paintseeds, float_list):
    base_api_url = "https://api.csgotrader.app/float?url="
    headers = {'User-Agent': ua.random}

    for href in hrefs:
        try:
            api_url = base_api_url + href
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()

            data = response.json()
            floatvalue = data.get('iteminfo', {}).get('floatvalue', None)
            paintseed = data.get('iteminfo', {}).get('paintseed', None)
            
            if floatvalue is not None:
                print(f"Float value: {floatvalue}, Paintseed: {paintseed}")
                
                # Проверка условий в зависимости от наличия значений в списках
                if not float_list and paintseeds:  # Только paintseeds
                    if paintseed in paintseeds:
                        winsound.Beep(2000, 500)

                elif not paintseeds and float_list:  # Только float_list
                    if floatvalue < float_list:
                        winsound.Beep(2000, 500)

                elif paintseeds and float_list:  # Оба условия
                    if paintseed in paintseeds or floatvalue < float_list:
                        winsound.Beep(2000, 500)
                    
            else:
                print("Float value not found")

        except Exception as e:
            print(f"Error fetching float value: {e}")
            continue


if __name__ == "__main__":
    config = load_config('config.json')
    proxies = load_proxies('proxies.txt') 
    proxy_index = 0
    fetch_counter = 0

    if config and proxies:
        urls = config.get('urls', [])

        while True: 
            for url in urls:
                if fetch_counter == 20:
                    proxy_index = get_next_proxy(proxies, proxy_index)
                    fetch_counter = 0
                hrefs, proxy_index = fetch_hrefs(url, proxies, proxy_index) 
                fetch_counter += 1
                paintseeds = urls[url].get('paintseeds', [])
                float = urls[url].get('float', [])

                if hrefs:
                    fetch_floatvalue(hrefs, paintseeds, float)  

                time.sleep(uniform(1, 3)) 

            time.sleep(uniform(4, 6)) 
    else:
        print("Failed to load configuration or proxies.")
