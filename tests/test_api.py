# -*- coding: utf-8 -*-

import unittest
import os.path
import shutil
from fabric.state import env
from fabric.context_managers import lcd
from fabric.api import settings
from frojd_fabric import paths
from frojd_fabric.api import setup, deploy, rollback
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

    def test_deploy_rollback(self):
        hooks.register_hook("copy", git.copy)

        with settings(
                branch="develop",
                repro_url="git@github.com:Frojd/Frojd-Django-Boilerplate.git",
                source_path="django_boilerplate",
                warn_only=True):

            setup()
            deploy()

            release_name = paths.get_current_release_name()

            deploy()  # Run another callback so we can can roll back
            rollback()

            self.assertTrue(os.path.exists(os.path.join(
                env.app_path, "current", "manage.py")
            ))

            releases = len(os.listdir(os.path.join(env.app_path, "releases")))
            self.assertEquals(releases, 1)

            self.assertTrue(env.exists(paths.get_releases_path(release_name)))


class TestDeployGit(unittest.TestCase):
    # TODO: Change git repro url into something connected to the project.

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
