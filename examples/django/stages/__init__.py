from fabric.state import env
# Include all your stage environments here
from demo import demo
from local import local
from stage import stage

from fabrik.transfer.git import copy


# Put settings used by all env stages
env.repro_url = "git@github.com:Frojd/Yourrepro.git"
