#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pip
from setuptools import setup, find_packages

import fabrik


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

package_exclude = ("tests*", "examples*")
packages = find_packages(exclude=package_exclude)


# Convert markdown to rst
try:
    from pypandoc import convert
    long_description = convert("README.md", "rst")
except:
    long_description = ""


setup(
    name="fabrik",
    version=fabrik.__version__,
    description="A simple to use deployment toolkit built on top of Fabric",
    long_description=long_description,
    author="Fröjd",
    author_email="martin.sandstrom@frojd.se",
    url="https://github.com/frojd/fabrik",
    packages=packages,
    include_package_data=True,
    install_requires=[
        'Fabric==1.12.0',
        'Unipath==1.1',
        'PyCrypto==2.6.1',
        'jinja2==2.8',
        'click>=5.0',
        'GitPython==1.0.1',
    ],
    tests_require=[
        'Fabric==1.12.0',
        'Unipath==1.1',
        'PyCrypto==2.6.1',
        'jinja2==2.8',
        'click>=5.0',
        'GitPython==1.0.1',
    ],
    entry_points={
        "console_scripts": [
            "fabrik = fabrik.scripts.fabrik:main",
            "fabrik_start = fabrik.cli.scripts.init:main",
            "fabrik_cleanup = fabrik.cli.scripts.cleanup:main",
        ]
    },
    license="MIT",
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Software Distribution",
        "Topic :: System :: Systems Administration",
    ],
)
