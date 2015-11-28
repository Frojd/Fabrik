# -*- coding: utf-8 -*-

"""
fabrik.ext.composer
-------------------------
Contains methods for syncing composer packages
"""

from fabric.decorators import task
from fabric.state import env
from fabrik import paths


@task
def install(install_path=None):
    if not install_path:
        install_path = paths.get_current_release_path()

    with(env.cd(install_path)):
        env.run("curl -sS https://getcomposer.org/installer | php")


@task
def update(install_path=None):
    if not install_path:
        install_path = paths.get_current_release_path()

    with(env.cd(install_path)):
        env.run("php composer.phar install --no-scripts --optimize-autoloader")
