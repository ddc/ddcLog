# -*- encoding: utf-8 -*-
import logging
from .log_utils import get_level


class BasicLog:
    def __init__(
        self,
        level: str = "info",
        datefmt: str = "%Y-%m-%dT%H:%M:%S",
        encoding: str = "UTF-8"
    ):
        self.level = get_level(level)
        self.datefmt = datefmt
        self.encoding = encoding

    def init(self):
        _debug_formatt = ""
        if self.level == logging.DEBUG:
            _debug_formatt = "[%(filename)s:%(funcName)s:%(lineno)d]:"

        formatt = f"[%(asctime)s.%(msecs)03d]:[%(levelname)s]:[NTL]:{_debug_formatt}%(message)s"
        logging.basicConfig(level=self.level, datefmt=self.datefmt, encoding=self.encoding, format=formatt)
        logger = logging.getLogger(__name__)
        return logger
