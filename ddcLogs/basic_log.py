# -*- encoding: utf-8 -*-
import logging
from .log_utils import get_level, get_format


class BasicLog:
    def __init__(
        self,
        level: str = "info",
        datefmt: str = "%Y-%m-%dT%H:%M:%S",
        encoding: str = "UTF-8",
        name: str = "UNDEFINED",
    ):
        self.level = get_level(level)
        self.datefmt = datefmt
        self.encoding = encoding
        self.name = name.lower()

    def init(self):
        fmt = get_format(self.level, self.name)
        logging.basicConfig(level=self.level, datefmt=self.datefmt, encoding=self.encoding, format=fmt)
        logger = logging.getLogger()
        return logger
