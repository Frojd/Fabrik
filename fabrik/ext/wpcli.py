# -*- coding: utf-8 -*-

"""
fabrik.ext.wpcli
------------------
A collection of celeryd helpers.
"""

from fabric.decorators import task
from fabric.state import env
from fabrik.utils.elocal import elocal


@task
def remote_to_local_db():
    name = "latest_land"

    env.run("wp db export /tmp/%s.sql" % name)
    elocal("scp land.se:/tmp/%s.sql ./" % name)
    elocal("wp db import %s.sql" % name)

    elocal("rm /tmp/%s.sql" % name)
