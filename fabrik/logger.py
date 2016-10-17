# -*- coding: utf-8 -*-

"""
fabrik.logger
-------------------
Root logger for library.
"""

import logging
import sys


logger = logging.getLogger(__name__)

out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(
    logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s'))
out_hdlr.setLevel(logging.INFO)

logger.addHandler(out_hdlr)
logger.setLevel(logging.INFO)
