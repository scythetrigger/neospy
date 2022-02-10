from setuptools import setup

setup(
    name = 'neos',
    version = '0.0.0',    
    description = 'A python module to make calls to the NEOS server.',
    #url='https://github.com/shuds13/pyexample',
    author = 'Nicholas Parham',
    author_email = 'nick-99@att.net',
    license = 'Apache Software License',
    packages = ['neos'],
    install_requires = [
        'base64',
        'bs4', 
        'requests',
        'amplParser'
        ],

    classifiers = [],
)