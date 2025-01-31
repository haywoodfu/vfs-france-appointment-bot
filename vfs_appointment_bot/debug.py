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
from _CheckFrSlot import _CheckFrSlot

from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


if __name__ == "__main__":
    count = 1
    fileConfig('config/logging.ini')
    logging = logging.getLogger(__name__);
    
    _CheckFrSlot = _CheckFrSlot()
    _config_reader = _ConfigReader()
    _begin = _config_reader.read_prop("DEFAULT", "interval")

    

    # 不采用自动登录的方式，直接在chrome上登录好，这个脚本只负责刷新slot
    logging.info("Starting VFS Appointment Bot")
    while True:
        try:
            logging.info("Running VFS Appointment Bot: Attempt#{}".format(count))
            _CheckFrSlot.has_validate_slot()

            _interval = random.randint(int(_begin),280)

            logging.debug("Sleeping for {} seconds".format(_interval))
            countdown(int(_interval))
        except Exception as e:
            logging.info(e.args[0] + ". Please check the logs for more details")
            logging.debug(e, exc_info=True, stack_info=True)

            _interval = random.randint(int(_begin),280)
            countdown(int(_interval))
            pass
        print("\n")
        count += 1
