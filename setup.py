# !/usr/bin/env python
from setuptools import setup
from setuptools import Command
from setuptools.command.test import test as TestCommand
from tempfile import NamedTemporaryFile
import io
import os
import re
import subprocess
import shutil
import sys
import urllib.request

here = os.path.abspath(os.path.dirname(__file__))


def read(*file_names, **kwargs):
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in file_names:
        with io.open(filename, encoding="utf-8") as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.rst', 'CHANGES.rst')

setup(
    name='genial',
    packages=['genial'],
    version='0.1.0',
    description='A "Génies en herbe" questions manager.',
    author='Adam Scott',
    license='GPLv3',
    author_email='ascott.ca@gmail.com',
    url='https://github.com/adamscott/genial',
    keywords=['quiz', 'manager', ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: MacOS X :: Aqua',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Natural Language :: French',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Education',
        'Topic :: Database'
    ],
    tests_require=['tox'],
    install_requires=['PyQt5', 'yapsy', 'appdirs'],
    include_package_data=True,
    extras_require={
        'testing': ['tox'],
    }
)
