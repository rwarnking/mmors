import calendar
import locale
import logging
import os
from pathlib import Path
from typing import List, Tuple

import dateutil.parser as parser

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

# TODO helper class
# TODO care this might vary between operating systems
locale.setlocale(locale.LC_ALL, "deu_deu")


class LocaleParserInfo(parser.parserinfo):
    WEEKDAYS: List[Tuple[str, ...]] = list(zip(calendar.day_abbr, calendar.day_name))
    MONTHS = list(zip(calendar.month_abbr, calendar.month_name))[1:]


EXPORT_HTML = True
EXPORT_CSV = False
