# -*- coding: utf-8 -*-

from fabric.task_utils import crawl
from fabric.api import execute
from fabric import state
from fabric.state import env


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


def get_stage_var(name):
    return env["%s_%s" % (env.stage.upper(), name)]
