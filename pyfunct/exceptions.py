# -*- coding: utf-8 -*-


class UnregisteredElementException(Exception):
    """
    Exception raised by trying to access an element that is not registered.
    to the current page.
    """


class SelectorTypeNotSupportedException(Exception):
    """
    Exception raised when trying to access an element by an unknown
    selector type.
    """


class InvalidUrlException(Exception):
    """
    Exception raised when the url doesn't follow the expected pattern.
    """


class InvalidConfigurationException(Exception):
    """
    Exception Raised when some config attribute is being used incorrectly.
    """


class PageNotLoadedException(Exception):
    """
    Exception raised when the page is not loaded properly
    """


class ActionNotPerformableException(Exception):
    """
        Raised whenever an action cannot be performed;
    """


class ExistentElementException(Exception):
    """
    Exception raised when trying to register duplicated elements in the
    same page.
    """
