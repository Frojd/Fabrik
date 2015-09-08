# -*- coding: utf-8 -*-

"""
fabrik.ext.npm
-------------------------
"""

from fabric.decorators import task
from fabric.state import env


def install():
    env.run("npm install")
