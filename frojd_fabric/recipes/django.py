from fabric.state import env
from fabric.context_managers import prefix
from frojd_fabric.ext import envfile, virtualenv
from frojd_fabric import paths
from frojd_fabric.hooks import hook


@hook("after_setup")
def after_setup():
    envfile.create_env()
    virtualenv.create_venv()


@hook("deploy")
def after_deploy():
    envfile.symlink_env()

    with prefix("source %s" % (virtualenv.get_path()+"/bin/activate")):
        virtualenv.update_requirements()
        _migrate()
        reload_uwsgi()


def _migrate():
    with(env.cd(paths.get_current_path())):
        env.run("python manage.py migrate")


@hook("deploy")
def reload_uwsgi():
    # env.run("touch %s/%s_uwsgi.ini" % (paths.get_deploy_path(), env.stage))
    pass


@hook("rollback")
def rollback():
    pass
