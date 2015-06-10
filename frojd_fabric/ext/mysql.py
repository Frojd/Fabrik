# -*- coding: utf-8 -*-

"""
frojd_fabric.ext.mysql
----------------------
Mysql extension that handles backup and restore (future).

Params:
    env.mysql_user
    env.mysql_password
    env.mysql_db
"""

from fabric.decorators import task
from fabric.state import env
from frojd_fabric import paths


@task
def backup_db(limit=5):
    current_release = paths.get_current_release_name()

    max_versions = limit+1

    if not current_release:
        return

    env.run("mkdir -p %s" % paths.get_backup_path("mysql"))

    backup_file = "mysql/%s.sql.gz" % current_release
    backup_path = paths.get_backup_path(backup_file)

    env.run("mysqldump -u %s -p%s %s | gzip -c > %s" %
            (env.mysql_user, env.mysql_password, env.mysql_db, backup_path))

    # Remove older releases
    env.run("ls -dt %s/* | tail -n +%s | xargs rm -rf" % (
        paths.get_backup_path("mysql"),
        max_versions)
    )

