"""
Example of a django environment that creates a local build.
"""

import os.path
from fabric.state import env
from fabric.decorators import task
from fabric.context_managers import lcd
from frojd_fabric.utils import get_stage_var
from frojd_fabric.utils.elocal import elocal


@task
def local():
    from frojd_fabric.recipes import django

    # We use local versions of run, cd and exists
    env.run = elocal
    env.cd = lcd
    env.exists = os.path.exists

    env.stage = "local"
    env.branch = "develop"

    # SSH info are not needed on local deployment.
    # env.hosts = [get_stage_var("HOST")]
    # env.user = get_stage_var("USER")
    # env.password = get_stage_var("PASSWORD")
    env.app_path = get_stage_var("APP_PATH")
    env.source_path = get_stage_var("APP_SOURCE_PATH", "src")

    # Django
    env.requirements = "prod.txt"

    # Venv
    env.venv_path = get_stage_var("VENV_PATH")

