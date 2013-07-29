# coding=utf-8

import zooz

from setuptools import setup, find_packages


setup(
    name='zooz-python',
    version=zooz.__version__,
    install_requires=['requests==1.2.3'],
    include_package_data=True,
    packages=find_packages(),
    license=zooz.__license__,
)
