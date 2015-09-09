# -*- coding: utf-8 -*-

"""
fabrik.recipes.node
---------------------------------
Recipe for node.js that includes envfile
"""

from fabric.state import env
from fabrik.hooks import hook
from fabrik.ext import npm, forever, envfile
from fabrik import paths


@hook("setup")
def setup():
    envfile.create_env()


@hook("deploy")
def deploy():
    envfile.symlink_env()

    with(env.cd(paths.get_current_path())):
        npm.install()

