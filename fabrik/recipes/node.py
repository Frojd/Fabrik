# -*- coding: utf-8 -*-

"""
fabrik.recipes.node
---------------------------------
Recipe for node.js that includes envfile
"""

from fabric.state import env

from fabrik import paths, hooks
from fabrik.ext import npm, envfile


def setup():
    envfile.create_env()


def deploy():
    envfile.symlink_env()

    with(env.cd(paths.get_source_path(env.current_release))):
        npm.install()


def register():
    hooks.register_hook("setup", setup)
    hooks.register_hook("deploy", deploy)


def unregister():
    hooks.unregister_hook("setup", setup)
    hooks.unregister_hook("deploy", deploy)
