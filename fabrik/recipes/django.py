# -*- coding: utf-8 -*-

"""
fabrik.recipes.django
---------------------------
This recipe holds the most standard components of a django installation.
"""

from fabric.state import env
from fabric.context_managers import prefix
from fabrik.ext import envfile, virtualenv
from fabrik import paths
from fabrik.hooks import hook


@hook("init_tasks")
def init_tasks():
    # Remove trailing slash
    if "public_path" in env:
        public_path = env.public_path.rstrip("/")
        env.public_path = public_path


@hook("setup")
def setup():
    envfile.create_env()
    virtualenv.create_venv()


@hook("deploy")
def after_deploy():
    envfile.symlink_env()

    with prefix("source %s" % (virtualenv.get_path()+"/bin/activate")):
        virtualenv.update_requirements()
        _migrate()

        # Handle invalid collectstatic gracefully
        _collectstatic()

    if "public_path" in env:
        paths.symlink(paths.get_current_path(), env.public_path)


def _migrate():
    with(env.cd(paths.get_current_path())):
        env.run("python manage.py migrate --noinput")


def _collectstatic():
    with(env.cd(paths.get_current_path())):
        env.run("python manage.py collectstatic --noinput", warn_only=True)


@hook("rollback")
def rollback():
    # TODO: Add migration rollback logic.
    pass
