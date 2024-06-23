#!/usr/bin/env python3
"""Move photo files.

This script is organize and move photo files into folders.

1. List jpeg files
2. Get the shooting date from EXIF
3. Create a subdirectory from the date of shooting
     (current)/2019/2019-05/
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

from PIL import Image
from PIL.ExifTags import TAGS

LOGGING_CONFIG = {
    "version": 1,
    "disable_exisiting_loggers": True,
    "formatters": {"default": {"format": "%(asctime)s [%(levelname)s]: %(message)s"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "level": "DEBUG", "formatter": "default"}},
    "loggers": {
        "": {"level": "WARNING", "handlers": ["console"], "propagate": False},
        "__main__": {"level": "DEBUG", "handlers": ["console"], "propagate": False},
    },
}
logging.config.dictConfig(LOGGING_CONFIG)
logger = getLogger(__name__)


def find_photo_files(dir: str):
    """Finds photo files (.jpg|.jpeg) from specified directory.

    Args:
        dir: Source Directory in photo files.
    Yields:
        Path: Path instance of photo file .
    """
    ext_matcher = re.compile(".*\\.jpe?g\\Z", re.IGNORECASE)
    for f in (d for d in Path(dir).glob("**/*") if (d.match("[!\\.]*/*") and ext_matcher.match(d.name))):
        yield f


def do_operation_image(path: str, func):
    """Do operation wrapper for image instance.

    Args:
        path: Image file path.
        func: Function of operation.
    Returns:
        any: operation result.
    """
    img = Image.open(path)
    result = func(img)
    img.close()
    return result


def get_exif_shooting_date(img: Image):
    """Gets EXIF shooting date from image.

    Args:
        img : Image instance of photo.

    Returns:
        datetime: EXIF shooting date (DateTimeOriginal).
    """
    exif = img._getexif()
    try:
        for id, val in exif.items():
            tg = TAGS.get(id, id)
            if tg == "DateTimeOriginal":
                dt = datetime.strptime(val, "%Y:%m:%d %H:%M:%S")
                return dt

    except (AttributeError, ValueError) as e:
        logger.warning(repr(e))

    return None


def move_file(source: Path, dest: Path):
    """Moves source photo file to destination path.

    Args
        source: Source image file path
        dest: Destination directory path
    """
    dest.mkdir(mode=0o777, parents=True, exist_ok=True)

    try:
        # shutil.copy2(str(source), str(dest))
        # shutil.move(str(source), str(dest))
        logger.debug("move: {} -> {}".format(source, dest))

    except shutil.Error as e:
        logger.warning(repr(e))


def main():
    parser = argparse.ArgumentParser(
        description="Organize and move photo files into folders.")
    parser.add_argument(
        "-o", "--out", default=None, help="destination folder path.(default src_path)", dest="dest_path"
    )
    parser.add_argument("src_path", help="source folder path.")

    args = parser.parse_args()

    source_path = args.src_path
    dest_path_root = Path(args.dest_path or args.src_path)

    try:
        logger.info('"{}" - started.'.format(Path(__file__).name))
        logger.info("src_path:  {}".format(source_path))
        logger.info("dest_path: {}".format(dest_path_root))

        for path in find_photo_files(source_path):
            date_of_shooting = do_operation_image(path, get_exif_shooting_date)
            if not isinstance(date_of_shooting, datetime):
                logger.warning(
                    "can not get the shooting date of EXIF: {}".format(path))
                continue

            dest_path = dest_path_root / date_of_shooting.strftime("%Y/%Y-%m")

            if isinstance(dest_path, Path):
                move_file(path, dest_path)

        logger.info('"{}" - finished.\n'.format(Path(__file__).name))

    except Exception:
        logger.exception("Unhandled.")


if __name__ == "__main__":
    main()
