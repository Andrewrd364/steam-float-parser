import requests
import logger

def buy_listing(href, ua, cookies, sessionid):
    url = f"https://steamcommunity.com/market/buylisting/{href["listingid"]}"
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

    response = requests.post(url, headers=headers, data=formdata)

    if response.status_code == 200:
        print("Покупка выполнена успешно!")
        print(response.json())
        logger.log_info(f'\ninspect link: {href["link"]}\ntotal: {href["total"]/100} rub\nresponse: {response.json()}')
    else:
        print(f"Ошибка: {response.status_code}")
        print(response.text)
        logger.log_error(f'\ninspect link: {href["link"]}\ntotal: {href["total"]/100} rub\nresponse: {response.json()}')
