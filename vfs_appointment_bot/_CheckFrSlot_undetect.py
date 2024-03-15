import sys
import logging
from cmath import exp
import email
import time
import datetime
import random

from logging.config import fileConfig
from _Timer import countdown
from _ConfigReader import _ConfigReader
from _TelegramClient import _TelegramClient

from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium_stealth import stealth
from selenium.webdriver.common.by import By

class _CheckFrSlot_undetect:
    def __init__(self):
        self._telegram_client = _TelegramClient()
        self._config_reader = _ConfigReader()

        self._init_web_driver()

    def _init_web_driver(self):
        # 连接到已打开的 Firefox 实例
        #options = webdriver.FirefoxOptions()
        #options.add_argument('-remote-debugging-port=9222')  # 9222 是 Firefox 默认的调试端口
        #options.add_argument('--disable-blink-features=AutomationControlled')
        #driver = webdriver.Firefox(options=options)
        #driver = webdriver.Firefox(executable_path = '/Users/haywood/Documents/Develop/python/geckodriver')

        #user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        options = uc.ChromeOptions() 
        #options.add_argument('--headless=new')
        options.add_argument("--start-maximized")
        #options.add_argument("user-agent={}".format(user_agent))

        #run in headless mode
        #options.add_argument("--headless")

        # disable the AutomationControlled feature of Blink rendering engine
        options.add_argument('--disable-blink-features=AutomationControlled')
         
        # disable pop-up blocking
        options.add_argument('--disable-popup-blocking')
         
        # start the browser window in maximized mode
        options.add_argument('--start-maximized')
         
        # disable extensions
        options.add_argument('--disable-extensions')
         
        # disable sandbox mode
        options.add_argument('--no-sandbox')
         
        # disable shared memory usage
        options.add_argument('--disable-dev-shm-usage')

        # Step 3: Rotate user agents 
        user_agents = [
            # Add your list of user agents here
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
        ]

        # select random user agent
        user_agent = random.choice(user_agents)

        # pass in selected user agent as an argument
        options.add_argument(f'user-agent={user_agent}')

        #options.add_experimental_option("excludeSwitches", ["enable-automation"])
        #options.add_experimental_option('useAutomationExtension', False)
        #options.headless = False  # Set headless to False to run in non-headless mode
        #options.add_experimental_option("debuggerAddress", "127.0.0.1:9515")
        self._web_driver = uc.Chrome(options=options)
        stealth(self._web_driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True
        )

        self._web_driver.get("https://www.g2.com/products/asana/reviews?__cf_chl_tk=Ksyz06hsSvzL6FKfYNxaAhPXG2xvAKO1ViVXe7WGJ4c-1710495286-0.0.1.1-1621") 
        
        #self._web_driver.get("https://visas-fr.tlscontact.com/appointment/gb/gbLON2fr/15060605") 
        #self._web_driver.maximize_window() 

        # Change the property value of the navigator for webdriver to undefined
        self._web_driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # Wait for page to load
        while self._web_driver.execute_script("return document.readyState") != "complete":
            pass
        time.sleep(2)
        self._web_driver.save_screenshot("opensea.png")

    def _refresh(self):
        print("current_url:" + self._web_driver.current_url)
        #self._web_driver.get(self._web_driver.current_url)
        #time.sleep(2)
        self._web_driver.refresh()

    def has_turnstile_wrapper(self):
        #print(self._web_driver.page_source)
        self._web_driver.switch_to.default_content()
        try:
            turnstile_wrapper = self._web_driver.find_element(By.XPATH,'//*[@id="turnstile-wrapper"]')
            if turnstile_wrapper:
                print("has turnstile_wrapper")
                countdown(15)
                self._web_driver.switch_to.frame(0)
                #//div[@id="challenge-stage"]/input[@type="checkbox"]
                try:
                    ctp_checkbox_label = self._web_driver.find_element(By.XPATH,'//div[@id="challenge-stage"]/div/label/input')
                    if ctp_checkbox_label:
                        ctp_checkbox_label.click()
                        _interval = random.randint(15,40)
                        countdown(_interval)
                        self.has_turnstile_wrapper()
                except Exception as e:
                    print("exception:"+str(e))
                    self.has_turnstile_wrapper() 
                    pass
            else:
                print("Success pass bot detection")
        except Exception as e:
            print("exception:"+str(e))
            countdown(15)
            self.has_turnstile_wrapper()
            pass
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

