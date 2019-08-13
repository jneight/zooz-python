# coding=utf-8


from setuptools import setup, find_packages

import zooz

setup(
    name='zooz-python',
    version=zooz.__version__,
    url='https://github.com/jneight/zooz-python',
    install_requires=['requests==2.20.0'],
    description="Python client for ZooZ payments API",
    author=zooz.__author__,
    author_email=zooz.__email__,
    include_package_data=True,
    packages=find_packages(),
    license=zooz.__license__,
    test_suite="tests",
)
