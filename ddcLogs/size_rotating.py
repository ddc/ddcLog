# -*- encoding: utf-8 -*-
import logging.handlers
import os
from .log_utils import (
    check_directory_permissions,
    check_filename_instance,
    get_exception,
    get_level,
    get_log_path,
    get_logger_and_formatter,
    gzip_file,
    list_files,
    remove_old_logs,
    write_stderr
)


class SizeRotatingLog:
    def __init__(
        self,
        level: str = "info",
        directory: str = "logs",
        filenames: list | tuple = None,
        encoding: str = "UTF-8",
        datefmt: str = "%Y-%m-%dT%H:%M:%S",
        days_to_keep: int = 30,
        max_mbytes: int = 50,
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
        self.days_to_keep = days_to_keep
        self.max_mbytes = max_mbytes
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
            stream_hdlr = logging.StreamHandler()
            stream_hdlr.setFormatter(formatter)
            stream_hdlr.setLevel(self.level)
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
            new_file_number = 1
            previous_gz_files = list_files(self.directory, ends_with=".gz")
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
                            f"{get_exception(e)}"
                        )
                        raise

            if os.path.isfile(source):
                gzip_file(source, new_file_number)
