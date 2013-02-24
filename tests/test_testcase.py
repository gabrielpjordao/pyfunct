import unittest

from pyfunct import FunctTestCase, BaseConfig, action
from pyfunct.browsers import BaseBrowserDriver

class TestBrowserDriver(BaseBrowserDriver):
    """
        Browser Driver used for testing purposes.
    """

    driver_name = 'testing_browser'

    quit_call_count = 0

    def quit(self):
        self.quit_call_count += 1

class TestConfig(BaseConfig):
    """
        Overrides default browser in order to test the testcase and prevent opening
        browsers.
    """

    default_driver_name = 'testing_browser'

class TestCaseTester(FunctTestCase):

    def runTest(self):
        """
            Overrides it to prevent running tests from the testcase, as it's being
            tested.
        """
        pass

class FunctTestCaseTestCase(unittest.TestCase):

    def test_create_browser_with_default_config(self):
        testcase = TestCaseTester()
        driver = testcase.create_browser()

        self.assertIsInstance(driver, TestBrowserDriver)

        self.assertIn(driver, testcase.browsers)

    def test_create_browser_choosing_the_driver(self):

        class CustomDriver(BaseBrowserDriver):
            driver_name = 'custom_browser'

        testcase = TestCaseTester()

        driver = testcase.create_browser('custom_browser')

        self.assertIsInstance(driver, CustomDriver)

        self.assertIn(driver, testcase.browsers)

    def test_actions_are_added_to_testcase(self):
        @action
        def some_action():
            return 'called'

        testcase = TestCaseTester()

        self.assertEqual(testcase.actions.some_action(), 'called')

    def test_setUp(self):

        testcase = TestCaseTester()

        # No browsers were added yet
        self.assertEqual(len(testcase.browsers), 0)

        testcase.setUp()

        # After setup, one browser was created
        self.assertEqual(len(testcase.browsers), 1)

    def test_tearDown(self):
        """
            Checks if the browsers were quitted after tearDown
        """

        testcase = TestCaseTester()

        driver = testcase.create_browser()

        # assert that no quit calls were made before teardown
        self.assertEqual(driver.quit_call_count, 0)

        testcase.tearDown()

        # assert that, after teardown, the browser was quitted
        self.assertEqual(driver.quit_call_count, 1)
