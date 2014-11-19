from fabric.decorators import task
from fabric.state import env
from frojd_fabric import paths
from unipath import Path


@task
def create_venv():
    env.run("virtualenv %s" % paths.get_deploy_path("venv"))


@task
def update_requirements():
    env.run("pip install -r %s" %
        Path(env.current_release, "requirements", env.requirements),
    )
