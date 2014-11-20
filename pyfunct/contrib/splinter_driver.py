# -*- coding: utf-8 -*-

from functools import wraps
from pyfunct import config
from pyfunct.browsers import BaseBrowserDriver
from pyfunct.exceptions import (
    PageNotLoadedException,
    ActionNotPerformableException)

splinter_available = True

try:
    from splinter import Browser
except ImportError:
    splinter_available = False


def element_action(func):
    """
        Decorator that provides a shortcut for performing browser actions into
        elements, such as click, mouse_over, etc.
        When used, it should receive either an element or a string as the first
        parameter (after self). If It's a string, it should be an alias to
        a page element, and the action will be performed into this element.

        It also executes `_handle_empty_element_action` before performing
        the action.
    """
    @wraps(func)
    def wrapper(self, element, *args, **kwargs):
        if isinstance(element, str):
            element = self.get_page_element(element)
        self._handle_empty_element_action(element)
        return func(self, element, *args, **kwargs)
    return wrapper


class SplinterBrowserDriver(BaseBrowserDriver):
    """
        This is a BrowserDriver for splinter
        (http://splinter.cobrateam.info)
        that implements the BaseBrowserDriver API.

        To use it, you must have splinter installed on your env.

        For itself it's a browser driver that supports multiple browsing
        technologies such as selenium, phantomjs, zope, etc.
    """

    driver_name = 'splinter'

    def __init__(self, *args, **kwargs):
        _args = args or (config.default_browser, )
        super(SplinterBrowserDriver, self).__init__()
        if not splinter_available:
            raise ImportError(
                "In order to use splinter Base Driver you have to install it. "
                "Check the instructions at http://splinter.cobrateam.info")
        self._browser = Browser(*_args, **kwargs)

    def _handle_empty_element_action(self, element):
        if not element:
            raise ActionNotPerformableException(
                "The action couldn't be perfomed because the element couldn't "
                "be found; Try checking if your element"
                "selector is correct and if the page is loaded properly.")

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
        self._browser.driver.get(url)

    def close(self):
        return self._browser.driver.close()

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

    @element_action
    def type(self, element, text, slowly=False):
        return element.type(text, slowly)

    @element_action
    def fill(self, element, text):
      return element.fill(text)

    @element_action
    def clear(self, element):
      self.fill(element, '')

    @element_action
    def click(self, element):
        return element.click()

    @element_action
    def choose(self, element, value):
        return element.choose(value)

    @element_action
    def select(self, element, value):
        return element.select(value)

    @element_action
    def select_by_text(self, element, text):
        return element.find_by_xpath(
            'option[normalize-space(.)="%s"]' % text).first._element.click()

    @element_action
    def check(self, element):
        return element.check()

    @element_action
    def uncheck(self, element):
        return element.uncheck()

    @element_action
    def mouse_over(self, element):
        return element.mouse_over()

    @element_action
    def mouse_out(self, element):
        return element.mouse_out()

    def reload(self):
        return self._browser.reload()

    def go_back(self):
        return self._browser.back()

    def go_forward(self):
        return self._browser.forward()

    def execute_script(self, script):
        """This method is deprecated. Use `execute_javascript` instead.
        """
        return self._browser.evaluate_script(script)

    def execute_javascript(self, script):
        return self._browser.evaluate_script(script)

    def get_iframe(self, iframe_id):
        return self._browser.get_iframe(iframe_id)

    def get_alert(self):
        return self._browser.get_alert()

    def attach_file(self, input_name, file_path):
        return self._browser.attach_file(input_name, file_path)

    def wait_pageload(self, timeout=30):
        wait_interval = 0.05
        elapsed = 0

        while self.execute_javascript('document.readyState') != 'complete':
            self.wait(wait_interval)
            elapsed += wait_interval

            if elapsed > timeout:
                raise PageNotLoadedException

    def click_and_wait(self, element, timeout=30):
        self.click(element)
        self.wait_pageload(timeout)

    def clear_session(self):
      self._browser.driver.delete_all_cookies()

