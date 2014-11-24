from fabric.state import env


@task
def restart_gunicorn():
    env.run("service gunicorn restart")
