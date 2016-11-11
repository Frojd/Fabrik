# -*- coding: utf-8 -*-

"""
fabrik.transfer.scp
-------------------------
Transfer release by scp
"""

from fabric.state import env
from fabric.operations import local, put
from fabric.context_managers import settings, lcd, cd

from fabrik.hooks import hook
from fabrik.logger import logger

ignore_list = []


@hook("copy")
def copy():
    env.run('mkdir ' + env.current_release)

    with lcd('..'), cd(env.current_release):
        build_filename = "build.tar.gz"
        build_remote_path = "/".join([env.current_release, build_filename])

        local("ls | egrep -v 'build.tar.gz|git-hooks|scripts|deploy|docker' | xargs tar -zcf " + build_filename)
        put(build_filename, build_remote_path)
        env.run("tar -xzf " + build_remote_path)

        env.run("rm " + build_remote_path)
        local("rm build.tar.gz")
