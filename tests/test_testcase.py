import unittest

from pyfunct import FunctTestCase, BaseConfig, action
from pyfunct.browsers import BaseBrowserDriver


class TestBrowserDriver(BaseBrowserDriver):
    """
        Browser Driver used for testing purposes.
    """

    driver_name = 'testing_browser'

    quit_call_count = 0
    clear_session_call_count = 0
    close_call_count = 0

    def quit(self):
        self.quit_call_count += 1

    def close(self):
        self.close_call_count += 1

    def clear_session(self):
        self.clear_session_call_count += 1


class TestConfig(BaseConfig):
    """
        Overrides default browser in order to test the testcase and prevent opening
        browsers.
    """

    default_driver_name = 'testing_browser'


class TestCaseTester(FunctTestCase):

    reuse_browser = True

    def runTest(self):
        """
            Overrides it to prevent running tests from the testcase, as it's being
            tested.
        """
        pass


class NonReuseTestCaseTester(FunctTestCase):

    reuse_browser = False

    def runTest(self):
        """
            Overrides it to prevent running tests from the testcase, as it's being
            tested.
        """
        pass


class FunctTestCaseTestCase(unittest.TestCase):

    def tearDown(self):
        TestCaseTester.tearDownClass()

    def test_create_browser_with_default_config(self):
        testcase = TestCaseTester()
        driver = testcase.create_browser()

        self.assertIsInstance(driver, TestBrowserDriver)

        self.assertIn(driver, testcase.browsers)

    def test_create_browser_choosing_the_driver(self):

        class CustomDriver(BaseBrowserDriver):
            driver_name = 'custom_browser'

            def quit(self):
                pass

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

    def test_disabling_reuse_browser(self):

        testcase = NonReuseTestCaseTester()

        # No browsers were added yet
        self.assertEqual(len(testcase.browsers), 0)

        testcase.setUp()

        # After setup, no browser was created
        self.assertEqual(len(testcase.browsers), 0)

    def test_tearDown(self):
        """
            Checks if the browsers weren't quitted after tearDown
        """

        testcase = TestCaseTester()
        testcase.setUp()

        driver = testcase.create_browser()

        # assert that no close/quit calls were made before teardown
        self.assertEqual(driver.quit_call_count, 0)
        self.assertEqual(driver.close_call_count, 0)
        self.assertEqual(driver.clear_session_call_count, 0)

        self.assertEqual([testcase.browser, driver], testcase.browsers)

        testcase.tearDown()

        # assert that, after teardown, the browser was closed
        self.assertEqual(driver.quit_call_count, 0)
        self.assertEqual(driver.close_call_count, 1)
        self.assertEqual(driver.clear_session_call_count, 0)

        # assert that default browser was only cleared
        self.assertEqual(testcase.browser.quit_call_count, 0)
        self.assertEqual(testcase.browser.close_call_count, 0)
        self.assertEqual(testcase.browser.clear_session_call_count, 1)

        # assert that testcase keeps only the default browser
        self.assertEqual([testcase.browser], testcase.browsers)

    def test_tearDown_without_reuse_browser(self):
        testcase = TestCaseTester()
        testcase.reuse_browser = False

        testcase.setUp()

        driver = testcase.create_browser()

        # assert that no quit/close calls were made before teardown
        self.assertEqual(driver.quit_call_count, 0)
        self.assertEqual(driver.close_call_count, 0)
        self.assertEqual(driver.clear_session_call_count, 0)

        self.assertEqual([driver], testcase.browsers)

        testcase.tearDown()

        # assert that, after teardown, the browser was closed
        self.assertEqual(driver.quit_call_count, 0)
        self.assertEqual(driver.close_call_count, 1)
        self.assertEqual(driver.clear_session_call_count, 0)

        # assert that testcase keeps no browser
        self.assertEqual([], testcase.browsers)

    def test_tearDownClass(self):

        testcase = TestCaseTester()

        driver = testcase.create_browser()

        # assert that no quit calls were made before teardown
        self.assertEqual(driver.quit_call_count, 0)

        testcase.tearDownClass()

        # assert that, after teardown, the browser was quitted
        self.assertEqual(driver.quit_call_count, 1)

        # assert that testcase keeps no browser
        self.assertEqual([], testcase.browsers)
