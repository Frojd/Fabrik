"""
Example of a production environment that uses django + uwsgi
"""

from fabric.state import env
from fabric.api import run
from fabric.decorators import task
from fabric.context_managers import cd
from frojd_fabric.utils import get_stage_var


@task
def demo():
    from frojd_fabric.recipes import django_uwsgi

    env.run = run
    env.cd = cd

    env.stage = "prod"
    env.branch = "master"

    # Standard config
    env.hosts = [get_stage_var("HOST")]
    env.user = get_stage_var("USER")
    env.password = get_stage_var("PASSWORD")
    env.app_path = get_stage_var("APP_PATH")
    env.source_path = get_stage_var("APP_SOURCE_PATH", "src")

    # Django
    env.requirements = "prod.txt"

    # Virtualenv
    env.venv_path = get_stage_var("VENV_PATH")

    # UWSGI
    env.uwsgi_ini_path = get_stage_var("UWSGI_INI_PATH")
