# -*- encoding: utf-8 -*-
import logging.handlers
import os
from typing import Optional
from .log_utils import (
    check_directory_permissions,
    check_filename_instance,
    get_level, get_log_path,
    get_logger_and_formatter,
    get_stream_handler,
    gzip_file,
    list_files,
    remove_old_logs, write_stderr,
)
from .settings import LogSettings


class SizeRotatingLog:
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
        max_mbytes: Optional[int] = None,

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
        self.max_mbytes = max_mbytes or _settings.max_file_size_mb

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

            file_handler = logging.handlers.RotatingFileHandler(
                filename=log_file_path,
                mode="a",
                maxBytes=self.max_mbytes * 1024 * 1024,
                backupCount=self.days_to_keep,
                encoding=self.encoding,
                delay=False,
                errors=None
            )
            file_handler.rotator = GZipRotatorSize(
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


class GZipRotatorSize:
    def __init__(self, dir_logs: str, days_to_keep: int):
        self.directory = dir_logs
        self.days_to_keep = days_to_keep

    def __call__(self, source: str, dest: str) -> None:
        remove_old_logs(self.directory, self.days_to_keep)
        if os.path.isfile(source) and os.stat(source).st_size > 0:
            source_filename, _ = os.path.basename(source).split(".")
            new_file_number = self._get_new_file_number(self.directory, source_filename)
            if os.path.isfile(source):
                gzip_file(source, new_file_number)


    @staticmethod
    def _get_new_file_number(directory, source_filename):
        new_file_number = 1
        previous_gz_files = list_files(directory, ends_with=".gz")
        for gz_file in previous_gz_files:
            if source_filename in gz_file:
                try:
                    oldest_file_name = gz_file.split(".")[0].split("_")
                    if len(oldest_file_name) > 1:
                        new_file_number = int(oldest_file_name[1]) + 1
                except ValueError as e:
                    write_stderr(
                        "Unable to get previous gz log file number | "
                        f"{gz_file} | "
                        f"{repr(e)}"
                    )
                    raise
        return new_file_number
