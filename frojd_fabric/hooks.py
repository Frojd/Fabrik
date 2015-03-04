# -*- coding: utf-8 -*-

"""
frojd_fabric.hooks
------------------
A simple hook subscription utility, used when triggering recipe tasks.
"""

from functools import wraps


_hooks = {}


def hook(hook_name=None, priority=-1):
    """
    Decorator
    """

    if not hook_name in _hooks:
        _hooks[hook_name] = []

    hook_list = _hooks[hook_name]

    if priority == -1:
        priority = len(hook_list)

    def _hook(view_func):
        def _decorator(*args, **kwargs):
            return view_func(*args, **kwargs)

        wrap = wraps(view_func)(_decorator)
        hook_list.insert(min(len(hook_list), priority), wrap)

        return wrap
    return _hook


def run_hook(hook_name, *args, **kwargs):
    if not has_hook(hook_name):
        return

    hook_list = _hooks[hook_name]
    for hook_function in hook_list:
        hook_function(*args, **kwargs)


def has_hook(hook_name):
    return hook_name in _hooks

