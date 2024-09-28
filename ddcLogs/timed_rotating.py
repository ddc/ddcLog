# -*- encoding: utf-8 -*-
import os
from logging.handlers import TimedRotatingFileHandler
from .log_utils import (
    remove_old_logs,
    get_level,
    get_log_path,
    set_file_log_format,
    gzip_file,
)


class TimedRotatingLog:
    """
    TimedRotatingLog class

    Current 'when' events supported:
    S - Seconds
    M - Minutes
    H - Hours
    D - Days
    midnight - roll over at midnight
    W{0-6} - roll over on a certain day; 0 - Monday
    """

    def __init__(
        self,
        level: str = "info",
        directory: str = "logs",
        filename: str = "app.log",
        encoding: str = "UTF-8",
        datefmt: str = "%Y-%m-%dT%H:%M:%S",
        days_to_keep: int = 7,
        when: str = "midnight",
        utc: bool = True,
        name: str = "UNDEFINED",
    ):
        self.level = get_level(level)
        self.directory = directory
        self.filename = filename
        self.encoding = encoding
        self.datefmt = datefmt
        self.days_to_keep = days_to_keep
        self.when = when
        self.utc = utc
        self.name = name.lower()

    def init(self):
        log_file_path = get_log_path(self.directory, self.filename)
        file_hdlr = TimedRotatingFileHandler(filename=log_file_path,
                                             encoding=self.encoding,
                                             when=self.when,
                                             utc=self.utc,
                                             backupCount=self.days_to_keep)
        file_hdlr.suffix = "%Y%m%d"
        file_hdlr.rotator = GZipRotatorTimed(self.directory, self.days_to_keep)
        return set_file_log_format(file_hdlr, self.level, self.datefmt, self.name)


class GZipRotatorTimed:
    def __init__(self, dir_logs: str, days_to_keep: int):
        self.dir = dir_logs
        self.days_to_keep = days_to_keep

    def __call__(self, source: str, dest: str) -> None:
        remove_old_logs(self.dir, self.days_to_keep)
        output_dated_name = os.path.splitext(dest)[1].replace(".", "")
        gzip_file(source, output_dated_name)
