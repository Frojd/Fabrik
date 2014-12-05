# -*- coding: utf-8 -*-

"""
frojd_fabric.ext.npm
-------------------------
"""

from fabric.decorators import task
from fabric.state import env


def install():
    env.run("npm install")

