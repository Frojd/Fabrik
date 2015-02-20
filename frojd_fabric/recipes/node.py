# -*- coding: utf-8 -*-

"""
frojd_fabric.recipes.node
---------------------------------
Recipe for node.js that includes envfile
"""

from fabric.state import env
from frojd_fabric.hooks import hook
from frojd_fabric.ext import npm, forever, envfile
from frojd_fabric import paths


@hook("setup")
def setup():
    envfile.create_env()


@hook("deploy")
def deploy():
    envfile.symlink_env()

    with(env.cd(paths.get_current_path())):
        npm.install()

