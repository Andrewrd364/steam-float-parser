import aiohttp
import logger
import asyncio

async def buy_listing(href, ua, cookies, sessionid):
    url = f"https://steamcommunity.com/market/buylisting/{href['listingid']}"
    
    headers = {
        "Cookie": cookies,
        "Host": "steamcommunity.com",
        "Origin": "https://steamcommunity.com",
        "Referer": href["referer"],
        "User-Agent": ua
    }

    formdata = {
        "sessionid": sessionid,
        "currency": "5",
        "subtotal": href["subtotal"],
        "fee": href["fee"],
        "total": href["total"],
        "quantity": "1",
        "billing_state": "",
        "save_my_address": ""
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=formdata) as response:
            if response.status == 200:
                json_response = await response.json()
                print("Покупка выполнена успешно!")
                print(json_response)
                logger.log_info(f'\ninspect link: {href["link"]}\ntotal: {href["total"]/100} rub\nresponse: {json_response}')
            else:
                text_response = await response.text()
                print(f"Ошибка: {response.status}")
                print(text_response)
                logger.log_error(f'\ninspect link: {href["link"]}\ntotal: {href["total"]/100} rub\nresponse: {text_response}')