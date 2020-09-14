import logging


def _log_formatter():
    return logging.Formatter('%(module)s - %(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_logger(name: str, level):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(_log_formatter())
    logger.addHandler(ch)
    return logger
