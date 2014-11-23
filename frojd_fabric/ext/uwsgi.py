from fabric.state import env


def restart():
    env.run("service uwsgi restart")

def reload():
    env.run("touch %s/%s_uwsgi.ini" % (_get_deploy_path(), env.stage))
