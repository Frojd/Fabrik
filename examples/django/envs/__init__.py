from fabric.state import env
from demo import demo
from local import local
from stage import stage


# Put settings used by all env stages
env.repro_url = "git@github.com:Frojd/Yourrepro.git"

