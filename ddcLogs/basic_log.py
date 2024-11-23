# -*- encoding: utf-8 -*-
import logging
import time
from .log_utils import get_format, get_level
from .settings import LogSettings


class BasicLog:
    def __init__(
        self,
        level: str = None,
        name: str =  None,
        encoding: str = None,
        datefmt: str = None,
        utc: bool = None,
        show_location: bool = None,
    ):
        _settings = LogSettings()
        self.level = get_level(_settings.level if not level else level)
        self.name = _settings.name if not name else name
        self.encoding = _settings.encoding if not encoding else encoding
        self.datefmt = _settings.date_format if not datefmt else datefmt
        self.utc = _settings.utc if not utc else utc
        self.show_location = _settings.show_location if not show_location else show_location

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
