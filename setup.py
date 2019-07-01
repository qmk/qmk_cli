#!/usr/bin/env python
# Special thanks to Hynek Schlawack for providing excellent documentation:
#
# https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
import os
from setuptools import setup, find_packages, Command


def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()


setup(
    name='qmk',
    version='0.0.1',
    description='Program to help you work with qmk_firmware.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/qmk/qmk_cli',
    license='MIT License',
    author='skullydazed',
    author_email='skullydazed@gmail.com',
    install_requires=['argcomplete', 'colorama'],
    packages=find_packages(),
    py_modules=['milc'],
    scripts=['qmk'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
)
