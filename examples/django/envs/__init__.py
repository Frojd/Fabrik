from fabric.state import env
from demo import demo
from local import local_django

# Put settings used by all envs here;
env.repro_url = "git@github.com:Frojd/Si-Fundamentet-Admin.git"
