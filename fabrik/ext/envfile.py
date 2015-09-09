# -*- coding: utf-8 -*-

"""
fabrik.ext.envfile
------------------
Contains .env-file helpers
"""

from fabric.decorators import task
from fabric.state import env
from fabrik import paths


@task
def create_env():
    env.run("touch %s" % paths.get_shared_path(".env"))
    env.run("chmod 400 %s" % paths.get_shared_path(".env"))


@task
def symlink_env():
    paths.symlink(
        paths.get_shared_path(".env"),
        paths.get_current_path(".env")
    )
