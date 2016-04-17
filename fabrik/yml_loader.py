import os
from os.path import exists as lexists
import sys
import importlib

from jinja2 import Template
import yaml
from fabric.state import env
from fabric.api import run
from fabric.context_managers import cd
from fabric.contrib.files import exists
from fabric.context_managers import lcd
from fabric.utils import abort
from fabric.decorators import task

from utils.elocal import elocal


def _load_config(config_path):
    current_dir = os.getcwd()
    config_file = os.path.join(current_dir, config_path)

    with open(config_file, 'r') as stream:
        config_yaml = stream.read()

    config_yaml = Template(config_yaml).render(**env)
    config = yaml.load(config_yaml)

    return config


def _create_stages(stages):
    for name in stages:
        stage = stages[name]

        if not isinstance(stage, dict):
            abort('"{0}" is not a valid environment/stage'.format(name))

        # stage = _normalize_config(stage)
        module_obj = sys.modules[__name__]
        setattr(module_obj, name, _create_stage(name, stage))


def _create_stage(name, stage_config):
    def stage_wrap(*args, **kwargs):
        recipe_module = stage_config.pop('recipe', None)
        print(recipe_module)
        importlib.import_module(recipe_module)

        for key, value in stage_config.iteritems():
            setattr(env, key, value)

        if not stage_config.get('local', False):
            env.exists = exists
            env.run = run
            env.cd = cd
        else:
            env.exists = lexists
            env.run = elocal
            env.cd = lcd

    stage_wrap.__name__ = name
    return task(stage_wrap)


def _parse_settings(data):
    transfer_module = data.pop('transfer', None)

    # name = task_path.split(".")[-1]
    importlib.import_module(transfer_module)

    if transfer_module:
        pass

    for key, value in data.iteritems():
        env[key] = value

    return data


if __name__ == 'yml_loader':
    # sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from recipes import wordpress
    from api import setup, deploy, rollback, debug

    config_path = 'fabrik.yml'
    config = _load_config(config_path)

    # Manage settings
    settings_data = config.pop('settings', {})
    _parse_settings(settings_data)

    _create_stages(config)
    print(config)
