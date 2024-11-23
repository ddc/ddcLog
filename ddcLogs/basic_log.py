# -*- encoding: utf-8 -*-
import logging
import time
from dotenv import load_dotenv
from .log_utils import get_format, get_level
from .settings import LogSettings


load_dotenv()
settings = LogSettings()


class BasicLog:
    def __init__(
        self,
        level: str = settings.level,
        name: str =  settings.name,
        encoding: str = settings.encoding,
        datefmt: str = settings.date_format,
        utc: bool = settings.utc,
        show_location: bool = settings.show_location,
    ):
        self.level = get_level(level)
        self.name = name
        self.encoding = encoding
        self.datefmt = datefmt
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
