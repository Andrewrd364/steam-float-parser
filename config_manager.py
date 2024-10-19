import json

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