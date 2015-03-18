#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from setuptools import setup, find_packages
from pip.req import parse_requirements
import frojd_fabric


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

package_exclude = ("tests*", "examples*")
packages = find_packages(exclude=package_exclude)

with open("README.md") as f:
    readme = f.read()

requires = parse_requirements("requirements/install.txt")
install_requires = [str(ir.req) for ir in requires]

requires = parse_requirements("requirements/tests.txt")
tests_require = [str(ir.req) for ir in requires]

long_description = """

---

%s

""" % readme


setup(
    name="frojd-fabric",
    version=frojd_fabric.__version__,
    description=("A simple to use deployment toolkit built on top of Fabric"),
    long_description=long_description,
    author="Fröjd",
    author_email="martin.sandstrom@frojd.se",
    url="https://github.com/frojd/frojd-fabric",
    packages=packages,
    include_package_data=True,
    install_requires=install_requires,
    tests_require=tests_require,
    license="MIT",
    zip_safe=False,
    classifiers=(
        "Development Status :: 4 - Beta",
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
    ),
)
