from fabric.decorators import task
from fabric.state import env
from frojd_fabric import paths
from unipath import Path


@task
def create_env():
    env.run("touch %s" % paths.get_shared_path(".env"))


@task
def symlink_env():
    paths.symlink(
        paths.get_shared_path(".env"),
        paths.get_current_path(".env")
    )
