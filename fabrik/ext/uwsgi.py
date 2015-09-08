# -*- coding: utf-8 -*-

"""
fabrik.ext.uwsgi
----------------------
Methods for handling the uwsgi server.
"""

from fabric.state import env


def restart():
    env.run("service uwsgi restart")


# This is deprecated, use touch_restart() instead
def touch_reload():
    touch_restart()


def touch_restart():
    env.run("touch %s" % env.uwsgi_ini_path)


def service_reload():
    env.run("service uwsgi reload")


def service_restart():
    env.run("service uwsgi restart")
