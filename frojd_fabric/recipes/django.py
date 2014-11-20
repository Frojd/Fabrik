from fabric.state import env
from fabric.decorators import task
from fabric.context_managers import cd, prefix
from frojd_fabric import setup, deploy, rollback
from frojd_fabric.transfer.git import copy
from frojd_fabric.ext import envfile, virtualenv
from frojd_fabric import paths
from frojd_fabric.hooks import hook, run_hook
from envs import demo
from unipath import Path


@hook("after_setup")
def after_setup():
    envfile.create_env()
    env.run("virtualenv %s" % paths.get_deploy_path("venv"))


@hook("deploy")
def after_deploy():
    envfile.symlink_env()

    with prefix("source %s" % (paths.get_deploy_path("venv")+"/bin/activate")):
        virtualenv.update_requirements()
        # _update_requirements()
        # _migrate()
        # reload_uwsgi()


def _migrate():
    with(cd("%s/%s/" % (paths.get_current_path(), env.stage))):
        env.run("python manage.py migrate")


@hook("deploy")
def reload_uwsgi():
    env.run("touch %s/%s_uwsgi.ini" % (paths.get_deploy_path(), env.stage))


@hook("rollback")
def rollback():
    pass
