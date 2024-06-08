from pathlib import Path
import logging
import os

DEBUG = True

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.StreamHandler())
# _logger.setLevel(logging.DEBUG)
_logger.setLevel(logging.INFO)

OUT_DIR = Path.cwd() / "out"
DEBUG_DIR = Path.cwd() / "debug"

if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

if not os.path.exists(DEBUG_DIR):
    os.makedirs(DEBUG_DIR)

IGNORE_ADDS = True
