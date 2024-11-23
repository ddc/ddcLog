# -*- encoding: utf-8 -*-
import logging
import time
from .log_utils import get_format, get_level


class BasicLog:
    def __init__(
        self,
        level: str = "info",
        datefmt: str = "%Y-%m-%dT%H:%M:%S",
        encoding: str = "UTF-8",
        name: str = None,
        utc: bool = True,
        show_location: bool = False,
    ):
        self.level = get_level(level)
        self.datefmt = datefmt
        self.encoding = encoding
        self.name = "app" if not name else name
        self.utc = utc
        self.show_location = show_location

    def init(self):
        if self.utc:
            logging.Formatter.converter = time.gmtime

        formatt = get_format(self.show_location, self.name)
        logging.basicConfig(level=self.level,
                            datefmt=self.datefmt,
                            encoding=self.encoding,
                            format=formatt)
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)
        return logger
