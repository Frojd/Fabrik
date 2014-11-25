"""
Example of a django environment that creates a local build.
"""

from fabric.state import env
from fabric.decorators import task
from fabric.context_managers import lcd
from frojd_fabric.utils import get_stage_var
from frojd_fabric.utils.elocal import elocal


@task
def local_django(default=True):
    from frojd_fabric.recipes import django

    env.run = elocal
    env.cd = lcd
    env.stage = "local"
    env.branch = "develop"
    # env.domain = ""
    # env.symlink_name = ""
    # env.hosts = []
    env.user = "root"
    env.password = "password"
    env.app_path = get_stage_var("APP_PATH")
    env.source_path = get_stage_var("APP_SOURCE_PATH")
    env.warn_only = False
    env.max_releases = 5

    # Django
    env.requirements = "prod.txt"

    # Venv
    env.venv_path = get_stage_var("VENV_PATH")
