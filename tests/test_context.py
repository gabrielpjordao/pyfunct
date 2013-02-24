import unittest

from pyfunct.context import BaseConfig, config
from pyfunct.exceptions import InvalidConfigurationException

class ConfigTestCase(unittest.TestCase):

    def test_override_config(self):

        overriden_url = 'http://some_url'

        class MyConf(BaseConfig):
            base_url = overriden_url

        # The global config got the new value
        self.assertEqual(config.base_url, overriden_url)

    def test_invalid_base_url(self):

        with self.assertRaises(InvalidConfigurationException):
            class MyConf(BaseConfig):
                base_url = 'url_ending_with_slash.com/'
