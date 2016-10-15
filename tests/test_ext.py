import os.path
import unittest
from fabrik.utils.elocal import elocal
from fabric.state import env
from fabrik.ext import composer
from fabric.context_managers import lcd


def run_capture(command):
    """Helper for retriving env.run issued commands"""
    run_capture.out = getattr(run_capture, "out", [])
    run_capture.out.append(command)




class TestComposerFlags(unittest.TestCase):
    def setUp(self):
        # Reset run capture

        # Run in local mode
        env.run = run_capture
        env.cd = lcd
        env.exists = os.path.exists

        run_capture.out = []

    def test_cookie(self):
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
            self.assertIn(flag, run_capture.out[-1])
