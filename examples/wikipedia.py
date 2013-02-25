# -*- coding: utf-8 -*-

from pyfunct import BaseConfig

class WikipediaConfig(BaseConfig):
    base_url = 'http://en.wikipedia.org'

from pyfunct import Page

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


from pyfunct import action
@action
def perform_search(browser, query):
    # This goes to the page and loads it's elements selectors.
    browser.open_page('wikipedia index')

    # Fill the search input with "Functional testing"
    search_input = browser.get_page_element('search input')
    browser.type(search_input, 'Functional testing')

    # Submit the search by clicking the button
    search_button = browser.get_page_element('search button')
    browser.click_and_wait(search_button)

@action
def assert_title_contains(browser, expected_title):
    page_title = browser.page_title
    assert expected_title in page_title, "The expected title was not found in the page title"

from pyfunct import FunctTestCase
class MyTestCase(FunctTestCase):

    def test_searching_a_wiki(self):
        # This goes to the page and loads it's elements selectors.
        self.browser.open_page('wikipedia index')

        # Fill the search input with "Functional testing"
        search_input = self.browser.get_page_element('search input')
        self.browser.type(search_input, 'Functional testing')

        # Submit the search by clicking the button
        search_button = self.browser.get_page_element('search button')
        self.browser.click_and_wait(search_button)

        page_title = self.browser.page_title
        expected_title = 'Functional testing - Wikipedia, the free encyclopedia'
        self.assertIn(expected_title, page_title)

    def test_searching_a_wiki_using_actions(self):
        self.actions.perform_search(self.browser, 'Functional testing')

        expected_title = 'Functional testing - Wikipedia, the free encyclopedia'

        self.actions.assert_title_contains(self.browser, expected_title)
