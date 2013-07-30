# coding=utf-8

__title__ = 'zooz-python'
__version__ = '0.2'
__license__ = 'Apache 2.0'
__author__ = 'Javier Cordero Martinez'
__email__ = 'jcorderomartinez@gmail.com'


from setuptools import setup, find_packages

setup(
    name='zooz-python',
    version=__version__,
    url='https://github.com/jneight/zooz-python',
    install_requires=['requests==1.2.3'],
    author=__author__,
    author_email=__email__,
    include_package_data=True,
    packages=find_packages(),
    license=__license__,
)
