# -*- encoding: utf-8 -*-
import os
import logging.handlers
from .log_utils import (
    get_exception,
    get_format,
    get_level,
    get_log_path,
    gzip_file,
    remove_old_logs,
    write_stderr
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
        filenames: list | tuple = ("app.log",),
        encoding: str = "UTF-8",
        datefmt: str = "%Y-%m-%dT%H:%M:%S",
        sufix: str =  "%Y%m%d",
        days_to_keep: int = 30,
        when: str = "midnight",
        utc: bool = True,
        name: str = None,
        stream_handler: bool = True,
        show_location: bool = False,
    ):
        self.level = get_level(level)
        self.directory = directory
        self.filenames = filenames
        self.encoding = encoding
        self.datefmt = datefmt
        self.sufix = sufix
        self.days_to_keep = days_to_keep
        self.when = when
        self.utc = utc
        self.name = name
        self.stream_handler = stream_handler
        self.show_location = show_location

    def init(self):
        if not isinstance(self.filenames, list | tuple):
            write_stderr(
                "Unable to parse filenames. "
                "Filenames are not list or tuple. | "
                f"{self.filenames}"
            )
            return

        formatt = get_format(self.show_location, self.name)
        formatter = logging.Formatter(formatt, datefmt=self.datefmt)

        if not self.name:
            self.name = "app"

        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)

        for file in self.filenames:
            try:
                log_file_path = get_log_path(self.directory, file)
            except Exception as e:
                write_stderr(
                    "Unable to create logs. | "
                    f"{self.directory} | "
                    f"{get_exception(e)}"
                )
                return

            file_handler = logging.handlers.TimedRotatingFileHandler(
                filename=log_file_path,
                encoding=self.encoding,
                when=self.when,
                utc=self.utc,
                backupCount=self.days_to_keep
            )
            file_handler.suffix = self.sufix
            file_handler.rotator = GZipRotatorTimed(self.directory, self.days_to_keep)
            file_handler.setFormatter(formatter)
            file_handler.setLevel(self.level)
            logger.addHandler(file_handler)

        if self.stream_handler:
            stream_hdlr = logging.StreamHandler()
            stream_hdlr.setFormatter(formatter)
            stream_hdlr.setLevel(self.level)
            logger.addHandler(stream_hdlr)

        return logger


class GZipRotatorTimed:
    def __init__(self, dir_logs: str, days_to_keep: int):
        self.dir = dir_logs
        self.days_to_keep = days_to_keep

    def __call__(self, source: str, dest: str) -> None:
        remove_old_logs(self.dir, self.days_to_keep)
        output_dated_name = os.path.splitext(dest)[1].replace(".", "")
        gzip_file(source, output_dated_name)
