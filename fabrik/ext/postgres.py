# -*- coding: utf-8 -*-

"""
fabrik.ext.postgresql
----------------------
Postgresql extension.
"""

import time
from fabric.decorators import task
from fabric.state import env
from fabric.api import get, put
from fabric import context_managers

from fabrik.logger import logger
from fabrik import paths
from fabrik.api import init_tasks
from fabrik.utils.elocal import elocal, LocalFailedCommand


def _check_requirements():
    assert "psql_user" in env, "Missing psql_user in env"
    assert "psql_db" in env, "Missing psql_db in env"
    assert "psql_password" in env, "Missing psql_password in env"

    assert "local_psql_user" in env, "Missing local_psql_user in env"
    assert "local_psql_db" in env, "Missing local_psql_db in env"
    assert "local_psql_password" in env, "Missing local_psql_password in env"


@task
def sync_remote_to_local():
    """
    Sync your remote postgres database with local
    """
    _check_requirements()

    init_tasks()  # Bootstrap fabrik

    # Create database dump
    remote_file = "postgresql/sync_%s.sql.tar.gz" % int(time.time()*1000)
    remote_path = paths.get_backup_path(remote_file)

    env.run("mkdir -p %s" % paths.get_backup_path("postgresql"))

    with context_managers.shell_env(PGPASSWORD=env.psql_password):
        env.run("pg_dump -h localhost -Fc -f %s -U %s %s --no-acl --no-owner" % (
            remote_path, env.psql_user, env.psql_db
        ))

    local_path = "/tmp/%s" % remote_file

    # Download sync file
    get(remote_path, local_path)

    # Import sync file by performing the following task (drop, create, import)
    with context_managers.shell_env(PGPASSWORD=env.local_psql_password):
        try:
            elocal('psql -U %s -h localhost -c "drop database %s"' % (
                env.local_psql_user,
                env.local_psql_db)
            )
        except LocalFailedCommand as e:  # NOQA
            logger.info("Database %s was not found, proceeding to import" %
                        env.local_psql_db)

        elocal('psql -U %s -h localhost -c "create database %s"' % (
            env.local_psql_user,
            env.local_psql_db)
        )

        elocal('pg_restore --clean -h localhost -d %s -U %s "%s"' % (
            env.local_psql_db,
            env.local_psql_user,
            local_path)
        )

    # Cleanup
    env.run("rm %s" % remote_path)
    elocal("rm %s" % local_path)
