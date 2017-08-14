from setuptools import setup, find_packages

import sys

from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        import shlex
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)

with open('requirements.txt') as fd:
    requirements = [line.rstrip() for line in fd]

setup(
    name='interative_map_based_visiualization_tool',
    version="0.1",
    packages=find_packages(),

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = requirements,
    # metadata for upload to PyPI
    author = "deathcoder007",
    author_email = "chinmay.rakshit@gmail.com",
    description = "Creating an interactive map based visualization tool for data that is spread out across time and space.",
    license = "MIT",
    keywords = ['data visualization', 'mapbox'],
    url = "https://interative-map-based-visiualiz.herokuapp.com/",   # project home page, if any
    zip_safe = True,
    tests_require = ['pytest'],
    cmdclass = {'test': PyTest},
    # could also include long_description, download_url, classifiers, etc.
)