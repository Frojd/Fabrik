# -*- coding: utf-8 -*-

from fabric.decorators import task
from fabric.context_managers import cd, prefix
from fabric.state import env
from fabric.api import execute
from fabric.task_utils import crawl
from fabric import state
from utils import run_task, has_task
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
        raise Exception("No copy method has been defined")
        return

    # run_task("before_deploy")
    run_hook("before_deploy")

    release_name = int(time.time())
    release_path = paths.get_releases_path(release_name)

    env.current_release = release_path

    try:
        run_hook("copy")
    except Exception, e:
        print e
        print "Error occured on copy, starting rollback..."
        run_task("rollback")

    # Symlink current folder
    paths.symlink(paths.get_source_path(release_name), paths.get_current_path())


    try:
        run_hook("deploy")
    except Exception, e:
        print e
        print "Error occured in deploy, starting rollback..."
        run_task("rollback")
        return

    # Clean older releases
    if "max_releases" in env:
        cleanup_releases(int(env.max_releases))

    run_hook("after_deploy")


@task
def rollback():
    print "Rolling back!"

    # env.run("rm -rf %s" % env.

    run_hook("rollback")


@task
def cleanup_releases(limit=5):
    max_versions = limit + 1

    env.run("ls -dt %s/*/ | tail -n +%s | xargs rm -rf" % (
        paths.get_releases_path(),
        max_versions)
    )

