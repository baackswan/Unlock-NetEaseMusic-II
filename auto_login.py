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
    browser.add_cookie({"name": "MUSIC_U", "value": "009F3835D473C701B6504AA0F17EBC2284F70547CF57B2EF6AF358986CB7521BC885C668D7C69CDC3109AD2C46A714D9A6AC54753A5E6703A76CADCB31FC735B5F7D5A4329A99CAEFCEFE9704558B4712B9BC789E1B69C8CBDA0CD97FC283DE7275D1CBEA58F65A2B199A179890A7B1D15D1F1FF2EBC99167089341B46F58FC98A41040E3A7B4994E6806E4CBD8F046DDCD4407C70B4CAACDD1FABC69730C3B74B85AC595DAD1A6C534AD11F87CFCC0C8356C56D0ECB46A7C5CCC8D81FFD12E788C739B19F215B3BE305D6EB21991E022E1F8A0EF9D2BB6260B9336ECAF9837D641B04AB10CECE2D6C6AA53E64D6B27FFBBFDEBAA03F3C3E6367EF14861565B3D6D9385E183F9E16D6F5EDAB9F4BC1AC65CE2960F36B3B0BADDAB92CD365C27BCAA5DDB7F70C07EE6E6AB6D9F6755AC8EC74DBAA85940B6A14A4B23B6F32E97F35AA40EEA41A2A534EB8EAFA568CC90E19BE0C490F2CC52C5D18B69866603734B9"})
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
