#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import fabric.main


def main():
    # Supply default fabricrc (if one does not exist)
    """
    if "-c" not in sys.argv:
        rc_files = ("fabrik.env", "fabricrc.txt", ".fabricrc")

        for path in rc_files:
            if os.path.exists(path):
                sys.argv.extend(("-c", path))
                print('Loading vars from {0}'.format(path))
                break
    """

    # root_path = os.path.dirname(os.path.abspath(os.path.join(__file__, '..')))
    # sys.path.append(root_path)

    path = os.path.dirname(os.path.abspath(__file__))
    fabfile_path = os.path.join(path, '../yml_loader.py')
    fabfile_path = os.path.abspath(fabfile_path)

    fabric.main.main([fabfile_path])


if __name__ == '__main__':
    main()
