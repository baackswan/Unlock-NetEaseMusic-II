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
    browser.add_cookie({"name": "MUSIC_U", "value": "00344E23462D9CB9E19C3B759A9E85935AA585FE9A6D02FFE378D1F19B8565789B7FEFFEAC4D86E422CDC166836ADF6798D959FE85C9458986E87F90C656D2BF95AEC82B963FCD326733ACDA148E4994076549C2D89CD2138972809C4E165766DEDE2C60499DF00AECF4633C182582738E16AD65E24E00C7E7D7D91F1D1D5ECDD7EEAD946E6CF80391298290A0A4DC4DD453E4BC7CDFAA625F90836E80CD301BC14CBC12935DB885A4000B57022EBD2AF1F2612918CEAA5725B5FAE832519CFE6AE414F5E8B50DB325672F387173FBDA1EEF246EC6737A552196BB0BF16BCAAF5FC63EFD75709E2E6FC6AB7FFD06734881A0689D35C1D1E56E3C1F523349EA062A7BD2474FF1944707D71128B041D106AA3D47D9BEE4627DF8E1D35031023A136824EE1CE10B94DC6A1932FC1C6E4FE091026B71414AE9348FD0BB823FDE182325991BE1165DECD788EEC5BE3109895A774C011D32AB510009C42254EB4802C22D"})
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
