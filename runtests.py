# -*- coding: utf-8 -*-

import unittest
import sys
from fabric.state import env
from fabric.state import output


test_suite = [
    "tests.test_api",
    "tests.test_ext",
    "tests.test_recipes",
    "tests.test_cli",
]


def prepare_test():
    import logging
    from fabrik.logger import logger

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

    # Disable fabrik logging
    logger.setLevel(logging.CRITICAL)


def runtests(test_modules=None):
    prepare_test()

    # List of modules to test
    if (not test_modules):
        test_modules = test_suite

    # Construct and run test suite
    suite = unittest.TestSuite()

    for t in test_modules:
        try:
            mod = __import__(t, globals(), locals(), ["suite"])
            suitefn = getattr(mod, "suite")
            suite.addTest(suitefn())
        except (ImportError, AttributeError):
            suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())


if __name__ == "__main__":
    test_modules = None

    if len(sys.argv) > 1:
        test_modules = [sys.argv[1]]

    runtests(test_modules)
