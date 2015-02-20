# -*- coding: utf-8 -*-

"""
frojd_fabric.ext.virtualenv
---------------------------
Holds methods for managing virtualenv.
"""

from fabric.decorators import task
from fabric.state import env
from frojd_fabric import paths
from unipath import Path


@task
def create_venv():
    if "venv_path" not in env:
        raise Exception("No env.venv_path has been specified")

    env.run("virtualenv %s" % get_path())


@task
def update_requirements():
    if "requirements" not in env:
        raise Exception("Missing env.requirements")

    env.run("pip install -r %s" % Path(
        env.current_release, "requirements", env.requirements),
    )


def get_path():
    if "venv_path" in env:
        return env.venv_path

    return paths.get_deploy_path("venv")


