# -*- coding: utf-8 -*-

"""
fabrik.transfer.git
-------------------------
Sets up a standard git clone procedure.

Params:
    env.git_passphrase: Remote server git ssh passphrase (Optional)
"""

from fabric.state import env
from fabric.context_managers import settings

from fabrik.hooks import hook
from ..logger import logger


@hook("copy")
def copy():
    branch = None

    if "repro_url" not in env:
        logger.warn("repro_url is missing in configuration")

    if "branch" in env:
        branch = env.branch
    else:
        logger.warn("Git branch not set, using master instead")
        branch = "master"

    with apply_settings(), env.cd(env.app_path):
        env.run("git clone  --depth 1 -b %(branch)s %(repro)s %(path)s" % {
            "branch": branch,
            "repro": env.repro_url,
            "path": env.current_release
        })


def apply_settings():
    """
    Applies additional settings before clone takes place"
    """

    prompts = {}

    if "git_passphrase" in env:
        prompts["': "] = env.git_passphrase

    return settings(prompts=prompts)
