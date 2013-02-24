import unittest

from pyfunct.pages import Page, REGISTERED_PAGES

from pyfunct.exceptions import SelectorTypeNotSupportedException

class PagesTestCase(unittest.TestCase):

    def test_page_registering(self):

        elements_selectors = (
            ('elxpath', '//el', 'xpath'),
            ('elcss', '#my-id', 'css'),
            ('elname', 'somename', 'name'),
            ('elid',  'someid', 'id'),
        )
        class TestPage(Page):

            page_name = 'test_1'

            @property
            def elements_selectors(self):
                return elements_selectors


        page = REGISTERED_PAGES['test_1']
        self.assertIsInstance(page, Page)

        # Checks for elements registration
        for alias, selector, selection_type in elements_selectors:
            registered_element = page.elements[alias]
            self.assertEqual(registered_element['selector'], selector)
            self.assertEqual(registered_element['selection_type'], selection_type)

    def test_page_without_name(self):
        with self.assertRaises(NotImplementedError):
            class PageWithoutName(Page):
                pass

    def test_NotImplementedError_if_page_doesnt_override_page_url(self):
        with self.assertRaises(NotImplementedError):
            class PageWithoutURL(Page):
                page_name = 'page_without_get_url'

            page = PageWithoutURL()
            page.get_url()

    def test_page_with_invalid_element_type(self):
        with self.assertRaises(SelectorTypeNotSupportedException):
            class PageWithInvalidElementSelector(Page):

                page_name = 'page_with_invalid_element_selection_type'
                @property
                def elements_selectors(self):
                    return [('alias', 'selector', 'invalid-selector')]

            page = PageWithInvalidElementSelector()
