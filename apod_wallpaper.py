#!/usr/bin/env python
from pathlib import Path
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y/%d/%m %H:%M:%S', level=logging.ERROR)
log = logging.getLogger(__name__)

from apod_wallpaper.cli import main


if __name__ == '__main__':
    from apod_wallpaper.cli import cli_entry

    raise SystemExit(cli_entry())