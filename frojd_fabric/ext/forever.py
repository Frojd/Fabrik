# -*- coding: utf-8 -*-

"""
frojd_fabric.ext.forever
-------------------------
Contains methods for dealing with nodejs forever

https://github.com/nodejitsu/forever

forever start app.js
forever stop app.js
forever restart app.js

"""

from fabric.decorators import task
from fabric.state import env
from frojd_fabric import paths


@task
def restart():
    if "forever_app" not in env:
        raise Exception("Could not find app to run"
                "env.forever_app must be set")

    env.run("forever start %s" % env.forever_app)

