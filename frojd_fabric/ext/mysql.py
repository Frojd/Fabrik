# -*- coding: utf-8 -*-

"""
frojd_fabric.ext.mysql
----------------------
Mysql extension that handles backup and restore (future).

Params:
    env.mysql_user
    env.mysql_password
    env.mysql_host
    env.mysql_db
"""

from fabric.decorators import task
from fabric.state import env
from frojd_fabric import paths


@task
def backup_db(release=None, limit=5):
    """
    Backup database and associate it with current release
    """

    if not release:
        release = paths.get_current_release_name()

    max_versions = limit+1

    if not release:
        return

    env.run("mkdir -p %s" % paths.get_backup_path("mysql"))

    backup_file = "mysql/%s.sql.gz" % release
    backup_path = paths.get_backup_path(backup_file)

    env.run("mysqldump -u %s -p%s -h %s %s | gzip -c > %s" %
            (env.mysql_user, env.mysql_password, env.mysql_host, env.mysql_db,
             backup_path))

    # Remove older releases
    env.run("ls -dt %s/* | tail -n +%s | xargs rm -rf" % (
        paths.get_backup_path("mysql"),
        max_versions)
    )


@task
def restore_db(release=None):
    """
    Restores backup back to version, uses current version by default.
    """

    if not release:
        release = paths.get_current_release_name()

    if not release:
        raise Exception("Release %s was not found" % release)

    backup_file = "mysql/%s.sql.gz" % release
    backup_path = paths.get_backup_path(backup_file)

    if not env.exists(backup_path):
        raise Exception("Backup file %s not found" % backup_path)

    env.run("gunzip < %s | mysql -u %s -p%s -h %s %s" %
            (backup_path, env.mysql_user, env.mysql_password, env.mysql_host,
             env.mysql_db))
