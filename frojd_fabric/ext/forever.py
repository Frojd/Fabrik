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


@task
def restart_forever():
    env.run("forever restart %s" % app)

