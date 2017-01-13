# -*- coding: utf-8 -*-

"""
fabrik.api
----------------
This module implements the fabrik api.
"""

import time
import sys

from fabric.api import run
from fabric.state import env
from fabric.decorators import task, runs_once
from fabric.context_managers import cd
from fabric.contrib.files import exists

from utils import run_task
from hooks import run_hook, has_hook
import paths
from .logger import logger


def report(msg, err=None):
    logger.error(msg)

    if err:
        logger.error(err)

    if getattr(env, "raise_errors", True) and err:
        raise

    sys.exit(msg)


@runs_once
def init_tasks():
    """
    Performs basic setup before any of the tasks are run. All tasks needs to
    run this before continuing. It only fires once.
    """

    # Make sure exist are set
    if "exists" not in env:
        env.exists = exists

    if "run" not in env:
        env.run = run

    if "cd" not in env:
        env.cd = cd

    if "max_releases" not in env:
        env.max_releases = 5

    if "public_path" in env:
        public_path = env.public_path.rstrip("/")
        env.public_path = public_path

    run_hook("init_tasks")


@task
def setup():
    """
    Creates shared and upload directory then fires setup to recipes.
    """

    init_tasks()

    run_hook("before_setup")

    # Create shared folder
    env.run("mkdir -p %s" % (paths.get_shared_path()))
    env.run("chmod 755 %s" % (paths.get_shared_path()))

    # Create backup folder
    env.run("mkdir -p %s" % (paths.get_backup_path()))
    env.run("chmod 750 %s" % (paths.get_backup_path()))

    # Create uploads folder
    env.run("mkdir -p %s" % (paths.get_upload_path()))
    env.run("chmod 775 %s" % (paths.get_upload_path()))

    run_hook("setup")
    run_hook("after_setup")


@task
def deploy():
    """
    Performs a deploy by invoking copy, then generating next release name and
    invoking necessary hooks.
    """

    init_tasks()

    if not has_hook("copy"):
        return report("No copy method has been defined")

    if not env.exists(paths.get_shared_path()):
        return report("You need to run setup before running deploy")

    run_hook("before_deploy")

    release_name = int(time.time()*1000)
    release_path = paths.get_releases_path(release_name)

    env.current_release = release_path

    try:
        run_hook("copy")
    except Exception as e:
        return report("Error occurred on copy. Aborting deploy", err=e)

    if not env.exists(paths.get_source_path(release_name)):
        return report("Source path not found '%s'" %
                      paths.get_source_path(release_name))

    try:
        run_hook("deploy")
    except Exception as e:
        message = "Error occurred on deploy, starting rollback..."

        logger.error(message)
        logger.error(e)

        run_task("rollback")
        return report("Error occurred on deploy")

    # Symlink current folder
    paths.symlink(paths.get_source_path(release_name),
                  paths.get_current_path())

    # Clean older releases
    if "max_releases" in env:
        cleanup_releases(int(env.max_releases))

    run_hook("after_deploy")

    if "public_path" in env:
        paths.symlink(paths.get_source_path(release_name), env.public_path)

    logger.info("Deploy complete")


@task
def rollback():
    """
    Rolls back to previous release
    """

    init_tasks()

    run_hook("before_rollback")

    # Remove current version
    current_release = paths.get_current_release_path()
    if current_release:
        env.run("rm -rf %s" % current_release)

    # Restore previous version
    old_release = paths.get_current_release_name()
    if old_release:
        paths.symlink(paths.get_source_path(old_release),
                      paths.get_current_path())

    run_hook("rollback")
    run_hook("after_rollback")

    logger.info("Rollback complete")


@task
def cleanup_releases(limit=5):
    """
    Removes older releases.
    """

    init_tasks()

    max_versions = limit + 1

    env.run("ls -dt %s/*/ | tail -n +%s | xargs rm -rf" % (
        paths.get_releases_path(),
        max_versions)
    )


@task
def debug():
    """
    Outputs debug information, needs to run before the task".

    Example:
        fab prod debug deploy.
    """

    from fabric.network import ssh

    init_tasks()

    ssh.util.log_to_file("fabrik-debug.log", 10)


@task
def test():
    """
    Prints environment information.
    """

    init_tasks()

    env.run("cat /etc/*-release")  # List linux dist info
