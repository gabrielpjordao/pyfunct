# -*- coding: utf-8 -*-

from time import sleep

from pyfunct.exceptions import (
    SelectorTypeNotSupportedException,
    InvalidUrlException,
    UnregisteredElementException)
from pyfunct.pages import REGISTERED_PAGES
from pyfunct import config

# Should contain all browsers that were registered and are available.
# `BrowserDriverMetaclass` takes care of adding the browsers here.
REGISTERED_DRIVERS = {}


class BrowserDriverMetaclass(type):
    """
        Browser Driver Metaclass. It makes any browser that extends
        `BaseBrowserDriver` to be added to `REGISTERED_DRIVERS`, making it
        usable by any `FunctTestCase`.
    """

    def __init__(cls, name, bases, attributes):

        try:
            driver_name = attributes['driver_name']
        except KeyError:
            raise NotImplementedError(
                "You must specify the driver_name for %s." % cls.__name__)

        if driver_name is not None:
            REGISTERED_DRIVERS[driver_name] = cls

        return super(BrowserDriverMetaclass, cls).__init__(name, bases,
                                                           attributes)


class BaseBrowserDriver(object):
    """
        This is the API for Browser Drivers.
    """

    __metaclass__ = BrowserDriverMetaclass

    driver_name = None
    """
        This must be set to a string as the browser driver identifier.
    """

    _current_page = None

    def __init__(self):
        """
            Defines the methods used to select elements.
        """
        self.selection_methods = {
            'xpath': self.get_element_by_xpath,
            'css': self.get_element_by_css,
            'id': self.get_element_by_id,
            'tag': self.get_element_by_tag
        }

    @property
    def page_url(self):
        """
            Current's page url.
        """
        raise NotImplementedError(
            "This browser doesn't support accessing the page url")

    @property
    def page_source(self):
        """
            Current's page source code.
        """
        raise NotImplementedError(
            "This browser doesn't support accessing the page source")

    @property
    def page_title(self):
        """
            Current's page title.
        """
        raise NotImplementedError(
            "This browser doesn't support accessing the page title")

    def switch_page(self, page_name):
        """
            Switchs to a new page, making it's elements accessible.

            It just sets the current page, taking off the elements from the
            previous page and adding the new ones, but doesn't change the
            browser active page.
        """
        self._current_page = REGISTERED_PAGES[page_name]
        return self._current_page

    def open_page(self, page_name, *args, **kwargs):
        """
            Calls `switch_page`, which will load the new page instance and then
            goes with the browser to the new page.
        """
        self.switch_page(page_name)

        url = self._current_page.get_url(*args, **kwargs)

        if not url.startswith('/'):
            raise InvalidUrlException

        url = config.base_url + url

        return self.open_url(url)

    def reload(self):
        """
            Reloads the page
        """
        raise NotImplementedError("This page doesn't support reloading;")

    def go_back(self):
        """
            Goes back in history
        """
        raise NotImplementedError("This page doesn't support going back")

    def go_forward(self):
        """
            Goes forward in history
        """
        raise NotImplementedError("This page doesn't support going forward")

    def __getitem__(self, key):
        """
            Offers a shortcut for getting page elements.
        """
        return self.get_page_element(key)

    def click(self, element):
        """
            Clicks an element.
        """
        raise NotImplementedError(
            "This browser doesn't support clicking elements")

    def check(self, element):
        """
            Checks a checkbox element.
        """
        raise NotImplementedError(
            "This browser doesn't support checking elements")

    def uncheck(self, element):
        """
            Unchecks a checkbox element.
        """
        raise NotImplementedError(
            "This browser doesn't support unchecking elements")

    def mouse_over(self, element):
        """
            Simulates an element mouse over.
        """
        raise NotImplementedError("This browser doesn't support mouse over.")

    def open_url(self, url):
        """
            Opens an URL and returns it's response.
        """
        raise NotImplementedError("This browser doesn't support opening urls")

    def quit(self):
        """
            Quits the browser.
        """
        raise NotImplementedError("This browser doesn't support quitting")

    def is_element_present(self, element):
        """
            Returns `True` if an element is present in the page source,
            even if it's hidden. Otherwise, returns `False`.
        """
        raise NotImplementedError(
            "This browser doesn't support checking elements presence")

    def is_element_visible(self, element):
        """
            Returns `True` if an element is present the page source and
            it's visible. Otherwise, returns `False`.
        """
        raise NotImplementedError(
            "This browser doesn't support checking elements visibility")

    def get_element_text(self, element):
        """
            Returns the text for an element.
        """
        raise NotImplementedError(
            "This browser doesn't support getting text from elements")

    def get_element(self, selector, selection_type='xpath'):
        """
            Chooses a method based on `selection_type` and uses this method
            to get the element for `selector` selector value.
        """
        try:
            return self.selection_methods[selection_type](selector)
        except KeyError:
            raise SelectorTypeNotSupportedException

    def get_page_element(self, alias):
        """
            Gets an element from the currently active page, based on it's
            `alias`.
        """
        try:
            page_element = self._current_page.elements[alias]
        except KeyError:
            raise UnregisteredElementException

        selector = page_element['selector']
        selection_type = page_element['selection_type']

        return self.get_element(selector, selection_type)

    def get_element_by_xpath(self, selector):
        """
            Gets an element using an xPath selector.
        """
        raise NotImplementedError(
            "This browser doesn't support getting elements by xpath")

    def get_element_by_css(self, selector):
        """
            Gets an element using an CSS selector.
        """
        raise NotImplementedError(
            "This browser doesn't support getting elements by css")

    def get_element_by_id(self, selector):
        """
            Gets an element using it's html ID.
        """
        raise NotImplementedError(
            "This browser doesn't support getting elements by id")

    def get_element_by_tag(self, selector):
        """
            Gets an element, selecting it by it's tag.
        """
        raise NotImplementedError(
            "This browser doesn't support getting elements by tag")

    def type(self, element, text, slowly=False):
        """
            Enters a text into an input element. If slowly is `True`, it should
            press one key at a time, simulating a user input.
        """
        raise NotImplementedError(
            "This browser doesn't support typing texts into elements.")

    def execute_javascript(self, script):
        """
            Should execute javascript in the current browser and then
            return the execution result.
        """
        raise NotImplementedError(
            "This browser doesn't support executing javascript.")

    def wait(self, seconds):
        """
            Just a utilitarian method to wait.
        """
        sleep(seconds)

    def wait_pageload(self, timeout=30):
        """
            Checks if the current page is loaded, until timeout is reached.
        """
        raise NotImplementedError(
            "This browser doesn't support checking if pageload is complete.")

    def click_and_wait(self, element, timeout=30):
        """
            Clicks an element and waits for the page to load.
        """
        raise NotImplementedError(
            "This browser doesn't support clicking an element and waiting")
