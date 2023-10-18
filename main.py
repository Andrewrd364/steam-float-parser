import requests
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import winsound
import time

patterns = [511, 550, 897, 396, 639, 487, 87, 298, 12, 140, 508, 800, 597, 86, 302, 936, 172, 654, 399, 89]

op = webdriver.ChromeOptions()
op.add_argument('headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=op)

base_url = "https://inspect.pricempire.com/"

item_url = "https://steamcommunity.com/market/listings/730/Glock-18%20%7C%20High%20Beam%20%28Factory%20New%29"
driver.get(item_url)

while True:
    time.sleep(4)
    driver.refresh()
    btns = driver.find_elements(By.CSS_SELECTOR, '.market_actionmenu_button')
    inspect_links = []
    for btn in btns:
        driver.execute_script("arguments[0].click();", btn)
        popup = driver.find_element(By.CSS_SELECTOR, '#market_action_popup_itemactions > a')

        href = popup.get_attribute('href')
        inspect_links.append(href)

    if len(inspect_links) > 0:
        print('\n' * 15)

    for i in inspect_links:
        full_url = base_url + "?url=" + i
        response = requests.get(full_url)

        if response.status_code == 200:
            data = json.loads(response.text)
            floatvalue = data['iteminfo']['floatvalue']
            paintseed = data['iteminfo']['paintseed']
            print(f'Float: {floatvalue}, Pattern: {paintseed}')
            if int(paintseed) in patterns or float(floatvalue) < 0.001:
                winsound.Beep(1000, 500)
        else:
            print("Request failed with status code:", response.status_code, response.content)
