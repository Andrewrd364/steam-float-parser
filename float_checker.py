from collections import OrderedDict
import aiohttp

MAX_CACHE_SIZE = 500
cache = OrderedDict()

async def fetch_floatvalue(href, paintseeds, float_list, user_agent):
    base_api_url = "https://api.csgotrader.app/float?url="
    headers = {'User-Agent': user_agent}

    if href["link"] in cache:
        cached_data = cache[href["link"]]
        print(f"Cached Float value: {cached_data.get('floatvalue')}, Paintseed: {cached_data.get('paintseed')}")
    else:
        try:
            api_url = base_api_url + href["link"]

            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, headers=headers) as response:
                    response.raise_for_status()
                    data = await response.json()

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

    return False