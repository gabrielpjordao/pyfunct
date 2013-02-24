# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

__version__ = '0.1.0'

setup(
    name='pyfunct',
    version=__version__,
    url='https://github.com/gabrielpjordao/pyfunct',
    author=u'Gabriel Jordão',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['splinter'],
    tests_require=['mock'],
)