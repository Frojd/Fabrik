# -*- coding: utf-8 -*-

"""
fabrik.recipes.wordpress
--------------------------
This is a basic wordpress recipe that handles shared htaccess, config and files
"""

import os.path

from fabric.state import env

from fabrik import paths, hooks
from fabrik.ext import composer


def setup():
    env.run("touch %s" % paths.get_shared_path("wp-config.php"))
    env.run("chmod 400 %s" % paths.get_shared_path("wp-config.php"))

    env.run("touch %s" % paths.get_shared_path(".htaccess"))
    env.run("chmod 644 %s" % paths.get_shared_path(".htaccess"))


def deploy():
    paths.symlink(
        paths.get_shared_path("wp-config.php"),
        os.path.join(paths.get_source_path(env.current_release),
                     "wp-config.php")
    )


def after_deploy():
    paths.symlink(
        paths.get_shared_path(".htaccess"),
        paths.get_current_path(".htaccess")
    )

    paths.symlink(
        paths.get_upload_path(),
        paths.get_current_path("wp-content/uploads")
    )


def register():
    hooks.register_hook("setup", setup)
    hooks.register_hook("deploy", deploy)
    hooks.register_hook("after_deploy", after_deploy)


def unregister():
    hooks.unregister_hook("setup", setup)
    hooks.unregister_hook("deploy", deploy)
    hooks.unregister_hook("after_deploy", after_deploy)
