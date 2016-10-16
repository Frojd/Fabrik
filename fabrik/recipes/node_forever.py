# -*- coding: utf-8 -*-

"""
fabrik.recipes.node_forever
---------------------------------
This recipe is based on node, but introduces a forever reload on after_deploy
"""

from fabric.state import env

from fabrik import paths, hooks
from fabrik.ext import forever
from fabrik.recipes import node


def after_deploy():
    with(env.cd(paths.get_current_path())):
        forever.restart()


def register():
    node.register()

    hooks.register_hook("after_deploy", after_deploy)


def unregister():
    node.unregiser()

    hooks.unregister_hook("after_deploy", after_deploy)
