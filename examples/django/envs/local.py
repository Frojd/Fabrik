"""
Example of a django environment that creates a local build.
"""

from fabric.state import env
from fabric.decorators import task
from fabric.context_managers import lcd
from frojd_fabric.utils import get_stage_var
from frojd_fabric.utils.elocal import elocal


@task
def local():
    from frojd_fabric.recipes import django

    env.run = elocal        # We use local versions of run and cd,
    env.cd = lcd

    env.stage = "local"
    env.branch = "develop"

    # Standard config
    env.user = "root"
    env.password = "password"
    env.app_path = get_stage_var("APP_PATH")
    env.source_path = get_stage_var("APP_SOURCE_PATH", "src")
    env.warn_only = False

    # Django
    env.requirements = "prod.txt"

    # Venv
    env.venv_path = get_stage_var("VENV_PATH")

