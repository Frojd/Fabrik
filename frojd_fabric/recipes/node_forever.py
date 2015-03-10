# -*- coding: utf-8 -*-

"""
frojd_fabric.recipes.node_forever
---------------------------------
This recipe is based on node, but introduces a forever reload on after_deploy
"""

from fabric.state import env
from frojd_fabric.hooks import hook
from frojd_fabric.ext import npm, forever, envfile
from frojd_fabric import paths
from frojd_fabric.recipes import node


@hook("setup")
def setup():
    envfile.create_env()


@hook("deploy")
def deploy():
    envfile.symlink_env()

    with(env.cd(paths.get_current_path())):
        npm.install()


@hook("after_deploy")
def after_deploy():
    with(env.cd(paths.get_current_path())):
        forever.restart()

