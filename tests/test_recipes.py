# -*- coding: utf-8 -*-

import unittest
import os.path
import shutil

from fabric.state import env
from fabric.api import settings

from fabrik import hooks
from fabrik.api import setup, deploy, rollback
from fabrik.transfer import git
from fabrik.recipes import (
    django as django_recipe,
)
from helpers import run_capture, cd_capture, empty_copy




class TestDjangoRecipe(unittest.TestCase):
    def setUp(self):

        # Reset run capture
        self.out = []

        # Run in local mode
        env.run = run_capture(self.out)
        env.cd = cd_capture(self.out)
        env.exists = lambda x: True
        # env.exists = os.path.exists

        current_path = os.path.dirname(os.path.abspath(__file__))
        env.app_path = os.path.join(current_path, "tmp")
        env.stage = 'stage'
        env.repro_url = "github.com/frojd/random"

        django_recipe.register()

    def tearDown(self):
        hooks.unregister_hook("copy", git.copy)
        hooks.unregister_hook("copy", empty_copy)
        env.venv_path = None

        try:
            shutil.rmtree(env.app_path)
            pass
        except OSError:
            pass

        django_recipe.unregister()

    def test_deploy_flow(self):
        hooks.register_hook("copy", git.copy)

        with settings(source_path="src", warn_only=True):
            deploy()

        self.assertTrue(self.out[-2].endswith('current'))
