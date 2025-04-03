# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "002C589332F55C187FFC0A13E90F76DCC341FA9C365E70B205BB80A9ADA098E73DD86EBDB2A251961A41ACA62606127DE150FF8BF831BFC628AA39EC83CB6DDB5DEBDE99651DDC2BFC491A7DFEF289A690538AF50F23717880628546DB442A3A8E36F468A2DBBF9B6F36642210D334D2969B6E625078019772D1D01419784119FC484AD1A06C1413CB6F1C0CAC3A7B4EB162BA36081DE2F7C122CEFD48385448F1CEDEE395D37B501F598EE4DA54C028C42A11A6207AD1F17524965EEC28DF538EEC4887AA2E8220EA2636BB2633ADD96015012D922DC587A6C0C11D3FAE25B8DB533861141126E8A7B53B5A7A611B78BBBC4589B7993221BB6BDE67B999D4B1D4F913B86CC5170891A3044A387824D70DF197CAF2C4A60D62DE3A539B17E7D3ED2255DB8BD523F3FC36AF07BCE1C19A82E99B96B1FC4F5B97C1217AEEECFFA23C7314F7F688D44BCC30A7A5D62B3661B6"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
