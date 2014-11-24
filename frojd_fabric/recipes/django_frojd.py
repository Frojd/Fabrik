from frojd_fabric.hooks import hook
from frojd_fabric.ext import uwsgi
from frojd_fabric.recipes import django


@hook("after_deploy")
def after_deploy():
    uwsgi.reload()

