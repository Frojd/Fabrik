# -*- coding: utf-8 -*-


"""
fabrik.recipes.vendors.glesys_wordpress
---------------------------------------------
Wordpress recipe for Glesys Wordpress managed hosting.
"""

from fabrik.recipes import wordpress
from fabrik.ext import mysql


__version__ = "1.0.0"


@hook("before_deploy")
def backup_db():
    mysql.backup_db()
