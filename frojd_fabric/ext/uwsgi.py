from fabric.state import env


def restart():
    env.run("service uwsgi restart")

def reload():
    env.run("touch %s" % (env.uwsgi_ini_path))

