"""
Example of a wordpress environment that creates a stage build.
"""

from fabric.state import env
from fabric.decorators import task
from fabrik.utils import get_stage_var


@task
def stage():
    from fabrik.recipes import wordpress
    wordpress.register()

    env.stage = "stage"
    env.branch = "develop"

    # SSH info are not needed on local deployment.
    env.hosts = [get_stage_var("HOST")]
    env.user = get_stage_var("USER")
    env.password = get_stage_var("PASSWORD")
    env.app_path = get_stage_var("APP_PATH")
    env.source_path = get_stage_var("APP_SOURCE_PATH", "src")

    # (Optional) Public path (example: var/www/yourproject)
    env.public_path = get_stage_var("PUBLIC_PATH")
