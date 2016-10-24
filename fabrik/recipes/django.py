# -*- coding: utf-8 -*-

"""
fabrik.recipes.django
---------------------------
This recipe holds the most standard components of a django installation.
"""

from fabric.state import env
from fabric.context_managers import prefix

from fabrik import paths, hooks
from fabrik.ext import envfile, virtualenv


def setup():
    envfile.create_env()
    virtualenv.create_venv()


def deploy():
    envfile.symlink_env()

    with prefix("source %s" % (virtualenv.get_path()+"/bin/activate")):
        virtualenv.update_requirements()
        _migrate()

    if "public_path" in env:
        paths.symlink(paths.get_current_path(), env.public_path)


def after_deploy():
    with prefix("source %s" % (virtualenv.get_path()+"/bin/activate")):
        _collectstatic()


def _migrate():
    with(env.cd(paths.get_source_path(env.current_release))):
        env.run("python manage.py migrate --noinput")


def _collectstatic():
    with(env.cd(paths.get_source_path(env.current_release))):
        env.run("python manage.py collectstatic --noinput", warn_only=True)


def rollback():
    # TODO: Add migration rollback logic.
    pass


def register():
    hooks.register_hook("setup", setup)
    hooks.register_hook("deploy", deploy)
    hooks.register_hook("after_deploy", after_deploy)
    hooks.register_hook("rollback", rollback)


def unregister():
    hooks.unregister_hook("setup", setup)
    hooks.unregister_hook("deploy", deploy)
    hooks.unregister_hook("after_deploy", after_deploy)
    hooks.unregister_hook("rollback", rollback)
