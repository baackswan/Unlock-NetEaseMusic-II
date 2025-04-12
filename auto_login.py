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
    browser.add_cookie({"name": "MUSIC_U", "value": "0082C9107A0EADE764F5EA0D65A70804A7209AB452DC2039999F89814EB4442CE8958A8D3504C475B596172A9B60270C26189F628644B0024485985F10C4FC317D901C3317669F936A57D71257F182A9ECB645A1EB94899093CDAAB0C8C239CB7372B6879F435410FC708AC0A482091ED527595AE927594CEF970DDFC17421F30E96AF860C722F9BC5547D3FD72B16988B434528138C012A38F1053833B6BC486DA2D14153D26B3E1854D486AF92042836BE11D5A02BCCBFA66E52D5ECDE753F1A92E0AABF80449D84301FC0A1FB09835E3637007C2BBEBC2F3DFE5A92F7991217ECC555E12C9C0446B2ED9877F9FB1A9143AD24A312DE29586142ECB1ECDFD9F03F6AF9D2E0504419AFAC3247F01985272C7BFCF13A0A983224B8C42DB46508ADE3657C88B1B9B5D544BE5F3346E81323D462B463793AAE72B0774891C2B9B8B0771A4001D184C7B7E742EC41647F6FB7"})
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
