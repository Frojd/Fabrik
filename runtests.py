import unittest
import os.path
import shutil
from fabric.state import env
from fabric.context_managers import lcd
from frojd_fabric.api import setup
from frojd_fabric.utils.elocal import elocal


class TestApi(unittest.TestCase):
    def setUp(self):
        env.run = elocal
        env.cd = lcd
        env.exists = os.path.exists

    def tearDown(self):
        try:
            shutil.rmtree("./tmp/")
        except OSError:
            pass

    def test_setup(self):
        env.app_path = "./tmp/"
        setup()

        self.assertTrue(os.path.exists(os.path.join(env.app_path, "shared")))
        self.assertTrue(os.path.exists(os.path.join(env.app_path, "upload")))


def runtests():
    unittest.main()


if __name__ == "__main__":
    runtests()
