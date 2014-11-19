from fabric.decorators import task
from fabric.state import env
from fabric.context_managers import cd, prefix
from frojd_fabric.hooks import hook, run_hook

@task
@hook("copy")
def copy():
    with(cd(env.app_path)):
        env.run("git clone  -b %(branch)s %(repro)s %(path)s" % {
            "branch": env.branch,
            "repro": env.repro_url,
            "path": env.current_release
        })
