# -*- coding: utf-8 -*-

"""
fabrik.utils.erun
-----------------------
Fabric "run" command that raises an exception
"""

from fabric.api import run, settings


class RunFailedCommand(Exception):
    def __init__(self, message, result):
        Exception.__init__(self, message)
        self.result = result


def erun(*args, **kwargs):
    with settings(warn_only=True):
        result = run(*args, **kwargs)
        if result.failed:
            raise RunFailedCommand("args: %r, kwargs: %r, error code: %r"
                                   % (args, kwargs, result.return_code),
                                   result)
        return result
