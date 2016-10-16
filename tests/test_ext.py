import os.path
import unittest
from fabrik.utils.elocal import elocal
from fabric.state import env
from fabrik.ext import composer
from fabric.context_managers import lcd
from helpers import run_capture, cd_capture



class TestComposerFlags(unittest.TestCase):
    def setUp(self):
        # Reset run capture
        self.out = []

        # Run in local mode
        env.run = run_capture(self.out)
        env.cd = cd_capture(self.out)
        env.exists = os.path.exists

        env.composer_flags = composer.default_flags

    def test_default_flags(self):
        composer.update('./')

        flags = (
            '--no-ansi',
            '--no-dev',
            '--no-interaction',
            '--no-progress',
            '--no-scripts',
            '--optimize-autoloader',
        )

        for flag in flags:
            self.assertIn(flag, self.out[-1])

    def test_custom_flags(self):
        flags = (
            '--random',
        )

        env.composer_flags = flags

        composer.update('./')

        for flag in flags:
            self.assertIn(flag, self.out[-1])
