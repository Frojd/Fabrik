from fabric.decorators import task
from fabric.state import env


@task
def install():
    env.run("npm install")

