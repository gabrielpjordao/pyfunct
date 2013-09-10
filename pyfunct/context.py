# -*- coding: utf-8 -*-

from pyfunct.exceptions import InvalidConfigurationException


class DefaultConfig(object):
    """
        Holds the default test configuration. Attributes from it are overriden
        and added by classes that extend `BaseConfig`
    """

    base_url = 'http://localhost'
    default_driver_name = 'splinter'
    default_browser = 'firefox'


class ConfigMetaclass(type):
    """
        This Metaclass is responsible for making any class that extends
        from BaseConfig to have the attributes added/overrided to the global
        config, which can be accessed by `pyfunct.config`.
    """

    def __init__(cls, name, bases, attributes):
        """
            This is a Config Factory. It treats `base_url` configuration
            and sets the attributes of any class that inherits from
            `BaseConfig` to `DefaultConfig`, making the configuration global.
        """
        base_url = attributes.get('base_url')
        if base_url is not None and base_url.endswith('/'):
            raise InvalidConfigurationException(
                "Please provide a valid base_url, without a slash ending.")

        for attr_name, attr_value in attributes.items():
            if not attr_name.startswith('__'):
                setattr(DefaultConfig, attr_name, attr_value)

        return super(ConfigMetaclass, cls).__init__(name, bases, attributes)


class BaseConfig(object):
    """
        To add configuration, you should override this class and set the
        attributes that you want to override as class attributes.

        For example::
            from pyfunct import BaseConfig
            class MyCustomConfig(BaseConfig):
                base_url = 'http://www.mycoolsite.com/'

                test_username = 'testuser'
                test_password = 'S3crEtPa55w0rD'
    """

    __metaclass__ = ConfigMetaclass

config = DefaultConfig
