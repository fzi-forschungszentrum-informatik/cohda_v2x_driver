# -- BEGIN LICENSE BLOCK ----------------------------------------------
# -- END LICENSE BLOCK ------------------------------------------------
#
# ---------------------------------------------------------------------
# !\file
#
# \author  Albert Schotschneider <schotschneider@fzi.de>
# \date    2024-07-03
#
#
# ---------------------------------------------------------------------
# logger_config.py

import logging
import sys
from pathlib import Path
import time
import colorlog


def setup_logger(log_file=None, log_level=logging.INFO):
    """
    Set up a logger with colored console output and optional file output.

    Parameters
    ----------
    log_file : str
        Path to the log file. If None, the logger will not write to a file.
    log_level : int
        Logging level. Default is logging.INFO.

    Returns
    -------
    logging.Logger
    """
    logger = logging.getLogger("project_logger")
    logger.setLevel(log_level)

    # Prevent adding handlers if they already exist
    if not logger.handlers:
        # Create formatters
        console_formatter = colorlog.ColoredFormatter(
            "%(log_color)s[%(asctime)s.%(msecs)06d] [%(levelname)-8s] %(message)s",
            datefmt="%s",
            reset=True,
            log_colors={
                "DEBUG": "cyan",
                # "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bold",
            },
            secondary_log_colors={},
            style="%",
        )

        file_formatter = logging.Formatter(
            "%(log_color)s[%(asctime)s.%(msecs)06d] [%(levelname)-8s] %(message)s", datefmt="%s"
        )

        # Create console handler and set level
        console_handler = colorlog.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # Create file handler and set level (if log_file is provided)
        if log_file:
            file_handler = logging.FileHandler(Path(log_file), encoding="utf-8")
            file_handler.setLevel(log_level)
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

    return logger


logger = setup_logger(log_file=None, log_level=logging.DEBUG)
