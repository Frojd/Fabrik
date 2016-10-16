# -*- coding: utf-8 -*-

"""
fabrik.paths
------------------
This module generates the various paths used by fabrik.
"""

from fabric.state import env
from unipath import Path


def get_deploy_path(child=None):
    path = Path(env.app_path)

    if child:
        path = Path(path, child)

    return path


def get_current_release_path(child=None):
    release_name = get_current_release_name()

    if not release_name:
        return

    path = get_releases_path(release_name)

    if child:
        path = Path(path, child)

    return path


def get_current_release_name():
    run_args = {}

    # Append capture value if we are running locally
    if env.run.__name__ == "elocal":
        run_args["capture"] = True

    path = env.run(
        "ls -dt %s/*/ | sort -n -t _ -k 2 | tail -1" %
        get_releases_path(), **run_args)

    if not path:
        return

    release = Path(path)

    try:
        int(release.absolute().name)
    except ValueError as e:
        print e
        return

    return release.absolute().name


def get_releases_path(child=None):
    return _path_optional(get_deploy_path(), "releases", child)


def get_shared_path(child=None):
    return _path_optional(get_deploy_path(), "shared", child)


def get_backup_path(child=None):
    return _path_optional(get_deploy_path(), "backup", child)


def get_current_path(child=None):
    return _path_optional(get_deploy_path(), "current", child)


def get_upload_path(child=None):
    return _path_optional(get_deploy_path(), "upload", child)


def get_source_path(release):
    path = get_releases_path(release)

    if "source_path" in env:
        path = Path(path, env.source_path)

    return path


def _path_optional(base, sub, child=None):
    path = Path(base, sub)

    if child:
        path = Path(path, child)

    return path


def symlink(origin, dest):
    env.run("ln -nsf %s %s " % (origin, dest))
