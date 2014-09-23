# -*- coding: utf-8 -*-

import unittest

from pyfunct.browsers import REGISTERED_DRIVERS
from pyfunct.actions import Actions
from pyfunct.context import config


class FunctTestCase(unittest.TestCase):
    """
        This is the class that must be overriden to create your tests.
        As it inherits from unittest.TestCase, you'll be able to use the
        asserting methods from it (assertEqual, assertIn, assertRaises, etc).
    """

    #: If you want to use a browser driver different than the one specified in
    #: `config.default_driver_name`, you can set this as the driver identifier.
    driver_name = None

    #: If you don't want to reuse the same browser window in through the test case, set it to False.
    reuse_browser = True

    def __init__(self, *args, **kwargs):
        self.__class__.browsers = []
        self.__class__.browser = None

        super(FunctTestCase, self).__init__(*args, **kwargs)

        # Makes all actions registered with `@action` accessible by
        # `self.actions` attribute.
        self.actions = Actions()

    def setUp(self):
        if self.__class__.browser is None and self.reuse_browser:
            self.__class__.browser = self.create_browser()

    def tearDown(self):
        cls = self.__class__
        for browser in cls.browsers:
            if self.reuse_browser and browser == cls.browser:
                browser.clear_session()
            else:
                self.close_browser(browser)

    def create_browser(self, driver_name=None, *args, **kwargs):
        """
            This instantiates a browser and returns it. It also adds the
            browser to `self.browsers`, in order to quit them automatically in
            the tear down.
        """
        driver_name = driver_name or config.default_driver_name
        browser = REGISTERED_DRIVERS[driver_name](*args, **kwargs)
        self.__class__.browsers.append(browser)
        return browser

    def close_browser(self, browser):
        browser.close()
        self.__class__.browsers.remove(browser)

    @classmethod
    def tearDownClass(cls):
        for browser in cls.browsers:
            browser.quit()
        cls.browsers = []

