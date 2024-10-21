import aiohttp
import asyncio

async def fetch_hrefs(url, proxy, user_agent=None):
    headers = {
        'User-Agent': user_agent
    }
    proxy_url = proxy.get('http', None) if proxy else None
    try:
        url += '/render/?query=&start=0&count=10&country=RU&language=english&currency=5'

        async with aiohttp.ClientSession() as session:
            if proxy:
                async with session.get(url, headers=headers, proxy=proxy_url, timeout=3) as response:
                    response.raise_for_status()
                    data = await response.json()
            else:
                async with session.get(url, headers=headers, timeout=3) as response:
                    response.raise_for_status()
                    data = await response.json()

            hrefs = []
            for listing in data["listinginfo"].values():
                subtotal = listing.get("converted_price")
                if not subtotal:
                    continue
                fee = listing.get("converted_fee")
                total = subtotal + fee

                listingid = listing["listingid"]
                assetid = listing["asset"]["id"]
                link_template = listing["asset"]["market_actions"][0]["link"]
                link = link_template.replace("%listingid%", listingid).replace("%assetid%", assetid)
                print(link)
                iteminfo = {"link": link, "subtotal": subtotal, "fee": fee, "total": total, "listingid": listingid, "referer": url}
                hrefs.append(iteminfo)

            print(f"Successfully fetched with proxy: {proxy or 'No Proxy'}")
            return hrefs

    except aiohttp.ClientError as e:
        print(f"Error fetching page with proxy {proxy or 'No Proxy'}: {e}")
        return []
    except asyncio.TimeoutError:
        print(f"Request timed out with proxy {proxy_url or 'No Proxy'}")
        return []
