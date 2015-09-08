# -*- coding: utf-8 -*-

"""
fabrik.recipes.django_uwsgi
---------------------------------
This recipe is based on django, but introduces a uwsgi reload after_deploy
"""

from fabrik.hooks import hook
from fabrik.ext import uwsgi
from fabrik.recipes import django


@hook("setup")
def setup():
    # TODO: Copy .ini file from templates to server
    pass


@hook("after_deploy")
def after_deploy():
    uwsgi.touch_reload()
