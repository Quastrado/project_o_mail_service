from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name = 'owl_mail',
    version = '1.0',
    package = find_packages,
    long_description = open(jpin(dirname(__file__), 'README.txt')).read(),
)