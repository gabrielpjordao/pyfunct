# -*- coding: utf-8 -*-
from pyfunct import BaseConfig
from pyfunct import Page
from pyfunct import FunctTestCase
from pyfunct import action


class WikipediaConfig(BaseConfig):
    base_url = 'http://en.wikipedia.org'
    default_browser = 'phantomjs'


class IndexPage(Page):

    page_name = 'wikipedia index'

    def get_url(self):
        return '/'

    @property
    def elements_selectors(self):
        return (
            ('search input', "//input[@name='search']", 'xpath'),
            ('search button', "#searchButton", 'css')
        )


class MyTestCase(FunctTestCase):

    def test_searching_a_wiki(self):
        # This goes to the page and loads it's elements selectors.
        self.browser.open_page('wikipedia index')

        # Fill the search input with "Functional testing"
        self.browser.type('search input', 'Functional testing')

        # Submit the search by clicking the button
        self.browser.click_and_wait('search button')

        page_title = self.browser.page_title
        expected_title = 'Functional testing - Wikipedia'
        self.assertIn(expected_title, page_title)

    def test_searching_a_wiki_using_actions(self):
        self.actions.perform_search(self.browser, 'Functional testing')

        expected_title = 'Functional testing - Wikipedia'

        self.actions.assert_title_contains(self.browser, expected_title)


@action
def perform_search(browser, query):
    # This goes to the page and loads it's elements selectors.
    browser.open_page('wikipedia index')

    # Fill the search input with "Functional testing"
    browser.type('search input', 'Functional testing')

    # Submit the search by clicking the button
    browser.click_and_wait('search button')


@action
def assert_title_contains(browser, expected_title):
    page_title = browser.page_title
    assert expected_title in page_title, "The expected title was not found in"\
        "the page title"
