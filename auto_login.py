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
    browser.add_cookie({"name": "MUSIC_U", "value": "009CE3C79F3B402C34F14B83F100C8410029F4AF923D7ABF62FE9F7B1227E06FF047D912505FBBC8107AB18E96B6ED80AE89BAB6BACE22EA725F8504789F24FA4D3287F7ECDCB042C2ABA18D96216ADB5CEF0F1B9C0E30CF64F5E6D045C83AA0F28169DE52108D1C2B4F71D9ACD6567126AC886B658634D5FBF2D858135C7AB0A9BCDC8A9BC4737B040F25C95A0CD0D843A2D45D50AA11F0106691DB6A6CF49DF6FAB5792CAB2B3F361C3CE9D473CEA8AF585C5F8860480485A77075BC5171245B5492D656FA7D069EA472B59476DB8D45130C3CB90A767CBC2815D3E0385688276F43E75ACCA49A1546545F2FE2172F32D1DF1B571021679CE4B30299D820B615A0088031CD1242C8ADD788E0C2B0746B160111821DBB160D77C9FD0F8A1C68EB2CD9B1E4215D6F07007E0B0FCCB3F11669CFD574292431088854F0E103007ED4E9192AE19F470AF64F3140EA693C41CDC5D14F856BA0027241F8AE6F35A63537"})
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
