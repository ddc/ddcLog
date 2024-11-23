# -*- encoding: utf-8 -*-
import logging.handlers
import os
from .log_utils import (
    check_directory_permissions,
    check_filename_instance,
    get_level,
    get_log_path,
    get_logger_and_formatter,
    gzip_file,
    remove_old_logs
)


class TimedRotatingLog:
    """
    Current 'when' events supported:
        midnight - roll over at midnight
        W{0-6} - roll over on a certain day; 0 - Monday
    """

    def __init__(
        self,
        level: str = "info",
        directory: str = "logs",
        filenames: list | tuple = None,
        encoding: str = "UTF-8",
        datefmt: str = "%Y-%m-%dT%H:%M:%S",
        sufix: str =  "%Y%m%d",
        days_to_keep: int = 30,
        when: str = "midnight",
        name: str = None,
        utc: bool = True,
        stream_handler: bool = True,
        show_location: bool = False,
    ):
        self.level = get_level(level)
        self.directory = directory
        self.name = "app" if not name else name
        self.filenames = (f"{self.name}.log",) if not filenames else filenames
        self.encoding = encoding
        self.datefmt = datefmt
        self.sufix = sufix
        self.days_to_keep = days_to_keep
        self.when = when
        self.utc = utc
        self.stream_handler = stream_handler
        self.show_location = show_location

    def init(self):
        check_filename_instance(self.filenames)
        check_directory_permissions(self.directory)

        logger, formatter = get_logger_and_formatter(self.name,
                                                     self.datefmt,
                                                     self.show_location,
                                                     self.utc)
        logger.setLevel(self.level)

        for file in self.filenames:
            log_file_path = get_log_path(self.directory, file)

            file_handler = logging.handlers.TimedRotatingFileHandler(
                filename=log_file_path,
                encoding=self.encoding,
                when=self.when,
                utc=self.utc,
                backupCount=self.days_to_keep
            )
            file_handler.suffix = self.sufix
            file_handler.rotator = GZipRotatorTimed(
                self.directory,
                self.days_to_keep
            )
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
