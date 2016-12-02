import os
import click
import shutil


def callback(ctx, param, value):
    if not value:
        ctx.abort()


@click.command()
@click.option("--path", default="./")
@click.option("--force", is_flag=True, callback=callback,
              expose_value=True, prompt="Do you want to continue?")
def main(path, force):
    os.remove(os.path.join(path, "fabricrc.txt"))
    os.remove(os.path.join(path, "fabfile.py"))

    shutil.rmtree(os.path.join(path, "stages"))
