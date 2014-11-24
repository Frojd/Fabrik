from fabric.decorators import task
from fabric.state import env
from frojd_fabric import paths
from unipath import Path


@task
def create_venv():
    if "venv_path" not in env:
        # logger.error("No venv_path has been specified")
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


