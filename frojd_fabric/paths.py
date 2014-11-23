# -*- coding: utf-8 -*-

from fabric.state import env
from unipath import Path


def get_deploy_path(child=None):
    path = Path(env.app_path)

    if child:
        path = Path(path, child)

    return path


def get_current_release_path():
    path = env.run(
        "ls -dt %s/*/ | sort -n -t _ -k 2 | tail -1" %
        get_releases_path(), capture=True)

    if not path:
        return

    release = Path(path)

    try:
        int(release.absolute().name)
    except ValueError, e:
        print e
        return

    return release


def get_releases_path(child=None):
    return _path_optional(get_deploy_path(), "releases", child)


def get_shared_path(child=None):
    return _path_optional(get_deploy_path(), "shared", child)


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
