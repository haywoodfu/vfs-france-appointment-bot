import sys
import logging
from cmath import exp
import email
import time
import datetime

from logging.config import fileConfig
from _Timer import countdown
from _ConfigReader import _ConfigReader
from _TelegramClient import _TelegramClient

from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

_web_driver = None
_telegram_client = None

def _init_web_driver(self):
    global _web_driver
    # 连接到已打开的 Firefox 实例
    #options = webdriver.FirefoxOptions()
    #options.add_argument('-remote-debugging-port=9222')  # 9222 是 Firefox 默认的调试端口
    #options.add_argument('--disable-blink-features=AutomationControlled')
    #driver = webdriver.Firefox(options=options)
    #driver = webdriver.Firefox(executable_path = '/Users/haywood/Documents/Develop/python/geckodriver')

    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9515")
    _web_driver = webdriver.Chrome(options=options)

def _has_validate_slot(self):
    global _telegram_client
    try:
        pop_content = _web_driver.find_element_by_class_name("tls-popup-display--content")
        if pop_content == None:
            _telegram_client.send_message("has validate slot")
            logging.debug("has validate slot")
        else:
            _web_driver.refresh()
            logging.debug("There is no validate slot")
            raise Exception("There is no validate slot")
    except:
        logging.debug("There is no validate slot")
        raise Exception("There is no validate slot")

# def _login(self):
    # 使用 RemoteWebDriver 操作已打开的 浏览器 实例
    #driver.get('https://auth.visas-fr.tlscontact.com/auth/realms/atlas/protocol/openid-connect/auth?response_type=code&client_id=web_app&scope=openid%20roles%20atlas%20web-origins%20email%20offline_access%20profile%20address%20phone&state=A-YpBIzDctSBJLH-Y0YZod89sg8-KbUN13rxa_UYq6w%3D&redirect_uri=https://visas-fr.tlscontact.com/appointment/gb/gbLON2fr/15060605')
    #driver.get('https://www.baidu.com')
    ## logging in
    #time.sleep(10)
#
    ## sleep provides sufficient time for all the elements to get visible
    #_email_input = driver.find_element_by_xpath("//input[@id='username']")
    #_email_input.send_keys("futuresu44@gmail.com")
    #_password_input = driver.find_element_by_xpath("//input[@id='password']")
    #_password_input.send_keys("Susan363196@")
#
    #_login_button = driver.find_element_by_xpath("//button[@id='kc-login']")
    #driver.execute_script("arguments[0].click();",_login_button)

# def _check_valid_slot(self):

if __name__ == "__main__":
    count = 1
    fileConfig('config/logging.ini')
    logging = logging.getLogger(__name__);
    
    _telegram_client = _TelegramClient()
    _config_reader = _ConfigReader()
    _interval = _config_reader.read_prop("DEFAULT", "interval")
    logging.debug("Interval: {}".format(_interval))

    self._init_web_driver()

    # 不采用自动登录的方式，直接在chrome上登录好，这个脚本只负责刷新slot
    logging.info("Starting VFS Appointment Bot")
    while True:
        try:
            logging.info("Running VFS Appointment Bot: Attempt#{}".format(count))
            self._has_validate_slot()
            logging.debug("Sleeping for {} seconds".format(_interval))
            countdown(int(_interval))
        except Exception as e:
            logging.info(e.args[0] + ". Please check the logs for more details")
            logging.debug(e, exc_info=True, stack_info=True)
            countdown(int(60))
            pass
        print("\n")
        count += 1
