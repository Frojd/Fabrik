# -*- coding: utf-8 -*-

"""
fabrik.utils
------------------
Contains various utility function, such as hooks and way of retriving config
"""

from fabric.task_utils import crawl
from fabric.api import execute
from fabric import state
from fabric.state import env
from ..logger import logger


def run_task(task):
    """
    A method of running fabric task with silent errors.
    """

    if has_task(task):
        execute(task)


def has_task(task):
    """
    Checks if fabric task exists
    """

    return crawl(task, state.commands) is not None


def get_stage_var(name, default=None):
    if "stage" not in env:
        raise Exception("env.stage cannot be empty")

    key = "%s_%s" % (env.stage.upper(), name)

    if default is None:
        return env["%s_%s" % (env.stage.upper(), name)]

    return env.get(key, default)


def get_var(name):
    return env[name]
