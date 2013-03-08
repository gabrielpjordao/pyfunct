# -*- coding: utf-8 -*-

from pyfunct import config
from pyfunct.browsers import BaseBrowserDriver
from pyfunct.exceptions import PageNotLoadedException

splinter_available = True

try:
    from splinter import Browser
except ImportError:
    splinter_available = False


class SplinterBrowserDriver(BaseBrowserDriver):
    """
        This is a BrowserDriver based on splinter (http://splinter.cobrateam.info)
        that implements the BaseBrowserDriver API.

        To use it, you must have splinter installed on your env.

        For itself it's a browser driver that supports multiple browsing strategies,
        such as selenium, phantomjs, zope, etc.
    """

    driver_name = 'splinter'

    def __init__(self):
        super(SplinterBrowserDriver, self).__init__()
        if not splinter_available:
            raise ImportError("In order to use splinter Base Driver you have to "
                "install it. Check the instructions at http://splinter.cobrateam.info")
        self._browser = Browser(config.default_browser)

    @property
    def page_url(self):
        return self._browser.url

    @property
    def page_source(self):
        return self._browser.html

    @property
    def page_title(self):
        return self._browser.title

    def open_url(self, url):
        self._browser.visit(url)

    def quit(self):
        return self._browser.quit()

    def is_element_visible(self, element):
        return element.visible

    def get_element_text(self, element):
        return element.text

    def get_element_by_xpath(self, selector):
        return self._browser.find_by_xpath(selector)

    def get_element_by_css(self, selector):
        return self._browser.find_by_css(selector)

    def get_element_by_id(self, selector):
        return self._browser.find_by_id(selector)

    def get_element_by_tag(self, selector):
        return self._browser.find_by_tag(selector)

    def type(self, element, text, slowly=False):
        return element.type(text, slowly)

    def click(self, element):
        return element.click()

    def check(self, element):
        return element.check()

    def uncheck(self, element):
        return element.uncheck()

    def execute_script(self, script):
        return self._browser.evaluate_script(script)

    def wait_pageload(self, timeout=30):
        wait_interval = 0.05
        elapsed = 0

        while self.execute_script('document.readyState') != 'complete':
            self.wait(wait_interval)
            elapsed += wait_interval

            if elapsed > timeout:
                raise PageNotLoadedException

    def click_and_wait(self, element, timeout=30):
        self.click(element)
        self.wait_pageload(timeout)