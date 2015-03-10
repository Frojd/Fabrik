# -*- coding: utf-8 -*-

"""
frojd_fabric.ext.nginx
----------------------
Methods for handling nginx
"""

from fabric.state import env


def restart():
    env.run("service nginx restart")


def reload():
    env.run("nginx -s reload")

