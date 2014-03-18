import unittest

from mock import Mock
from pyfunct.browsers import REGISTERED_DRIVERS, BaseBrowserDriver
from pyfunct import Page, config
from pyfunct.exceptions import InvalidUrlException

class BrowserDriverMetaclassTestCase(unittest.TestCase):

    def test_registering_a_new_browser_successfully(self):
        """
            This basicly tests `BrowserDriverMetaClass` responsibilities
        """

        class MyNewDriver(BaseBrowserDriver):
            driver_name = 'new_browser_driver'

        new_driver = REGISTERED_DRIVERS['new_browser_driver']()
        self.assertIsInstance(new_driver, MyNewDriver)

    def test_registering_a_new_browser_without_name(self):
        with self.assertRaises(NotImplementedError):
            class UnnamedDriver(BaseBrowserDriver):
                """
                    This browser has no name, so it should raise the exception
                """
                pass


class BaseBrowserDriverTestCase(unittest.TestCase):

    def test_switch_page(self):
        class SwitchedPage(Page):
            page_name = 'page_i_wanna_switch'

        class SwitchPageDriver(BaseBrowserDriver):
            driver_name = 'page_switcher_tester'

        driver = SwitchPageDriver()
        self.assertEqual(driver._current_page, None)

        driver.switch_page('page_i_wanna_switch')

        self.assertIsInstance(driver._current_page, SwitchedPage)

    def test_open_page_successfully(self):

        class PageToOpen(Page):
            page_name = 'page_i_will_go'

            def get_url(self, article_id):
                return '/article/%i' % article_id

        class OpenPageDriver(BaseBrowserDriver):
            driver_name = 'page_opener_driver'

            def open_url(self, url):
                """
                    Mocks it in order to check if it was called properly
                """
                return 'Opened %s' % url

        driver = OpenPageDriver()

        response = driver.open_page('page_i_will_go',article_id=3)

        # Asserts that the page has been switched properly
        self.assertIsInstance(driver._current_page, PageToOpen)

        self.assertEqual(response, 'Opened %s' % config.base_url + '/article/3')

    def test_a_page_with_invalid_url_cant_be_opened(self):

        class PageWithInvalidUrl(Page):

            page_name = 'page_with_invalid_url'

            def get_url(self):
                return 'without_slash_start'

        class InvalidURLBrowserTester(BaseBrowserDriver):
            driver_name = 'invalid_url_driver'

        driver = InvalidURLBrowserTester()

        with self.assertRaises(InvalidUrlException):
            driver.open_page('page_with_invalid_url')

    def test_a_page_that_provides_full_url(self):

        class PageWithFullUrl(Page):

            page_name = 'page_with_full_url'
            provides_full_url = True

            def get_url(self):
                return 'http://myurl.com'

        class FullURLBrowserTester(BaseBrowserDriver):
            driver_name = 'full_url_driver'

            def open_url(self, url):
                """
                    Mocks it in order to check if it was called properly
                """
                return url

        driver = FullURLBrowserTester()

        response = driver.open_page('page_with_full_url')
        self.assertIsInstance(driver._current_page, PageWithFullUrl)

        self.assertEqual(response, 'http://myurl.com')

    def test_getting_elements_by_different_selection_types(self):

        class GetElementTestDriver(BaseBrowserDriver):
            driver_name = 'get_element_driver'

            def get_element_by_xpath(self, selector):
                return 'xpath(%s)' % selector

            def get_element_by_css(self, selector):
                return 'css(%s)' % selector

            def get_element_by_id(self, selector):
                return 'id(%s)' % selector

            def get_element_by_tag(self, selector):
                return 'tag(%s)' % selector

        driver = GetElementTestDriver()

        selection_types = ('xpath', 'css', 'id', 'tag')

        selector = 'anything'

        for selection_type in selection_types:
            element = driver.get_element(selector, selection_type)
            self.assertEqual(element, '%s(%s)' % (selection_type, selector))

    def test_get_page_element(self):
        class PageWithElement(Page):
            page_name = 'page_with_element'

            @property
            def elements_selectors(self):
                return [
                    ('the-alias', '//selector', 'xpath')
                ]

        class GetPageElementDriver(BaseBrowserDriver):

            driver_name = 'get_page_element_driver'

            def get_element_by_xpath(self, selector):
                return 'Element Got: selector=%s, selection_type=xpath' % (selector)

        driver = GetPageElementDriver()
        driver.switch_page('page_with_element')

        element = driver.get_page_element('the-alias')

        expected_element = 'Element Got: selector=//selector, selection_type=xpath'

        self.assertEqual(element, expected_element)

    def test_get_page_element_by_key_access(self):
        class PageWithElement(Page):
            page_name = 'page_with_element'

            @property
            def elements_selectors(self):
                return [
                    ('the-alias', '//selector', 'xpath')
                ]

        class GetPageElementDriver(BaseBrowserDriver):

            driver_name = 'get_page_element_driver'

            def get_element_by_xpath(self, selector):
                return 'Element Got: selector=%s, selection_type=xpath' % (selector)

        driver = GetPageElementDriver()
        driver.switch_page('page_with_element')

        element = driver['the-alias']

        expected_element = 'Element Got: selector=//selector, selection_type=xpath'

        self.assertEqual(element, expected_element)

    def test_is_element_present_string_true(self):
        browser = BaseBrowserDriver()
        element = Mock()
        browser.get_page_element = Mock(return_value=element)
        browser.get_page_element.called_once_with(element)
        self.assertTrue(browser.is_element_present('page element'))

    def test_is_element_present_string_false(self):
        browser = BaseBrowserDriver()
        element = []
        browser.get_page_element = Mock(return_value=element)
        browser.get_page_element.called_once_with(element)
        self.assertFalse(browser.is_element_present('page element'))

    def test_is_element_present_element_true(self):
        browser = BaseBrowserDriver()
        self.assertTrue(browser.is_element_present(Mock()))

    def test_is_element_present_element_false(self):
        browser = BaseBrowserDriver()
        self.assertFalse(browser.is_element_present([]))
