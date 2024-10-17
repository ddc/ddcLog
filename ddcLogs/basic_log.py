# -*- encoding: utf-8 -*-
import logging
from .log_utils import get_level, get_format


class BasicLog:
    def __init__(
        self,
        level: str = "info",
        datefmt: str = "%Y-%m-%dT%H:%M:%S",
        encoding: str = "UTF-8",
        name: str = None,
    ):
        self.level = get_level(level)
        self.datefmt = datefmt
        self.encoding = encoding
        self.name = name

    def init(self):
        if not self.name:
            self.name = "app"

        formatt = get_format(self.level, self.name)
        logging.basicConfig(level=self.level, datefmt=self.datefmt, encoding=self.encoding, format=formatt)
        logger = logging.getLogger()
        return logger
