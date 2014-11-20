from fabric.state import env
from fabric.decorators import task
from fabric.operations import local
from frojd_fabric.utils import get_stage_var


@task
def demo(default=True):
    env.run = local
    env.stage = "demo"
    env.branch = "develop"
    #env.domain = ""
    # env.symlink_name = ""
    #env.hosts = []
    env.user = "root"
    env.password = "password"
    env.app_path = get_stage_var("APP_PATH")
    env.source_path = get_stage_var("APP_SOURCE_PATH")
    env.warn_only = True
    env.max_releases = 5

    # Django
    env.requirements = "prod.txt"
