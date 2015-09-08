# -*- coding: utf-8 -*-

"""
fabrik.ext.forever
-------------------------
Contains methods for dealing with nodejs forever

Api doc: https://github.com/nodejitsu/forever
"""

from fabric.decorators import task
from fabric.state import env
from fabrik import paths


@task
def restart():
    if "forever_app" not in env:
        raise Exception("Could not find app to run"
                "env.forever_app must be set")

    env.run("forever start %s" % env.forever_app)


def restart_service():
    env.run("service forever restart")
