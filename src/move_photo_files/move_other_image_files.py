#!/usr/bin/env python3
"""Move other image files.

This script is organize and move image files into folders.

1. List image files (jpeg,png,gif)
2. Get the file update date
3. Create a subdirectory from the date of shooting
     (current)/2019/2019-nodate/
4. Move file (make it without subdirectory)
...repeat
"""
import argparse
import logging.config
import re
import shutil
from datetime import datetime
from logging import getLogger
from pathlib import Path

LOGGING_CONFIG = {
    'version': 1,
    'disable_exisiting_loggers': True,
    'formatters': {
        'default': {
            'format': '%(asctime)s [%(levelname)-8s]: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default'
        }
    },
    'loggers': {
        '': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': False
        },
        '__main__': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False
        }
    }
}
logging.config.dictConfig(LOGGING_CONFIG)
logger = getLogger(__name__)


def find_image_files(dir: str):
    """Finds image files (.jpg|.jpeg|.png|gif) from specified directory.

    Args:
        dir: Source Directory in photo files.
    Yields:
        Path: Path instance of photo file .
    """
    ext_matcher = re.compile('.*\\.(jpe?g|png|gif)\\Z', re.IGNORECASE)
    for f in (d for d in Path(dir).glob('**/*') if (d.match('[!\\.]*/*') and ext_matcher.match(d.name))):
        yield f


def move_file(source: Path, dest: Path):
    """Moves source photo file to destination path.

    Args
        source: Source image file path
        dest: Destination directory path
    """
    dest.mkdir(mode=0o777, parents=True, exist_ok=True)
    
    try:
        #shutil.copy2(str(source), str(dest))
        #shutil.move(str(source), str(dest))
        logger.debug('move: {} -> {}'.format(source, dest))

    except (shutil.Error) as e:
        logger.warning(repr(e))


def main():
    parser = argparse.ArgumentParser(
        description='Organize and move photo files into folders.')
    parser.add_argument('-o', '--out', default=None,
                        help='destination folder path.(default src_path)', dest='dest_path')
    parser.add_argument('src_path',
                        help='source folder path.')

    args = parser.parse_args()

    source_path = args.src_path
    dest_path_root = Path(args.dest_path or args.src_path)

    try:
        logger.info('start.')
        logger.info('src_path:  {}'.format(source_path))
        logger.info('dest_path: {}'.format(dest_path_root))

        for path in find_image_files(source_path):
            update_time = datetime.fromtimestamp(path.stat().st_mtime)
            dest_path = dest_path_root / update_time.strftime('%Y/%Y-nodate')

            if isinstance(dest_path, Path):
                move_file(path, dest_path)

        logger.info('end.')

    except Exception:
        logger.exception('Unhandled.')


if __name__ == '__main__':
    main()
