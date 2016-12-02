import click

from fabrik.cli import generator
from fabrik.cli import utils


@click.command()
@click.option("--stages", default="stage,prod")
@click.option("--path", default="./")
@click.option("--recipe", default=False)
def main(stages, path, recipe):
    stage_list = stages.split(u",")
    stage_list = map(unicode.strip, stage_list)
    stage_list = filter(None, stage_list)

    formatted_stages = []

    config = {}
    params = {}

    for stage in stage_list:
        formatted_stages.append({
            "NAME": stage,
            "LOCAL": stage == "local"
        })

    if utils.has_git_repro(path):
        repro_url = utils.get_git_remote(path)
        repro_url = click.prompt("git repository", default=repro_url)

        config["git"] = True
        params["repro_url"] = repro_url

    if recipe:
        for stage in formatted_stages:
            stage["RECIPE"] = recipe

    gen = generator.Generator(stages=formatted_stages, path=path,
                              config=config, params=params)
    gen.create_index()
    gen.create_stages()
