# -*- coding: utf-8 -*-

"""
fabrik.ext.postgres
-------------------
A PostgreSQL extension that handles backups and remote/local syncing

Params:
    psql_user
    psql_db
    psql_password

    local_psql_user
    local_psql_db
    local_psql_password

Commands:
    backup_db
    restore_db
    sync_local_to_remote
    sync_remote_to_local
"""

import time

from fabric.decorators import task
from fabric.state import env
from fabric.api import get, put
from fabric import context_managers
from fabric.operations import prompt

from fabrik import paths
from fabrik.logger import logger
from fabrik.api import init_tasks
from fabrik.utils.elocal import elocal
from fabrik.hooks import run_hook, has_hook


def _check_requirements():
    assert "psql_user" in env, "Missing psql_user in env"
    assert "psql_db" in env, "Missing psql_db in env"
    assert "psql_password" in env, "Missing psql_password in env"

    assert "local_psql_user" in env, "Missing local_psql_user in env"
    assert "local_psql_db" in env, "Missing local_psql_db in env"
    assert "local_psql_password" in env, "Missing local_psql_password in env"


@task
def backup_db(release=None, limit=5):
    """
    Backup database and associate it with current release
    """

    assert "psql_user" in env, "Missing psql_user in env"
    assert "psql_db" in env, "Missing psql_db in env"
    assert "psql_password" in env, "Missing psql_password in env"

    if not release:
        release = paths.get_current_release_name()

    max_versions = limit+1

    if not release:
        logger.info("No releases present, skipping task")
        return

    remote_file = "postgresql/%s.sql.tar.gz" % release
    remote_path = paths.get_backup_path(remote_file)

    env.run("mkdir -p %s" % paths.get_backup_path("postgresql"))

    with context_managers.shell_env(PGPASSWORD=env.psql_password):
        env.run("pg_dump -h localhost -Fc -f %s -U %s %s -x -O" % (
            remote_path, env.psql_user, env.psql_db
        ))

    # Remove older releases
    env.run("ls -dt %s/* | tail -n +%s | xargs rm -rf" % (
        paths.get_backup_path("postgresql"),
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

    backup_file = "postgresql/%s.sql.gz" % release
    backup_path = paths.get_backup_path(backup_file)

    if not env.exists(backup_path):
        raise Exception("Backup file %s not found" % backup_path)

    with context_managers.shell_env(PGPASSWORD=env.psql_password):
        env.run("pg_restore --clean -h localhost -d %s -U %s '%s'" % (
            env.psql_db,
            env.psql_user,
            backup_path)
        )


@task
def sync_local_to_remote(force="no"):
    """
    Sync your local postgres database with remote

    Example:
        fabrik prod sync_local_to_remote:force=yes
    """

    _check_requirements()

    if force != "yes":
        message = "This will replace the remote database '%s' with your "\
            "local '%s', are you sure [y/n]" % (env.psql_db, env.local_psql_db)
        answer = prompt(message, "y")

        if answer != "y":
            logger.info("Sync stopped")
            return

    init_tasks()  # Bootstrap fabrik

    # Create database dump
    local_file = "sync_%s.sql.tar.gz" % int(time.time()*1000)
    local_path = "/tmp/%s" % local_file

    with context_managers.shell_env(PGPASSWORD=env.local_psql_password):
        elocal("pg_dump -h localhost -Fc -f %s -U %s %s -x -O" % (
            local_path, env.local_psql_user, env.local_psql_db
        ))

    remote_path = "/tmp/%s" % local_file

    # Upload sync file
    put(remote_path, local_path)

    # Import sync file by performing the following task (drop, create, import)
    with context_managers.shell_env(PGPASSWORD=env.psql_password):
        env.run("pg_restore --clean -h localhost -d %s -U %s '%s'" % (
            env.psql_db,
            env.psql_user,
            remote_path)
        )

    # Cleanup
    env.run("rm %s" % remote_path)
    elocal("rm %s" % local_path)

    # Trigger hook
    run_hook("postgres.after_sync_local_to_remote")

    logger.info("Sync complete")


@task
def sync_remote_to_local(force="no"):
    """
    Sync your remote postgres database with local

    Example:
        fabrik prod sync_remote_to_local
    """

    _check_requirements()

    if force != "yes":
        message = "This will replace your local database '%s' with the "\
            "remote '%s', are you sure [y/n]" % (env.local_psql_db, env.psql_db)
        answer = prompt(message, "y")

        if answer != "y":
            logger.info("Sync stopped")
            return

    init_tasks()  # Bootstrap fabrik

    # Create database dump
    remote_file = "postgresql/sync_%s.sql.tar.gz" % int(time.time()*1000)
    remote_path = paths.get_backup_path(remote_file)

    env.run("mkdir -p %s" % paths.get_backup_path("postgresql"))

    with context_managers.shell_env(PGPASSWORD=env.psql_password):
        env.run("pg_dump -h localhost -Fc -f %s -U %s %s -x -O" % (
            remote_path, env.psql_user, env.psql_db
        ))

    local_path = "/tmp/%s" % remote_file

    # Download sync file
    get(remote_path, local_path)

    # Import sync file by performing the following task (drop, create, import)
    with context_managers.shell_env(PGPASSWORD=env.local_psql_password):
        elocal("pg_restore --clean -h localhost -d %s -U %s '%s'" % (
            env.local_psql_db,
            env.local_psql_user,
            local_path)
        )

    # Cleanup
    env.run("rm %s" % remote_path)
    elocal("rm %s" % local_path)

    # Trigger hook
    run_hook("postgres.after_sync_remote_to_local")

    logger.info("Sync complete")
