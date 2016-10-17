# -*- coding: utf-8 -*-

"""
fabrik.recipes.django_uwsgi
---------------------------------
This recipe is based on django, but introduces a uwsgi reload on after_deploy
"""

from fabrik.ext import uwsgi
from fabrik.recipes import django
from fabrik import hooks


def after_deploy():
    uwsgi.service_restart()


def register():
    django.register()

    hooks.register_hook("after_deploy", after_deploy)


def unregister():
    django.unregister()

    hooks.unregister_hook("after_deploy", after_deploy)
