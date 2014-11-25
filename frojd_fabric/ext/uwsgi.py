# -*- coding: utf-8 -*-

"""
frojd_fabric.ext.uwsgi
----------------------
Methods for handling the uwsgi server.
"""

from fabric.state import env


def restart():
    env.run("service uwsgi restart")


def reload():
    env.run("touch %s" % env.uwsgi_ini_path)

