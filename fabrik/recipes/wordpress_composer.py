"""
recipes.wordpress_composer
--------------------------
Recipe for dealing with composer bases wordpress installations
"""

from fabric.state import env
from fabrik import paths
from fabrik.hooks import hook
from fabrik.ext import composer


@hook("init_tasks")
def init_tasks():
    # Remove trailing slash
    if "public_path" in env:
        public_path = env.public_path.rstrip("/")
        env.public_path = public_path


@hook("setup")
def setup():
    env.run("touch %s" % paths.get_shared_path("wp-config.php"))
    env.run("touch %s" % paths.get_shared_path(".htaccess"))


@hook("deploy")
def after_deploy():
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

    if "public_path" in env:
        paths.symlink(paths.get_current_path(), env.public_path)
