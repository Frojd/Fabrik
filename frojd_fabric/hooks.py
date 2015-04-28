# -*- coding: utf-8 -*-

"""
frojd_fabric.hooks
------------------
A simple hook subscription utility, used when triggering recipe tasks.
"""

from functools import wraps
import inspect


_hooks = {}


def hook(hook_name=None, priority=-1):
    """
    Decorator
    """

    def _hook(view_func):
        return register_hook(hook_name, view_func=view_func, priority=priority)

    return _hook


def register_hook(hook_name, view_func=None, priority=-1):
    if hook_name not in _hooks:
        _hooks[hook_name] = []

    hook_list = _hooks[hook_name]

    if priority == -1:
        priority = len(hook_list)

    def _decorator(*args, **kwargs):
        return view_func(*args, **kwargs)

    wrap = wraps(view_func)(_decorator)
    wrap.hook_id = _get_hook_id(view_func)

    hook_list.insert(min(len(hook_list), priority), wrap)

    return wrap


def _get_hook_id(view_func):
    package_name = inspect.getmodule(view_func).__name__
    full_path = "%s.%s" % (package_name, view_func.__name__)

    return full_path


def run_hook(hook_name, *args, **kwargs):
    if not has_hook(hook_name):
        return

    hook_list = _hooks[hook_name]
    for hook_function in hook_list:
        hook_function(*args, **kwargs)


def has_hook(hook_name, view_func=None):
    if hook_name not in _hooks:
        return False

    if len(_hooks[hook_name]) == 0:
        return False

    if not view_func:
        return True

    for hook_func in _hooks[hook_name]:
        hook_id = _get_hook_id(view_func)

        if hook_id == hook_func.hook_id:
            return True

    return False


def unregister_hook(hook_name, view_func=None):
    if not has_hook(hook_name, view_func=view_func):
        return

    hook_id = _get_hook_id(view_func)

    for hook_func in _hooks[hook_name][:]:
        if hook_id == hook_func.hook_id:
            _hooks[hook_name].remove(hook_func)
