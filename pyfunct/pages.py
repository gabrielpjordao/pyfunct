# -*- coding: utf-8 -*-

from pyfunct.exceptions import SelectorTypeNotSupportedException

REGISTERED_PAGES = {}


class PageMetaclass(type):
    """
      Metaclass for `Page`.
    """

    def __init__(cls, name, bases, attributes):
        """
            This registers the page elements defined in `elements_selectors`
            property and adds the page to the `REGISTERED_PAGES`.
        """
        try:
            page_name = attributes['page_name']
        except KeyError:
            raise NotImplementedError(
                "You must specify a page name for %s." % cls.__name__)

        if not hasattr(cls, 'elements'):
            cls.elements = {}

        page = cls()
        for element in page.elements_selectors:
            page.register_element(*element)

        if page_name is not None:
            REGISTERED_PAGES[page_name] = page

        return super(PageMetaclass, cls).__init__(name, bases, attributes)


class Page(object):
    """
        This class defines the Page model, which has two responsibilities:
        registering elements selectors and setting the url for the page.
    """

    __metaclass__ = PageMetaclass

    #: Should be set to a string and it's the alias used to identify the page
    page_name = None
    provides_full_url = False

    def get_url(self, *args, **kwargs):
        """
            It's the page URL. It's a function because some pages requires
            special behavior to build their urls, so it accepts arguments.

            The returned value must start with a slash.
        """
        raise NotImplementedError(
            "The page must implement the get_url method.")

    @classmethod
    def register_element(cls, alias, selector, selection_type='xpath'):
        """
            Register elements to the current page, using the elements list.
            Elements will be dicts with the following keys:
                `selection_type`: Stores the selector kind (css|xpath|id|tag)
                `elector`: Stores the actual selector
        """

        if selection_type not in ('xpath', 'id', 'css', 'name'):
            raise SelectorTypeNotSupportedException

        cls.elements[alias] = {
            'selector': selector,
            'selection_type': selection_type
        }

    @property
    def elements_selectors(self):
        """
            This property should return an iterable (a list, for instance)
            with tuples of length 3, with the element alias, selector and
            selection type, respectively. For example::

                @property
                def elements_selectors(self):
                    return [
                        ('login box', 'input#login-input', 'css'),
                        ('password box', 'input#password-input', 'css'),
                    ]
        """
        return []
