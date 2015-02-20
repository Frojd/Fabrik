# -*- coding: utf-8 -*-

"""
frojd_fabric.ext.composer
-------------------------
Contains methods for syncing composer packages
"""

from fabric.decorators import task
from fabric.state import env
from frojd_fabric import paths


@task
def install():
    release_path = paths.get_current_release_path()

    with(env.cd(release_path)):
        env.run("curl -sS https://getcomposer.org/installer | php")


@task
def update():
    release_path = paths.get_current_release_path()

    with(env.cd(release_path)):
        env.run("php composer.phar install")

