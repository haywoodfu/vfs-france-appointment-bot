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
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class _CheckFrSlot:
    def __init__(self):
        self._telegram_client = _TelegramClient()
        self._config_reader = _ConfigReader()

        self._init_web_driver()

    def _init_web_driver(self):
        # Link to the exsit Chrome instance
        options = webdriver.ChromeOptions()
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9515")
        self._web_driver = webdriver.Chrome(options=options)

    def _randomMoveWindow(self):
        # random scroll to prevent bot detection
        time.sleep(5)
        _height = random.randint(100,500)
        self._web_driver.execute_script("window.scrollTo(0, "+ str(_height) +")")
        print("window.scrollTo(0, "+ str(_height) +")")
        time.sleep(3)
        _height = random.randint(200,600)
        self._web_driver.execute_script("window.scrollTo(0, "+ str(_height) +")")
        print("window.scrollTo(0, "+ str(_height) +")")
        time.sleep(4)
        _height = random.randint(300,700)
        self._web_driver.execute_script("window.scrollTo(0, "+ str(_height) +")")
        print("window.scrollTo(0, "+ str(_height) +")")
        time.sleep(3)

    def _refresh(self):
        print("current_url:" + self._web_driver.current_url)
        self._web_driver.refresh()
        self._randomMoveWindow()
        # add click to precent bot detection
        try:
            _banner = self._web_driver.find_element("class name", "tls-popup-display--container")
            self._web_driver.execute_script("arguments[0].click();",_banner)
        except:
            print("there is no tls-popup-display--container")
            pass
        time.sleep(1)

    def _tryLogin(self):
        try:
            _login_button = self._web_driver.find_element(By.XPATH,'//*[@id="kc-login"]')
            if _login_button:
                print("begin login")
                self._login()
        except:
            # not in login page
            print("not in login page")
            pass

    def _login(self):
        _section_header = "VFS"
        _email = self._config_reader.read_prop(_section_header, "vfs_email");
        _password = self._config_reader.read_prop(_section_header, "vfs_password");

        print("Logging in with email: {}".format(_email))
        logging.debug("Logging in with email: {}".format(_email))

        # logging in
        countdown(10)

        # sleep provides sufficient time for all the elements to get visible
        _email_input = self._web_driver.find_element(By.XPATH,"//input[@id='username']")
        _email_input.send_keys(_email)
        time.sleep(2)
        _password_input = self._web_driver.find_element(By.XPATH,"//input[@id='password']")
        _password_input.send_keys(_password)
        time.sleep(3)
        _login_button = self._web_driver.find_element(By.XPATH,"//button[@id='kc-login']")
        self._web_driver.execute_script("arguments[0].click();",_login_button)
        print("click login button")
        countdown(30)
        
        # check is blocked by bot
        self.has_turnstile_wrapper()
        

    def has_turnstile_wrapper(self):
        # check if blocked by bot detection
        self._web_driver.switch_to.default_content()
        try:
            turnstile_wrapper = self._web_driver.find_element(By.XPATH,'//div[@id="turnstile-wrapper"]')
            if turnstile_wrapper:
                print("has turnstile_wrapper")

                print("_randomMoveWindow")
                self._randomMoveWindow()
                _interval = random.randint(5,20)
                countdown(_interval)

                print("find challenge-stage")
                self._web_driver.switch_to.frame(0)
                #//div[@id="challenge-stage"]/input[@type="checkbox"]
                try:
                    ctp_checkbox_label = self._web_driver.find_element(By.XPATH,'//div[@id="challenge-stage"]/div/label/input')
                    if ctp_checkbox_label:
                        ctp_checkbox_label.click()
                        _interval = random.randint(30,50)
                        countdown(_interval)
                        self.has_turnstile_wrapper()
                except Exception as e:
                    print("exception:"+str(e))
                    self.has_turnstile_wrapper() 
                    pass
            else:
                print("Success pass bot detection")
        except Exception as e:
            self._web_driver.switch_to.default_content()
            print("there is no bot block")
            #print("exception:"+str(e))
            pass

    def has_validate_slot(self):
        # print(self._web_driver.page_source)
        self.has_turnstile_wrapper()
        self._tryLogin()
        try:
            time_slot = self._web_driver.find_element("class name", "tls-time-group--slot")
        except:
            logging.debug("There is no time_slot")
            try:
                ctp_blocked_label = self._web_driver.find_element(By.XPATH,'/html/body/pre')
                if ctp_blocked_label:
                    logging.debug("IP is blocked, sleep 30 mins")
                    print("IP is blocked, sleep 30 mins")
                    # IP blocked,wait 30 mins
                    countdown(1800)
            except NoSuchElementException:
                pass
            self._refresh()
            raise Exception("There is no time_slot")   
        # check if there is a pop dialog 
        try:
            pop_content = self._web_driver.find_element("class name", "tls-popup-display--content")
            if pop_content:
                #self._telegram_client.send_message("There is no validate slot")
                logging.debug("There is no validate slot")
                self._refresh()
                raise Exception("There is no validate slot")
            else:
                self._telegram_client.send_message("has validate slot")
                logging.debug("has validate slot")
        except NoSuchElementException:
            self._telegram_client.send_message("has validate slot")
            logging.debug("has validate slot")
            pass
        except Exception as e:
            #self._refresh()
            logging.debug("exception:"+str(e))
            raise e

