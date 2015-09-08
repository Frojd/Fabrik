# -*- coding: utf-8 -*-

"""
fabrik.ext.celeryd
------------------
A collection of celeryd helpers.
"""

from fabric.decorators import task
from fabric.state import env


@task
def restart_celery():
    env.run("service celeryd restart")
