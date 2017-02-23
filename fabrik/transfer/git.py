# -*- coding: utf-8 -*-

"""
fabrik.transfer.git
-------------------------
Sets up a standard git clone procedure.

Params:
    env.git_passphrase: Remote server git ssh passphrase (Optional)
"""
import sys

from fabric.state import env
from fabric.context_managers import settings

from fabrik.hooks import hook
from fabrik.utils import gitext
from ..logger import logger


@hook("copy")
def copy():
    branch = None
    repro_url = None

    if "repro_url" in env:
        repro_url = env.repro_url

    if not repro_url:
        sys.exit("repro_url is missing in configuration")

    if "branch" in env:
        branch = env.branch

    if not branch and gitext.get_reverse_path():
        path = gitext.get_reverse_path()
        branch = gitext.get_git_branch(path)

    if not branch:
        logger.warn("Git branch not set, using master instead")
        branch = "master"

    with apply_settings(), env.cd(env.app_path):
        env.run("git clone  --depth 1 -b %(branch)s %(repro)s %(path)s" % {
            "branch": branch,
            "repro": repro_url,
            "path": env.current_release,
        })


def apply_settings():
    """
    Applies additional settings before clone takes place"
    """

    prompts = {}

    if "git_passphrase" in env:
        prompts["': "] = env.git_passphrase

    return settings(prompts=prompts)
