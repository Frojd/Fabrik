"""
Example of a wordpress environment that creates a prod build.
"""

import os.path
from fabric.state import env
from fabric.decorators import task
from frojd_fabric.utils import get_stage_var
from frojd_fabric.hooks import hook


@task
def stage():
    from frojd_fabric.recipes import wordpress

    env.stage = "prod"
    env.branch = "master"

    # SSH info are not needed on local deployment.
    env.hosts = [get_stage_var("HOST")]
    env.user = get_stage_var("USER")
    env.password = get_stage_var("PASSWORD")
    env.app_path = get_stage_var("APP_PATH")
    env.source_path = get_stage_var("APP_SOURCE_PATH", "src")

    # (Optional) Public path (example: var/www/yourproject)
    env.public_path = get_stage_var("PUBLIC_PATH")
