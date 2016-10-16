# -*- coding: utf-8 -*-

"""
fabrik.ext.composer
-------------------------
Contains methods for syncing composer packages

Params:
    env.composer_flags: Custom composer build flags (Optional)
"""

from fabric.decorators import task
from fabric.state import env

from fabrik import paths


default_flags = (
        '--no-ansi',
        '--no-dev',
        '--no-interaction',
        '--no-progress',
        '--no-scripts',
        '--optimize-autoloader'
    )

@task
def install(install_path=None):
    if not install_path:
        install_path = paths.get_source_path(env.current_release)

    with(env.cd(install_path)):
        env.run("curl -sS https://getcomposer.org/installer | php")


@task
def update(install_path=None):
    if not install_path:
        install_path = paths.get_source_path(env.current_release)

    flags = default_flags

    if "composer_flags" in env:
        flags = env.composer_flags

    with(env.cd(install_path)):
        env.run("php composer.phar install {}".format(" ".join(flags)))
