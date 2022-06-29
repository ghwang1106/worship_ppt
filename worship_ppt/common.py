"""
TODO
"""
import logging
import logging.config
from pathlib import Path


def get_logger(name: str,
               level: int) -> logging.Logger:  # WARNING 30, INFO 20, DEBUG 10
  fmt = '%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
  logging.basicConfig(level=level, format=fmt, datefmt='%Y-%m-%d %H:%M:%S')
  logging.config.dictConfig({
      'version': 1,
      'disable_existing_loggers': True
  })  # ignore warning from other module
  logger = logging.getLogger(name)

  # remove existing handlers -> prevents logging twice
  for hdlr in logger.handlers[:]:
    logger.removeHandler(hdlr)

  return logger


logging.getLogger('PIL').setLevel(logging.WARNING)

log = get_logger(__name__, 10)

DATA_PATH = Path(__file__).resolve().parent / 'data'
