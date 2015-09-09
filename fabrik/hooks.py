# -*- coding: utf-8 -*-

"""
fabrik.hooks
------------------
A simple hook subscription utility, used when triggering recipe tasks.
"""

from functools import wraps
import inspect


_hooks = {}


def hook(name=None, priority=-1):
    """
    Decorator
    """

    def _hook(hook_func):
        return register_hook(name, hook_func=hook_func, priority=priority)

    return _hook


def register_hook(name, hook_func=None, priority=-1):
    if name not in _hooks:
        _hooks[name] = []

    hook_list = _hooks[name]

    if priority == -1:
        priority = len(hook_list)

    def _decorator(*args, **kwargs):
        return hook_func(*args, **kwargs)

    wrap = wraps(hook_func)(_decorator)
    wrap.hook_id = _get_hook_id(hook_func)

    hook_list.insert(min(len(hook_list), priority), wrap)

    return wrap


def _get_hook_id(hook_func):
    package_name = inspect.getmodule(hook_func).__name__
    full_path = "%s.%s" % (package_name, hook_func.__name__)

    return full_path


def run_hook(name, *args, **kwargs):
    if not has_hook(name):
        return

    hook_list = _hooks[name]
    for function in hook_list:
        function(*args, **kwargs)


def has_hook(name, hook_func=None):
    if name not in _hooks:
        return False

    if len(_hooks[name]) == 0:
        return False

    if not hook_func:
        return True

    for func in _hooks[name]:
        hook_id = _get_hook_id(hook_func)

        if hook_id == func.hook_id:
            return True

    return False


def unregister_hook(name, hook_func=None):
    if not has_hook(name, hook_func=hook_func):
        return

    hook_id = _get_hook_id(hook_func)

    for func in _hooks[name][:]:
        if hook_id == func.hook_id:
            _hooks[name].remove(func)
