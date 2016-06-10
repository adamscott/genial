"""

"""
import os
import sys
import logging
from logging.handlers import RotatingFileHandler

from appdirs import *

__all__ = ['app_name', 'app_author', 'logging_level', 'debug', 'logger']


def _setup_debug() -> bool:
    return '--debug' in sys.argv


def _setup_logging_level() -> int:
    global debug
    if debug:
        return logging.DEBUG
    else:
        return logging.INFO


def _setup_logger() -> logging.Logger:
    global app_name, app_author, log_name, debug, logging_level
    log_dir = user_log_dir(appname=app_name, appauthor=app_author)
    os.makedirs(log_dir, exist_ok=True)
    log_file = "{}/{}.log".format(log_dir, log_name)
    formatter = logging.Formatter('[%(asctime)s] (%(levelname)s) %(filename)s:%(lineno)d :: %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging_level)
    file_handler = RotatingFileHandler(
        log_file, mode='a', maxBytes=5*1024*1024,
        backupCount=5, encoding=None, delay=0
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging_level)
    prepared_logger = logging.getLogger(app_name)
    prepared_logger.setLevel(logging_level)
    prepared_logger.addHandler(stream_handler)
    prepared_logger.addHandler(file_handler)
    return prepared_logger

app_name = "Génial"
app_author = "Génial"
log_name = "genial"
debug = _setup_debug()
logging_level = _setup_logging_level()
logger = _setup_logger()

