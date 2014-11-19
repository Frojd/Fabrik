from fabric.state import env
from fabric.decorators import task
from fabric.operations import local
from frojd_fabric.utils import get_stage_var


@task
def demo(default=True):
    env.stage = "demo"
    env.domain = ""
    env.symlink_name = ""
    env.hosts = []
    env.user = "root"
    env.password = "password"
    env.run = local
    env.app_path = get_stage_var("APP_PATH")
    env.source_path = get_stage_var("APP_SOURCE_PATH")
    env.branch = "develop"
    env.warn_only = True
    env.requirements = "prod.txt"
    env.max_releases = 5
