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
    browser.add_cookie({"name": "MUSIC_U", "value": "00612D458C6F0F5B2FB188F4B0E827C4942F02807B370D2859CCFA2BD1C6DDBEABF75FBA54CFC00F701D2DB023EE18AEFF74F220B48054D6E584EF9395B8EDD4184F8D626DB291E4919A03A969DB2103CA7A51FC96877D2189397F93839F32C4BE260F23A72020B9F43F4A03D6583D1DAB7AED816286F5F4F15BFCE0A66D8A750DD1F3789A1DD4DD16EB52B50BA80A9F62F61714E0375F32AA15654EBD0EFCC84D090FB8F9CA3CF9FBECB8F96BF51B24E8E4926DE345E72964F7C4A5E8A8E0CE9BD2C7A9707634171E545752477E593162B6030853948F3AAF58439D58E586639C9CB2C6E011D79D8397A616CABA1080F61820F9753B2AA7E8747C34E84B962BFD2A8F9FC60C35D65B6209E084C11826A9C357CDD4D53BE3298C75AB5D688785ECA9F106B9A0B3351B3BAF1B523A16C77C85D92A5A2535E71C1B88F4CDBBE70527C5907C60C6D940369114079D3A245F2B41DD3885BB23E020280F9A013EE2CCB3"})
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
