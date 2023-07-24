import logging
from logging.handlers import RotatingFileHandler

from constants import LOG_FILE

LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'


def configure_logging():
    rotating_handler = RotatingFileHandler(
        LOG_FILE,
        encoding='utf-8',
        maxBytes=10 ** 6,
        backupCount=5
    )
    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )
