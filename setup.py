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


packages = find_packages()

with open('README.md') as f:
    readme = f.read()

requires = parse_requirements("requirements.txt")
install_requires = [str(ir.req) for ir in requires]


long_description = """

---

%s

""" % readme


setup(
    name="frojd_fabric",
    version=frojd_fabric.__version__,
    description=(""),
    long_description=long_description,
    author="Fröjd",
    author_email="martin.sandstrom@frojd.se",
    url="https://github.com/frojd/frojd-fabric",
    packages=packages,
    include_package_data=True,
    install_requires=install_requires,
    license="MIT",
    zip_safe=False,
    classifiers=(
        "Development Status :: 4 - Beta",
        'Environment :: Web Environment',
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2',
        "Programming Language :: Python :: 2.7"
    ),
)
