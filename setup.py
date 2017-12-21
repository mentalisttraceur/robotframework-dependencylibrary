#!/usr/bin/env python

from os import path

from setuptools import setup

project_directory = path.abspath(path.dirname(__file__))
readme_path = path.join(project_directory, 'README.rst')
library_path = path.join(project_directory, 'DependencyLibrary.py')

with open(readme_path, encoding='utf-8') as readme_file:
    long_description = readme_file.read()

with open(library_path, encoding='utf-8') as library_file:
    for line in library_file:
        # This is of course extremely fragile, but XP/YAGNI-ing it:
        if line.startswith('__version__'):
            exec(line)
            break

setup(
    name='robotframework-dependencylibrary',
    version=__version__,
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
        'Programming Language :: Pythong :: 3',
        'Programming Language :: Pythong :: 2',
        'Operating System :: OS Independent',
    ],
    py_modules=['DependencyLibrary'],
    install_requires=['robotframework'],
)
