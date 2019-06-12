import re
from datetime import datetime

import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType

from bot.settings import Settings


class Bot:
    def __init__(self,
                 username=None,
                 password=None,
                 selenium_local_session=True,
                 page_delay=25,
                 headless_browser=False,
                 proxy_address=None,
                 proxy_chrome_extension=None,
                 proxy_port=0,
                 print=print,
                 sleep_time=2):
        self.sleep_time = sleep_time
        self.print = print
        self.password = password
        self.username = username
        self.browser = None
        self.headless_browser = headless_browser
        self.proxy_address = proxy_address
        self.proxy_port = proxy_port
        self.proxy_chrome_extension = proxy_chrome_extension
        self.page_delay = page_delay
        self.answered = []
        self.selenium_local_session = selenium_local_session

        if selenium_local_session:
            self.set_selenium_local_session()

    def set_selenium_local_session(self):
        """Starts local session for a selenium server.
        Default case scenario."""
        chromedriver_location = Settings.chromedriver_location
        chrome_options = Options()
        chrome_options.add_argument('--dns-prefetch-disable')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--lang=de-DE')
        chrome_options.add_argument('--disable-setuid-sandbox')

        # this option implements Chrome Headless, a new (late 2017)
        # GUI-less browser. chromedriver 2.9 and above required
        if self.headless_browser:
            chrome_options.add_argument('--headless')
            # Replaces browser User Agent from "HeadlessChrome".
            user_agent = "Chrome"
            chrome_options.add_argument('user-agent={user_agent}'
                                        .format(user_agent=user_agent))
        capabilities = DesiredCapabilities.CHROME
        # Proxy for chrome
        if self.proxy_address and self.proxy_port > 0:
            prox = Proxy()
            proxy = ":".join([self.proxy_address, self.proxy_port])
            prox.proxy_type = ProxyType.MANUAL
            prox.http_proxy = proxy
            prox.socks_proxy = proxy
            prox.ssl_proxy = proxy
            prox.add_to_capabilities(capabilities)

        # add proxy extension
        if self.proxy_chrome_extension and not self.headless_browser:
            chrome_options.add_extension(self.proxy_chrome_extension)

        chrome_prefs = {
            'intl.accept_languages': 'de-DE'
        }
        chrome_options.add_experimental_option('prefs', chrome_prefs)
        try:
            self.browser = webdriver.Chrome(chromedriver_location,
                                            desired_capabilities=capabilities,
                                            chrome_options=chrome_options)
        except selenium.common.exceptions.WebDriverException as exc:
            self.print(exc)
            raise Exception('ensure chromedriver is installed at {}'.format(
                Settings.chromedriver_location))

        # prevent: Message: unknown error: call function result missing 'value'
        matches = re.match(r'^(\d+\.\d+)',
                           self.browser.capabilities['chrome']['chromedriverVersion'])
        if float(matches.groups()[0]) < Settings.chromedriver_min_version:
            raise Exception('chromedriver {} is not supported, expects {}+'.format(
                float(matches.groups()[0]), Settings.chromedriver_min_version))

        self.browser.implicitly_wait(self.page_delay)
        self.print('Session started - %s'
                   % (datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        return self

    def set_selenium_remote_session(self, selenium_url=''):
        """Starts remote session for a selenium server.
         Useful for docker setup."""
        self.browser = webdriver.Remote(
            command_executor=selenium_url,
            desired_capabilities=DesiredCapabilities.CHROME)

        message = "Session started!"

        self.print(self.username)
        self.print(message)
        self.print("initialization")
        self.print("info")
        self.print('')

        return self

    def act(self, url=None):
        driver = self.browser
        u = url or 'http://localhost:5000'
        self.print("url: %s" % u)
        driver.get(u)
        text = driver.find_elements_by_tag_name('body')[0].text
        self.print(text)

    def end(self):
        """Closes the current session"""
        try:
            self.browser.delete_all_cookies()
            self.browser.quit()
        except WebDriverException as exc:
            self.print('Could not locate Chrome: {}'.format(exc))

        self.print('Session ended - {}'.format(
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        self.print('-' * 20 + '\n\n')
