# !/usr/bin/env python
from setuptools import setup
from setuptools.command.test import test as TestCommand
import io
import os


here = os.path.abspath(os.path.dirname(__file__))


def read(*file_names, **kwargs):
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in file_names:
        with io.open(filename) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.rst', 'CHANGES.rst')


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        import sys
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)


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
    install_requires=[],
    cmdclass={'test': Tox},
    include_package_data=True,
    extras_require={
        'testing': ['tox'],
    }
)
