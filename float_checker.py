import requests
import winsound
from collections import OrderedDict

MAX_CACHE_SIZE = 250
cache = OrderedDict()

def fetch_floatvalue(href, paintseeds, float_list, user_agent):
    base_api_url = "https://api.csgotrader.app/float?url="
    headers = {'User-Agent': user_agent}

    if href["link"] in cache:
        print(f"cached Float value: {cache[href["link"]].get('floatvalue')}, Paintseed: {cache[href["link"]].get('paintseed')}")
    else:
        try:
            api_url = base_api_url + href["link"]
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()

            data = response.json()
            floatvalue = data.get('iteminfo', {}).get('floatvalue', None)
            paintseed = data.get('iteminfo', {}).get('paintseed', None)

            if floatvalue is not None and paintseed is not None:
                print(f"Float value: {floatvalue}, Paintseed: {paintseed}")
                if len(cache) >= MAX_CACHE_SIZE:
                    cache.popitem(last=False)  

                cache[href["link"]] = {'floatvalue': floatvalue, 'paintseed': paintseed}
                    
                if paintseed in paintseeds or (float_list and floatvalue < float_list):
                    return True

        except Exception as e:
            print(f"Error fetching float value: {e}")