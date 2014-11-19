import time

from fabric.context_managers import cd, prefix
from fabric.decorators import task
from fabric.operations import local
from fabric.state import env
from fabric.api import run


__author__ = "frojd"


REPRO_URL = "SomeRepo"


"""Environments"""


@task
def prod():
    env.domain = ""
    env.stage = ""
    env.symlink_name = ""
    env.hosts = [env.PROD_HOST]
    env.user = env.PROD_USER

    if "PROD_PASSWORD" in env:
        env.password = env.PROD_PASSWORD
    else:
        env.key_filename = env.PROD_KEY_FILENAME

    env.branch = "master"
    env.warn_only = True
    env.requirements = "prod.txt"
    env.run = run
    env.app_path = env.PROD_APP_PATH
    env.venv_path = env.PROD_APP_PATH


@task
def dev():
    env.stage = env.DEV_APP_NAME
    env.symlink_name = "current"
    env.hosts = [env.DEV_HOST]
    env.user = env.DEV_USER

    if "DEV_PASSWORD" in env:
        env.password = env.DEV_PASSWORD
    else:
        env.key_filename = env.DEV_KEY_FILENAME

    env.branch = env.DEV_BRANCH
    env.warn_only = True
    env.requirements = env.DEV_APP_REQUIERMENTSFILE
    env.run = run
    env.app_path = env.DEV_APP_PATH
    env.venv_path = env.DEV_VENV_PATH


"""Commands"""


@task
def setup():
    run("mkdir -p %s" % (_get_shared_path()))
    run("chmod 755 %s" % (_get_shared_path()))
    run("mkdir -p %s" % (_get_upload_path()))
    run("chmod 777 %s" % (_get_upload_path()))
    # Create files
    run("touch %s/.env" % (_get_shared_path()))

# This task is for the internal demoserver only
@task
def setup_demo():
    run("mkdir -p %s" % (_get_shared_path()))
    run("chmod 755 %s" % (_get_shared_path()))
    run("mkdir -p %s" % (_get_upload_path()))
    run("chmod 777 %s" % (_get_upload_path()))
    # Create files
    run("touch %s/.env" % (_get_shared_path()))
    run("virtualenv %s/%s_venv" % (_get_deploy_path(), env.stage))
    run("cp /var/django/uwsgi_template.ini %s/%s_uwsgi.ini" % (_get_deploy_path(), env.stage))


@task
def deploy():
    release_name = int(time.time())
    release_path = "%s/%s" % (_get_releases_path(), release_name)

    # with(cd(env.app_path)):
    #     env.run("git clone  -b %(branch)s git@github.com:%(repro)s %(path)s" % {
    #         "branch": env.branch,
    #         "repro": REPRO_URL,
    #         "path": release_path
    #     })
    run("mkdir -p %s" % (release_path))
    run("touch %s/testfile.txt" % (release_path))

    run("ln -nsf %s %s" % (release_path,
                           _get_current_path()))

    remove_old_versions()

    # run("ln -nsf %s %s/%s" % (_get_deploy_path()+"/current/"+env.stage,
    #                           env.app_path, env.symlink_name))

    #symlink_shared()

    #with prefix("source %s" % (env.venv_path+"/bin/activate")):
        #_update_requirements()
        #_migrate()
        #reload_uwsgi()

    # TODO: Remove older releases


@task
def rollback():
    pass

@task
def remove_old_versions():
    if not "MAX_VERSIONS" in env:
        return

    if env.DEV_MAX_VERSIONS and _get_releases_path().endswith("/releases"):
        max_versions = int(env.DEV_MAX_VERSIONS)
        max_versions = max_versions + 1

        run("ls -dt %s/*/ | tail -n +%s | xargs rm -rf" % (_get_releases_path(),
            max_versions))

@task
def restart_nginx():
    run("service nginx restart")

@task
def reload_nginx():
    run("nginx -s reload")

@task
def restart_gunicorn():
    run("service gunicorn restart")

@task
def restart_uwsgi():
    run("service uwsgi restart")


@task
def reload_uwsgi():
    run("touch %s/%s_uwsgi.ini" % (_get_deploy_path(), env.stage))

# @task
# def reload_uwsgi():
#     run("uwsgi --reload /tmp/project-%s.pid" % (env.stage))

@task
def restart_celery():
    run("service celeryd restart")


@task
def backup_db():
    pass


@task
def restore_db():
    pass


@task
def symlink_shared():
    run("ln -nsf %s %s " % (_get_shared_path()+"/.env",
                            _get_current_path()+"/"+env.stage+"/.env"))


def _get_deploy_path():
    return env.app_path


def _get_releases_path():
    return _get_deploy_path()+"/releases"


def _get_shared_path():
    return _get_deploy_path()+"/shared"


def _get_current_path():
    return _get_deploy_path()+"/current"


def _get_upload_path():
    return _get_deploy_path()+"/upload"


def _update_requirements():
    run("pip install -r %(path)s/requirements/%(file)s" % {
        "path": _get_current_path(),
        "file": env.requirements
    })


def _migrate():
    with(cd("%s/%s/" % (_get_current_path(), env.stage))):
        run("python manage.py migrate")

