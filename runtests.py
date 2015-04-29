# -*- coding: utf-8 -*-

import unittest
from fabric.state import env
from fabric.state import output


def runtests():
    import logging
    from frojd_fabric.logger import logger

    # List of modules to test
    testmodules = [
        "tests.test_api"
    ]

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

    # Construct and run test suite
    suite = unittest.TestSuite()

    for t in testmodules:
        try:
            mod = __import__(t, globals(), locals(), ["suite"])
            suitefn = getattr(mod, "suite")
            suite.addTest(suitefn())
        except (ImportError, AttributeError):
            suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

    unittest.TextTestRunner().run(suite)


if __name__ == "__main__":
    runtests()
