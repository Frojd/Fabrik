# -*- coding: utf-8 -*-

"""
frojd_fabric.recipes.wordpress
-----------------------------
Standard recipe to handle wordpress installs.
"""

from fabric.state import env
from frojd_fabric import paths
from frojd_fabric.hooks import hook
from frojd_fabric.ext import composer


@hook("setup")
def setup():
    env.run("touch %s" % paths.get_shared_path("wp-config.php"))
    env.run("touch %s" % paths.get_shared_path(".htaccess"))


@hook("deploy")
def after_deploy():
    paths.symlink(
        paths.get_shared_path(".htaccess"),
        paths.get_current_path(".htaccess")
    )

    paths.symlink(
        paths.get_shared_path("wp-config.php"),
        paths.get_current_path("wp-config.php")
    )

    paths.symlink(
        paths.get_upload_path(),
        paths.get_current_path("wp-content/uploads")
    )

