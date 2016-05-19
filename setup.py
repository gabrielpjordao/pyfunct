# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

__version__ = '0.1.3'

setup(
    name='pyfunct',
    version=__version__,
    url='https://github.com/gabrielpjordao/pyfunct',
    author=u'Gabriel Jordão',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['splinter==0.6.0'],
    tests_require=['mock'],
    test_suite="tests"
)
