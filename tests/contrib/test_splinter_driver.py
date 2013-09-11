from mock import patch, Mock

from splinter.element_list import ElementList
from pyfunct import SplinterBrowserDriver, Page
from pyfunct.exceptions import (
    PageNotLoadedException,
    ActionNotPerformableException)
import unittest


class SplinterBrowserDriverTestCase(unittest.TestCase):

    def _get_driver(self, mocked_browser):
        """
            Sets `_browser` to the mocked browser to allow mocking the original
            splinter behavior, in order to test. It's just a util function.
        """
        driver = SplinterBrowserDriver()
        driver._browser = mocked_browser
        return driver

    @patch('pyfunct.contrib.splinter_driver.Browser')
    def test_page_url(self, mocked_browser):

        expected = 'some_url'

        mocked_browser.url = expected

        driver = self._get_driver(mocked_browser)

        self.assertEqual(driver.page_url, expected)

    @patch('pyfunct.contrib.splinter_driver.Browser')
    def test_page_source(self, mocked_browser):

        expected = '<html></html>'

        mocked_browser.html = expected

        driver = self._get_driver(mocked_browser)

        self.assertEqual(driver.page_source, expected)

    @patch('pyfunct.contrib.splinter_driver.Browser')
    def test_page_title(self, mocked_browser):

        expected = 'Pyfunct - Testing Title'

        mocked_browser.title = expected

        driver = self._get_driver(mocked_browser)

        self.assertEqual(driver.page_title, expected)

    @patch('pyfunct.contrib.splinter_driver.Browser')
    def test_open_url(self, mocked_browser):

        driver = self._get_driver(mocked_browser)

        url = 'some_url'

        driver.open_url(url)

        mocked_browser.driver.get.assert_called_once_with(url)

    @patch('pyfunct.contrib.splinter_driver.Browser')
    def test_quit(self, mocked_browser):

        driver = self._get_driver(mocked_browser)

        driver.quit()

        mocked_browser.quit.assert_called()

    @patch('pyfunct.contrib.splinter_driver.Browser')
    def test_reload(self, mocked_browser):

        driver = self._get_driver(mocked_browser)

        driver.reload()

        mocked_browser.reload.assert_called()

    @patch('pyfunct.contrib.splinter_driver.Browser')
    def test_go_forward(self, mocked_browser):

        driver = self._get_driver(mocked_browser)

        driver.go_forward()

        mocked_browser.forward.assert_called()

    @patch('pyfunct.contrib.splinter_driver.Browser')
    def test_go_back(self, mocked_browser):

        driver = self._get_driver(mocked_browser)

        driver.go_back()

        mocked_browser.back.assert_called()

    @patch('pyfunct.contrib.splinter_driver.Browser')
    def test_is_element_visible(self, mocked_browser):

        driver = self._get_driver(mocked_browser)

        element = Mock()
        element.visible = True

        visible = driver.is_element_visible(element)

        self.assertEqual(visible, True)

    @patch('pyfunct.contrib.splinter_driver.Browser')
    def test_get_element_text(self, mocked_browser):

        driver = self._get_driver(mocked_browser)

        text = 'SomeText'

        element = Mock()
        element.text = text

        element_text = driver.get_element_text(element)

        self.assertEqual(element_text, text)

    @patch('pyfunct.contrib.splinter_driver.Browser')
    def test_get_element_by_xpath(self, mocked_browser):

        driver = self._get_driver(mocked_browser)

        selector = 'some_selector'

        driver.get_element_by_xpath(selector)

        mocked_browser.find_by_xpath.assert_called_with(selector)

    @patch('pyfunct.contrib.splinter_driver.Browser')
    def test_get_element_by_css(self, mocked_browser):

        driver = self._get_driver(mocked_browser)

        selector = 'some_selector'

        driver.get_element_by_css(selector)

        mocked_browser.find_by_css.assert_called_with(selector)

    @patch('pyfunct.contrib.splinter_driver.Browser')
    def test_get_element_by_id(self, mocked_browser):

        driver = self._get_driver(mocked_browser)

        selector = 'some_selector'

        driver.get_element_by_id(selector)

        mocked_browser.find_by_id.assert_called_with(selector)

    @patch('pyfunct.contrib.splinter_driver.Browser')
    def test_get_element_by_tag(self, mocked_browser):

        driver = self._get_driver(mocked_browser)

        selector = 'some_selector'

        driver.get_element_by_tag(selector)

        mocked_browser.find_by_tag.assert_called_with(selector)

    @patch('pyfunct.contrib.splinter_driver.Browser')
    def test_type(self, mocked_browser):

        driver = self._get_driver(mocked_browser)

        text = 'Some Text'
        element = Mock()

        driver.type(element, text, slowly=True)

        element.type.assert_called_once_with(text, True)

    @patch('pyfunct.contrib.splinter_driver.Browser')
    def test_click(self, mocked_browser):

        driver = self._get_driver(mocked_browser)

        element = Mock()

        driver.click(element)

        element.click.assert_called()

    @patch('pyfunct.contrib.splinter_driver.Browser')
    def test_mouse_over(self, mocked_browser):

        driver = self._get_driver(mocked_browser)

        element = Mock()

        driver.mouse_over(element)

        element.mouse_over.assert_called()

    @patch('pyfunct.contrib.splinter_driver.Browser')
    def test_check(self, mocked_browser):

        driver = self._get_driver(mocked_browser)

        element = Mock()

        driver.check(element)

        element.check.assert_called()

    @patch('pyfunct.contrib.splinter_driver.Browser')
    def test_uncheck(self, mocked_browser):

        driver = self._get_driver(mocked_browser)

        element = Mock()

        driver.uncheck(element)

        element.uncheck.assert_called()

    @patch('pyfunct.contrib.splinter_driver.Browser')
    def test_execute_script(self, mocked_browser):

        driver = self._get_driver(mocked_browser)

        script = '<script></script>'
        expected_result = 'Script result'

        driver.execute_script(script)
        result = mocked_browser.execute_script.return_value = expected_result

        mocked_browser.evaluate_script.assert_called_once_with(script)
        self.assertEqual(expected_result, result)

    @patch('pyfunct.contrib.splinter_driver.Browser')
    def test_wait_pageload(self, mocked_browser):

        driver = self._get_driver(mocked_browser)
        mocked_browser.evaluate_script.return_value = 'unraedy'

        with self.assertRaises(PageNotLoadedException):
            driver.wait_pageload(timeout=0.01)

    @patch('pyfunct.contrib.splinter_driver.Browser')
    def test_click_and_wait(self, mocked_browser):

        driver = self._get_driver(mocked_browser)

        element = Mock()
        timeout = 10

        driver.click = Mock()
        driver.wait_pageload = Mock()

        driver.click_and_wait(element, timeout=timeout)

        driver.click.assert_called()
        driver.wait_pageload.assert_called_once_with(timeout)

    @patch('pyfunct.contrib.splinter_driver.Browser')
    def test_click_action_with_not_found_element_cannot_be_performed(
        self,
        mocked_browser
    ):
        driver = self._get_driver(mocked_browser)
        element = ElementList([])
        with self.assertRaises(ActionNotPerformableException):
            driver.click(element)

    @patch('pyfunct.contrib.splinter_driver.Browser')
    def test_check_action_with_not_found_element_cannot_be_performed(
        self,
        mocked_browser
    ):
        driver = self._get_driver(mocked_browser)
        element = ElementList([])
        with self.assertRaises(ActionNotPerformableException):
            driver.check(element)

    @patch('pyfunct.contrib.splinter_driver.Browser')
    def test_uncheck_action_with_not_found_element_cannot_be_performed(
        self,
        mocked_browser
    ):
        driver = self._get_driver(mocked_browser)
        element = ElementList([])
        with self.assertRaises(ActionNotPerformableException):
            driver.uncheck(element)

    @patch('pyfunct.contrib.splinter_driver.Browser')
    def test_type_action_with_not_found_element_cannot_be_performed(
        self,
        mocked_browser
    ):
        driver = self._get_driver(mocked_browser)
        element = ElementList([])
        with self.assertRaises(ActionNotPerformableException):
            driver.type(element, 'some-text')

    @patch('pyfunct.contrib.splinter_driver.Browser')
    def test_element_action_decorator_gets_elements_by_alias_str(
        self,
        mocked_browser
    ):

        selector = 'some_selector'
        alias = 'some_alias'
        test_page_name = 'TestPageForElementActionDecorator'

        class TestPage(Page):

            page_name = test_page_name

            def get_url(self):
                return '/'

            @property
            def elements_selectors(self):
                return ((alias, selector),)

        driver = self._get_driver(mocked_browser)
        driver.open_page(test_page_name)
        driver._browser.find_by_xpath.return_value = element_mock = Mock()

        driver.click(alias)
        driver._browser.find_by_xpath.assert_called_once_with(selector)
        element_mock.click.assert_called_once_with()
