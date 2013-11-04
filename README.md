# PyFunct
[![Build Status](https://travis-ci.org/gabrielpjordao/pyfunct.png)](https://travis-ci.org/gabrielpjordao/pyfunct)

PyFuncT stands for Python Functional Testing and it is a small framework that aims to help writing functional automated tests with python, to test web applications.

Principles:
* <b>Organization</b>: Provides a clean workflow to store elements selectors, pages and config, helping you to keep your tests organized and reusable.

* <b>Flexibility</b>: PyFunct tests are fully built with python, giving you total flexibility. With frameworks that provide natural-language like programming, sometimes it can get really tricky to perform simple actions (like opening two browsers in the same test if you need to test live updates, for instance)

* <b>Freedom</b>:  Most of the framework is customizable and optional, it means you can choose not to use some part of it or make a few tweaks, if necessary.

PyFunct includes:
* Pages (which holds elements selectors and URLS)
* Actions
* Config (global configuration easily manageable)
* [Splinter](http://splinter.cobrateam.info/) driver compatibility, which includes selenium, phantomJS, zopetest and more

## Getting started

This should get you started with the basic functionality. You can look for more examples
on `examples` folder.

## Installing
To install pyfunct, all you should do is:
`pip install pyfunct`

Or

`easy_install pyfunct`, if you must.


### Step 1 - The test case
Here is a code snippet with two basic tests that do the same thing: A wikipedia search. The first uses pages and the second uses pages and actions. Both concepts will be explained ahead.

```python
from pyfunct import FunctTestCase

class MyTestCase(FunctTestCase):

    def test_searching_a_wiki(self):
        # This goes to the page and loads it's elements selectors.
        self.browser.open_page('wikipedia index')

        # Fill the search input with "Functional testing"
        self.browser.type('search input', 'Functional testing')

        # Submit the search by clicking the button
        self.browser.click_and_wait('search button')

        page_title = self.browser.page_title
        expected_title = 'Functional testing - Wikipedia, the free encyclopedia'
        self.assertIn(expected_title, page_title)

    def test_searching_a_wiki_using_actions(self):
        self.actions.perform_search(self.browser, 'Functional testing')

        expected_title = 'Functional testing - Wikipedia, the free encyclopedia'

        self.actions.assert_title_contains(self.browser, expected_title)

```
In the above code, we wrote a testcase that inherits from `FunctTestCase`. All PyFunct tests should inherit from it.
`FunctTestCase` is just a testcase that inherits from `unittest.TestCase` (python's native unittest testcase) with some shortcuts. It means you can use it's methods (such as `assertIn`).

Before each test execution, a browser instance is initialized. When the test is finished. it's automatically exited.
If you want to create multiple browsers, all you need to do is call `self.create_browser()`.

### Step 2 - Creating pages
In Step 1 we've made references to `wikipedia index`, `search input` and `search button`. These are aliases that were defined in a Page class. To create it, you can do the following:
```python
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

```
All classes that inherits from Page and provides a `page_name` will be accessible by the browser.

### Step 3 - Creating Actions
In the second test (`test_searching_a_wiki_using_actions`), we've used two actions: `perform_search` and `assert_title_contains`. And with that, we've made the same thing as the first test, but in a simpler and reusable way. To write these actions and have them accessible by `actions`, from a `FunctTestCase`, you need to use the `@action` decorator, as follow:

```python

from pyfunct import action

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
    assert expected_title in page_title, "The expected title was not found in the page title"
```

### Step 4 - Manage your config
Until now, we did not define nor the browser driver or the base url we should use. Pyfunct comes with a simple class-based configuration, which sets the global configuration attributes of your choice. Check it:
```python
from pyfunct import BaseConfig

class WikipediaConfig(BaseConfig):
    base_url = 'http://en.wikipedia.org'
```

That's it, we've just set the global config to have the `base_url` as wikipedia, since we are testing the wikipedia page.
There's no need to change the `default_driver_name`, cause it's using splinter by default. Only if you want to use another browser. For that, you can check the documentation.

### Step 5 - Run your tests
Currently, PyFunct does not provide a test runner and you can run it as you wish. A good choice for it is [nose](https://github.com/nose-devs/nose).
