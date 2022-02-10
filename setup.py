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
        'bs4', 
        'requests',
        ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)