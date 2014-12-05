# -*- coding: utf-8 -*-

"""
frojd_fabric.transfer.git
-------------------------
Sets up a standard git clone procedure.
"""

from fabric.state import env
from fabric.context_managers import cd
from frojd_fabric.hooks import hook


@hook("copy")
def copy():
    with(cd(env.app_path)):
        env.run("git clone  --depth 1 -b %(branch)s %(repro)s %(path)s" % {
            "branch": env.branch,
            "repro": env.repro_url,
            "path": env.current_release
        })
