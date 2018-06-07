#!/usr/bin/env python

from os import path

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from DependencyLibrary import __version__

project_directory = path.abspath(path.dirname(__file__))
readme_path = path.join(project_directory, 'README.rst')

with open(readme_path) as readme_file:
    long_description = readme_file.read()

setup(
    name='robotframework-dependencylibrary',
    version=__version__ + '.post1',
    description='Declare dependencies between Robot Framework tests',
    long_description=long_description,
    license='0BSD (BSD Zero Clause License)',
    url='https://github.com/mentalisttraceur/robotframework-dependencylibrary',
    author='Alexander Kozhevnikov',
    author_email='mentalisttraceur@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Robot Framework :: Library',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'Operating System :: OS Independent',
    ],
    py_modules=['DependencyLibrary'],
    install_requires=['robotframework'],
)
