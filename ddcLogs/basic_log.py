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
        formatt = "[%(asctime)s.%(msecs)03d]:[%(levelname)s]:%(message)s"
        logging.basicConfig(level=logging.INFO, encoding=self.encoding, format=formatt, datefmt=self.datefmt)
        logger = logging.getLogger(__name__)
        return logger
