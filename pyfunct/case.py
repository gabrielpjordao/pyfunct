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

    def create_browser(self, driver_name=None, *args, **kwargs):
        """
            This instantiates a browser and returns it. It also adds the
            browser to `self.browsers`, in order to quit them automatically in
            the tear down.
        """
        driver_name = driver_name or config.default_driver_name
        browser = REGISTERED_DRIVERS[driver_name](*args, **kwargs)
        self.browsers.append(browser)
        return browser

    def __init__(self, *args, **kwargs):
        super(FunctTestCase, self).__init__(*args, **kwargs)

        # List of browsers to be quitted in tear down.
        self.browsers = []

        # Makes all actions registered with `@action` accessible by
        # `self.actions` attribute.
        self.actions = Actions()

    def setUp(self):
        self.browser = self.create_browser()

    def tearDown(self):
        for browser in self.browsers:
            browser.quit()
