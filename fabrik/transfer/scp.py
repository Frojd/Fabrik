# -*- coding: utf-8 -*-

"""
fabrik.transfer.scp
-------------------------
Transfer release by scp

Params:
    env.local_app_path: Manually defined path to local app path
    env.scp_ignore_list: A list of paths that should be ignored on sync
"""

from fabric.state import env
from fabric.operations import local, put
from fabric.context_managers import lcd, cd

from fabrik import paths
from fabrik.hooks import hook
from fabrik.utils.elocal import elocal


def get_local_app_path():
    if 'local_app_path' in env:
        return env.local_app_path

    path = elocal('git rev-parse --show-toplevel', capture=True)
    return path


@hook("copy")
def copy():
    default_ignore_list = ['build.tar.gz', ]
    ignore_list = []

    if 'scp_ignore_list' in env:
        ignore_list = env.scp_ignore_list

    ignore_list = ignore_list + default_ignore_list

    path = get_local_app_path()
    release_path = paths.get_deploy_path(env.current_release)

    env.run('mkdir -p {}'.format(release_path))

    with lcd(path), cd(release_path):
        build_filename = 'build.tar.gz'
        build_remote_path = "/".join([env.current_release, build_filename])

        exclude_args = map(lambda x: '--exclude="{}"'.format(x), ignore_list)

        local('tar {} -czf {} *'.format(
            ' '.join(exclude_args),
            build_filename
        ))

        put(build_filename, build_remote_path)
        env.run('tar -xzf {}'.format(build_filename))

        env.run('rm {}'.format(build_remote_path))
        local("rm build.tar.gz")
