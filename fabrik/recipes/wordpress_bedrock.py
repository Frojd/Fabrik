"""
recipes.wordpress_bedrock
--------------------------
Recipe for dealing with bedrock based wordpress installations
"""

import os.path

from fabrik import paths, hooks
from fabric.state import env
from fabrik.ext import composer, envfile


def setup():
    env.run("touch %s" % paths.get_shared_path(".htaccess"))
    env.run("touch %s" % paths.get_shared_path(".env"))


def deploy():
    composer.install()
    composer.update()

    envfile.symlink_env()


def after_deploy():
    paths.symlink(
        paths.get_shared_path(".htaccess"),
        paths.get_current_path(".htaccess")
    )

    paths.symlink(
        paths.get_upload_path(),
        paths.get_current_path("app/uploads")
    )


def register():
    hooks.register_hook("setup", setup)
    hooks.register_hook("deploy", deploy)
    hooks.register_hook("after_deploy", after_deploy)


def unregister():
    hooks.unregister_hook("setup", setup)
    hooks.unregister_hook("deploy", after_deploy)
    hooks.unregister_hook("after_deploy", after_deploy)
