from fabric.state import env


@task
def restart_celery():
    env.run("service celeryd restart")
