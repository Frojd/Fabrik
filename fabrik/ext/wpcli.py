# -*- coding: utf-8 -*-

"""
fabrik.ext.wpcli
------------------
A wp-cli extension that contains the following tasks:

Params:
    local_wp_dir

Commands:
    sync_remote_to_local
"""

import time
from fabric.decorators import task
from fabric.api import get
from fabric.context_managers import lcd
from fabric.state import env
from fabric.operations import prompt

from fabrik import paths
from fabrik.logger import logger
from fabrik.api import init_tasks
from fabrik.utils.elocal import elocal


@task
def sync_remote_to_local(force="no"):
    """
    Replace your remote db with your local

    Example:
        sync_remote_to_local:force=yes
    """

    assert "local_wp_dir" in env, "Missing local_wp_dir in env"

    if force != "yes":
        message = "This will replace your local database with your "\
            "remote, are you sure [y/n]"
        answer = prompt(message, "y")

        if answer != "y":
            logger.info("Sync stopped")
            return

    init_tasks()  # Bootstrap fabrik

    remote_file = "sync_%s.sql" % int(time.time()*1000)
    remote_path = "/tmp/%s" % remote_file

    with env.cd(paths.get_current_path()):
        env.run("wp db export %s" % remote_path)

    local_wp_dir = env.local_wp_dir
    local_path = "/tmp/%s" % remote_file

    # Download sync file
    get(remote_path, local_path)

    with lcd(local_wp_dir):
        elocal("wp db import %s" % local_path)

    # Cleanup
    env.run("rm %s" % remote_path)
    elocal("rm %s" % local_path)
