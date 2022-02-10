from setuptools import setup

setup(
    name = 'neospy',
    version = '0.0.1',    
    description = 'A python module to make calls to the NEOS server.',
    url = 'https://github.com/scythetrigger/neospy',
    author = 'Nicholas Parham',
    author_email = 'nick-99@att.net',
    license = 'Apache Software License',
    packages = ['neospy'],
    install_requires = [
        'bs4', 
        'requests',
        'amplParser'
        ],

    classifiers = [],
)