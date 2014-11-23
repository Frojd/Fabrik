# -*- coding: utf-8 -*-

from fabric.decorators import task
from fabric.state import env
from utils import run_task
from logger import logger
import paths
import time
from hooks import run_hook, has_hook


@task
def setup():
    run_hook("before_setup")

    # Create shared folder
    env.run("mkdir -p %s" % (paths.get_shared_path()))
    env.run("chmod 755 %s" % (paths.get_shared_path()))

    # Create uploads folder
    env.run("mkdir -p %s" % (paths.get_upload_path()))
    env.run("chmod 777 %s" % (paths.get_upload_path()))

    run_hook("setup")
    run_hook("after_setup")


@task
def deploy():
    if not has_hook("copy"):
        logger.error("No copy method has been defined")
        return


    # run_task("before_deploy")
    run_hook("before_deploy")

    release_name = int(time.time())
    release_path = paths.get_releases_path(release_name)

    env.current_release = release_path

    try:
        run_hook("copy")
    except Exception, e:
        logger.error("Error occured on copy, starting rollback...")
        logger.error(e)

        run_task("rollback")
        return

    # Symlink current folder
    paths.symlink(paths.get_source_path(release_name), paths.get_current_path())


    try:
        run_hook("deploy")
    except Exception, e:
        logger.error("Error occured on deploy, starting rollback...")
        logger.error(e)

        run_task("rollback")
        return

    # Clean older releases
    if "max_releases" in env:
        cleanup_releases(int(env.max_releases))

    run_hook("after_deploy")

    logger.info("Deploy complete")


@task
def rollback():
    run_hook("before_rollback")

    # Remove version
    env.run("rm -rf %s" % paths.get_current_release_path())

    # Restore to previous version
    paths.symlink(paths.get_current_release_path(), paths.get_current_path())

    run_hook("rollback")
    run_hook("after_rollback")

    logger.info("Rollback complete")


@task
def cleanup_releases(limit=5):
    max_versions = limit + 1

    env.run("ls -dt %s/*/ | tail -n +%s | xargs rm -rf" % (
        paths.get_releases_path(),
        max_versions)
    )

