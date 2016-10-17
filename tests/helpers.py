import os.path

from fabric.state import env


def run_capture(out = []):
    """Helper for retriving env.run issued commands"""
    return lambda command, *args, **kwargs: out.append(command.strip())


class CdPlaceholder(object):
    def __enter__(self, *args, **kwargs):
        return True
    def __exit__(self, type, value, traceback):
        return False


def cd_capture(out = []):
    def cd(command):
        command = command.strip()
        out.append('cd {}'.format(command))
        return CdPlaceholder()

    return cd


def empty_copy():
    """
    A stub copy method that does nothing more then create a .txt file.
    """

    source_path = os.path.join(env.current_release, "src")

    env.run("mkdir -p %s" % source_path)
    env.run("touch %s/app.txt" % source_path)
