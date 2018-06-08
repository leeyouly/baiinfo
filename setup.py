
from setuptools import setup, find_packages
import os

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
setup(
    name = 'baiinfo',
    version = '0.1.6',
    packages = find_packages(exclude=('tests',)),
    entry_points = {'scrapy': ['settings = baiinfo.settings']},
)