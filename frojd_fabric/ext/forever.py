# -*- coding: utf-8 -*-

"""
frojd_fabric.ext.forever
-------------------------
Contains methods for dealing with nodejs forever
"""

from fabric.decorators import task
from fabric.state import env


@task
def restart_forever():
    env.run("service forever restart")

