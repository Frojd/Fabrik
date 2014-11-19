# -*- coding: utf-8 -*-

"""
hooks
-----
A simple hook subscription utility.
"""

from functools import wraps


_hooks = {}

def hook(hook=None, priority=-1):
    if not hook in _hooks:
        _hooks[hook] = []

    hook_list = _hooks[hook]

    if priority == -1:
        priority = len(hook_list)

    def _hook(view_func):
        def _decorator(*args, **kwargs):
            return view_func(*args, **kwargs)

        wrap = wraps(view_func)(_decorator)
        hook_list.insert(min(len(hook_list), priority), wrap)

        return wrap
    return _hook


def run_hook(hook, *args, **kwargs):
    if not has_hook(hook):
        return

    hook_list = _hooks[hook]
    for hook_function in hook_list:
        hook_function(*args, **kwargs)


def has_hook(hook):
    return hook in _hooks
