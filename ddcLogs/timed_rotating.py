# -*- encoding: utf-8 -*-
import logging.handlers
import os
from typing import Optional
from .log_utils import (
    check_directory_permissions,
    check_filename_instance,
    get_level,
    get_log_path,
    get_logger_and_formatter,
    get_stream_handler,
    gzip_file,
    remove_old_logs
)
from .settings import LogSettings


class TimedRotatingLog:
    def __init__(
        self,
        level: Optional[str] = None,
        name: Optional[str] = None,
        directory: Optional[str] = None,
        filenames: Optional[list | tuple] = None,
        encoding: Optional[str] = None,
        datefmt: Optional[str] = None,
        days_to_keep: Optional[int] = None,
        utc: Optional[bool] = None,
        stream_handler: Optional[bool] = None,
        show_location: Optional[bool] = None,
        sufix: Optional[str] =  None,
        when: Optional[str] = None,

    ):
        _settings = LogSettings()
        self.level = get_level(level or _settings.level)
        self.name = name or _settings.name
        self.directory = directory or _settings.directory
        self.filenames = filenames or (_settings.filename,)
        self.encoding = encoding or _settings.encoding
        self.datefmt = datefmt or _settings.date_format
        self.days_to_keep = days_to_keep or _settings.days_to_keep
        self.utc = utc or _settings.utc
        self.stream_handler = stream_handler or _settings.stream_handler
        self.show_location = show_location or _settings.show_location
        self.sufix = sufix or _settings.rotating_file_sufix
        self.when = when or _settings.rotating_when

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
            stream_hdlr = get_stream_handler(self.level, formatter)
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
