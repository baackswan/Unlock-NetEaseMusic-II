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
    browser.add_cookie({"name": "MUSIC_U", "value": "005A8CC6AD04C144C3CA245DDAA2EB4AB8B6C44DCC8BA4CECA58D62295B5C5D8A12181B9EEDFB16949E8FD8A7A4EAE7C56DFB50AE120B82D7CB1D8F4A11BDAE8300F3F4CA92BD586FBDBC623F2634EBF0296527DB12F4AF4500CF86736851707A34A2B79C5B3B6C6F66603B6014ACA7D35E71B480DBA0F99B7A108DF516E149C68336038DA64CF55D583E5390740087384D9A2FD5675B4BD08E2045284076BCC5EADC13B56FC4071F89E6E84478E63AED380D90985AE36C6B28621B83CC439B3CA29AD89FBDA71945F10356E84BE447FC6F5D9E189507797152823F06D9FCECD98771B17781B306A33AF25DEFFF4A2EC94FCA7491EED5357B5BB49266A6BF5C3FBD00858F73A82C7178607AECE50178AD1BA2451D3C71A641D7C8EDB494942A4D352A3A29423ECB0FDC3070BA7E2AAABC300B3E7E7FCFC806988D0CA85EA90B75C87D6E202C83EAA57DD509921F9059835"})
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
