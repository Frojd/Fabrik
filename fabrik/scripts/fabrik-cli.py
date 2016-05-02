#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import fabric.main


def main():
    # Supply default fabricrc (if one does not exist)
    if "-c" not in sys.argv:
        rc_files = ("fabricrc.txt", ".fabricrc")

        for path in rc_files:
            if os.path.exists(path):
                sys.argv.extend(("-c", path))
                break

    fabric.main.main()
