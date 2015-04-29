# -*- coding: utf-8 -*-

import unittest
import os.path
import shutil
from fabric.state import env
from fabric.context_managers import lcd
from fabric.api import settings
from fabric.state import output
from frojd_fabric.api import setup, deploy
from frojd_fabric.utils.elocal import elocal
from frojd_fabric import hooks
from frojd_fabric.transfer import git


# Deregister git copy hook (so we can assign programmatically)
hooks.unregister_hook("copy", git.copy)

# Run in local mode
env.run = elocal
env.cd = lcd
env.exists = os.path.exists


class TestApi(unittest.TestCase):
    def setUp(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        env.app_path = os.path.join(current_path, "tmp")

    def tearDown(self):
        hooks.unregister_hook("copy", git.copy)

        try:
            shutil.rmtree(env.app_path)
            pass
        except OSError:
            pass

    def test_setup(self):
        setup()

        self.assertTrue(os.path.exists(os.path.join(env.app_path, "shared")))
        self.assertTrue(os.path.exists(os.path.join(env.app_path, "upload")))

    def test_deploy(self):
        with self.assertRaises(Exception) as context:
            deploy()

        self.assertTrue("No copy method has been defined" in context.exception)

    def test_deploy_copy(self):
        hooks.register_hook("copy", git.copy)

        with self.assertRaises(Exception) as context:
            deploy()

        self.assertTrue("You need to run setup before running deploy" in
                        context.exception)

    def test_deploy_setup(self):
        hooks.register_hook("copy", git.copy)

        setup()

        with self.assertRaises(Exception) as context:
            deploy()

        self.assertTrue("Error occurred on copy. Aborting deploy" in
                        context.exception)


class TestDeployGit(unittest.TestCase):
    def setUp(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        env.app_path = os.path.join(current_path, "tmp")

    def tearDown(self):
        hooks.unregister_hook("copy", git.copy)

        try:
            shutil.rmtree(env.app_path)
            pass
        except OSError:
            pass

    def test_deploy_404_repro(self):
        hooks.register_hook("copy", git.copy)

        with settings(
                branch="develop",
                repro_url="git@github.com:Frojd/Frojd-Django-Boilerplate1.git",
                source_path="django_boilerplate",
                warn_only=True):

            setup()

            with self.assertRaises(Exception):
                deploy()

    def test_deploy_repro(self):
        hooks.register_hook("copy", git.copy)

        with settings(
                branch="develop",
                repro_url="git@github.com:Frojd/Frojd-Django-Boilerplate.git",
                source_path="django_boilerplate",
                warn_only=True):

            setup()
            deploy()

            self.assertTrue(os.path.exists(os.path.join(
                env.app_path, "current", "manage.py")
            ))


def runtests():
    import logging
    from frojd_fabric.logger import logger

    # Mute fabric
    output["status"] = False
    output["aborts"] = False
    output["warnings"] = False
    output["running"] = False
    output["stdout"] = False
    output["stderr"] = False
    output["exceptions"] = False
    output["debug"] = False

    # Raise exceptions on errors
    env.raise_errors = True

    # Disable frojd_fabric logging
    logger.setLevel(logging.CRITICAL)

    unittest.main()


if __name__ == "__main__":
    runtests()
