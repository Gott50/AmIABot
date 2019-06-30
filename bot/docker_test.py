from bot import Bot

import json
import os
import traceback

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from urllib3.exceptions import NewConnectionError, ProtocolError, MaxRetryError


# Write your automation here
# Stuck ? Look at the github page or the examples in the examples folder


# If you want to enter your Instagram Credentials directly just enter
# username=<your-username-here> and password=<your-password> into InstaPy
# e.g like so InstaPy(username="instagram", password="test1234")


def selenium_driver(selenium_url):
    mobile_emulation = {"deviceName": "iPhone 5"}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument("disable-infobars")  # disabling infobars
    chrome_options.add_argument("--disable-extensions")  # disabling extensions
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems

    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    selenium_driver = webdriver.Remote(command_executor=selenium_url,
                                       desired_capabilities=chrome_options.to_capabilities())
    return selenium_driver


bot = Bot(selenium_local_session=False)
selenium_url = "http://%s:%d/wd/hub" % (os.environ.get('SELENIUM', 'selenium'), 4444)
bot.set_selenium_remote_session(selenium_url=selenium_url, selenium_driver=selenium_driver(selenium_url))

bot.act('http://web:5000')

# bot.end()
