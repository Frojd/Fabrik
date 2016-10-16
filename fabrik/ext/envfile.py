# -*- coding: utf-8 -*-

"""
fabrik.ext.envfile
------------------
Contains .env-file helpers
"""

import os.path

from fabric.state import env
from fabric.decorators import task
from fabrik import paths


@task
def create_env():
    env.run("touch %s" % paths.get_shared_path(".env"))
    env.run("chmod 400 %s" % paths.get_shared_path(".env"))


@task
def symlink_env():
    paths.symlink(
        paths.get_shared_path(".env"),
        os.path.join(paths.get_source_path(env.current_release), ".env")
    )
