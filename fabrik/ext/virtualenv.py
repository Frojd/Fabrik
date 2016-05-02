# -*- coding: utf-8 -*-

"""
fabrik.ext.virtualenv
---------------------------
Holds methods for managing virtualenv.
"""

import os
from unipath import Path
from fabric.decorators import task
from fabric.operations import prompt
from fabric.state import env

from fabrik import paths
from ..logger import logger


@task
def create_venv():
    if "venv_path" not in env:
        raise Exception("No env.venv_path has been specified")

    # Checks if venv exist and prompts user if reinstalling is an option
    if env.exists(Path(get_path(), "bin")):
        logger.warn("Virtualenv is already installed")
        prompt_result = prompt("Install anyways:", default="no")

        if prompt_result == "no":
            return

    env.run("virtualenv %s" % get_path())


@task
def update_requirements():
    req_dir = None
    req_path = None

    if "requirements_root" in env:
        req_dir = os.path.join(env.current_release, env.requirements_root)

    if not req_dir:
        req_dir = os.path.join(env.current_release, "requirements")

    if "requirements" in env:
        req_path = Path(req_dir, env.requirements)

    if not req_path:
        req_path = Path(req_dir, "%s.txt" % env.stage)

    if not env.exists(req_path):
        raise Exception("Requirement file not found at %s" % req_path)

    env.run("pip install -r %s" % req_path)


def get_path():
    if "venv_path" in env:
        return env.venv_path

    return paths.get_deploy_path("venv")
