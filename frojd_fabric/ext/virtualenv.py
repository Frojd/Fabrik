from fabric.decorators import task
from fabric.state import env
from frojd_fabric import paths
from unipath import Path
from frojd_fabric.logger import logger


@task
def create_venv():
    if "venv_path" not in env:
        raise Exception("No env.venv_path has been specified")
        return

    env.run("virtualenv %s" % get_path())


@task
def update_requirements():
    env.run("pip install -r %s" % Path(
        env.current_release, "requirements", env.requirements),
    )


def get_path():
    if "venv_path" in env:
        return env.venv_path

    return paths.get_deploy_path("venv")


