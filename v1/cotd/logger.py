import logging


def _log_formatter():
    return logging.Formatter(
        "%(asctime)s|(module:%(module)s - function:%(funcName)s - logger:%(name)s): %(levelname)s - %(message)s"
    )


def get_logger(name: str, level: str, formatter_factory=_log_formatter) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    ch = logging.StreamHandler()

    ch.setLevel(level)
    ch.setFormatter(_log_formatter())

    logger.addHandler(ch)

    return logger
