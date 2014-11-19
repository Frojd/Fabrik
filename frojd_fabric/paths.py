# -*- coding: utf-8 -*-

from fabric.state import env
from unipath import Path


def get_deploy_path(child=None):
    path = Path(env.app_path)

    if child:
        path = Path(path, child)

    return path


# TODO: Make this work
def get_latest_release_path():
    return _path_optional(get_deploy_path(), "releases", "test")

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
