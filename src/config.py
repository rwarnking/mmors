from pathlib import Path
import logging

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.StreamHandler())
_logger.setLevel(logging.DEBUG)

OUT_DIR = Path.cwd() / "out"
