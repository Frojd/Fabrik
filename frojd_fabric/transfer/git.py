# -*- coding: utf-8 -*-

"""
frojd_fabric.transfer.git
-------------------------
Sets up a standard git clone procedure.
"""

from fabric.state import env
from fabric.context_managers import cd
from frojd_fabric.hooks import hook
from ..logger import logger


@hook("copy")
def copy():
    branch = None

    if "branch" in env:
        branch = env.branch
    else:
        logger.warn("Git branch not set, using master instead")
        branch = "master"

    with(cd(env.app_path)):
        env.run("git clone  --depth 1 -b %(branch)s %(repro)s %(path)s" % {
            "branch": branch,
            "repro": env.repro_url,
            "path": env.current_release
        })
