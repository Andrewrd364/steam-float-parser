import json
import time
from constants import proxy_timeout, BLOCK_DURATION

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
        while True:
            proxy_index = (proxy_index + 1) % len(proxies)
            if is_proxy_available(proxies[proxy_index]):
                return proxy_index 
    return proxy_index

def is_proxy_available(proxy):
    current_time = time.time()
    proxy_key = proxy.get('http')

    last_block_time = proxy_timeout.get(proxy_key)

    if last_block_time and current_time - last_block_time < BLOCK_DURATION:
        return False

    return True

def block_proxy(proxy):
    proxy_key = proxy.get('http')
    proxy_timeout[proxy_key] = time.time()
    print(proxy_timeout)

def load_steam_cookies(file_path='steam_cookies.txt'):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            steam_cookies = file.readline().strip()
            return steam_cookies
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return None
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        return None