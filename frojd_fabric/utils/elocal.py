"""
fabric elocal - "local" command that raises an exception
---
Credit to https://gist.github.com/lost-theory/1831706
"""


from fabric.api import local, settings


class CommandFailed(Exception):
    def __init__(self, message, result):
        Exception.__init__(self, message)
        self.result = result

def elocal(*args, **kwargs):
    with settings(warn_only=True):
        result = local(*args, **kwargs)
        if result.failed:
            raise CommandFailed("args: %r, kwargs: %r, error code: %r"
                    % (args, kwargs, result.return_code), result)
        return result

