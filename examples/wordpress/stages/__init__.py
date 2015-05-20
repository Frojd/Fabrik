from fabric.state import env
from local import local

from frojd_fabric.transfer.git import copy


# Put settings used by all env stages
env.repro_url = "git@github.com:Frojd/Yourrepro.git"
