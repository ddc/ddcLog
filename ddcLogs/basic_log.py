# -*- encoding: utf-8 -*-
import logging
import time
from typing import Optional
from .log_utils import get_format, get_level
from .settings import LogSettings


class BasicLog:
    def __init__(
        self,
        level: Optional[str] = None,
        name: Optional[str] =  None,
        encoding: Optional[str] = None,
        datefmt: Optional[str] = None,
        utc: Optional[bool] = None,
        show_location: Optional[bool] = None,
    ):
        _settings = LogSettings()
        self.level = get_level(level or _settings.level)
        self.name = name or _settings.name
        self.encoding = encoding or _settings.encoding
        self.datefmt = datefmt or _settings.date_format
        self.utc = utc or _settings.utc
        self.show_location = show_location or _settings.show_location

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
