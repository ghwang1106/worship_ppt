import logging
import logging.config
from pathlib import Path


def get_logger(name, level):  # WARNING 30, INFO 20, DEBUG 10
  logging.basicConfig(level=level, format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                      datefmt="%Y-%m-%d %H:%M:%S")
  logging.config.dictConfig({'version': 1, 'disable_existing_loggers': True})  # ignore warning from other module
  logger = logging.getLogger(name)

  for hdlr in logger.handlers[:]:  # remove exsiting handlers -> prevents logging twice
    logger.removeHandler(hdlr)

  return logger


logger = get_logger(__name__, 20)

DATA_PATH = Path(__file__).resolve().parent / "data"
