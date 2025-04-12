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
    browser.add_cookie({"name": "MUSIC_U", "value": "00BDDFE1A594303FAE69C3A5F7CE9921123A29C9869D95363A8AD8B55B81943C784353B0781919724081D16488ACFF331AD7E6C437C7A482BF0C5D34BBBBE33A2006B4F2E4EF5BAE17F6A7DDE43DBD2FB6A170A493CA84A14028B1AAB4921CB20AFDD2BB2860AF26C4F307150FC82D228376E42C180BB64154C694A41F556656FF3079AEA5701B7FBC6ED504C5B9B26EDE303860EADFF5708097B7FD2154F80792B455AF9F02109A6913D9B36981C72655978B1B6EC29297BF1B47E3DC99A09C6830ABD614C2D1157B8EF222CE816619B450BF8F94083536FA82C6D0007FFCEB018324A740AD24441D81C33AEDCC1AFC88833BD17EA43E24F5249ED1005E77B74548FAB1313EE823B749062051B2633DB67067D7C9A7F338BAEBF2491D32E6FEF93ADE373879F84359C4C15137B045A6763E85DEA4377DF52C191399DA0C170569682F3A1AFC999871CDD04EF45B4453BF86412830CF8F9402161929B25D9D1942"})
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
