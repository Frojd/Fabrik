# -*- coding: utf-8 -*-


"""
frojd_fabric.recipes.vendors.glesys_wordpress
---------------------------------------------
Wordpress recipe for Glesys Wordpress managed hosting.
"""

from frojd_fabric.recipes import wordpress
from frojd_fabric.ext import mysql


__version__ = "1.0.0"


@hook("before_deploy")
def backup_db():
    mysql.backup_db()

