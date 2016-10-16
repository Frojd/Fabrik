"""
recipes.wordpress_composer
--------------------------
Recipe for dealing with composer bases wordpress installations
"""

from fabric.state import env

from fabrik import paths, hooks
from fabrik.ext import composer


def setup():
    env.run("touch %s" % paths.get_shared_path("wp-config.php"))
    env.run("touch %s" % paths.get_shared_path(".htaccess"))


def deploy():
    composer.install()
    composer.update()

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


def register():
    hooks.register_hook("setup", setup)
    hooks.register_hook("deploy", deploy)


def unregister():
    hooks.unregister_hook("setup", setup)
    hooks.unregister_hook("deploy", deploy)
