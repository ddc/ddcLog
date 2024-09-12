# -*- encoding: utf-8 -*-
import os
from logging.handlers import RotatingFileHandler
from .log_utils import (
    RemoveOldLogs,
    get_level,
    get_log_path,
    set_file_log_format,
    gzip_file,
    write_stderr,
    list_files,
    get_exception,
)


class SizeRotatingLog:
    """
    SizeRotatingLog class
    """

    def __init__(
        self,
        level: str = "info",
        directory: str = "logs",
        filename: str = "app.log",
        encoding: str = "UTF-8",
        datefmt: str = "%Y-%m-%dT%H:%M:%S",
        days_to_keep: int = 7,
        max_mbytes: int = 5,
        name: str = "UNDEFINED",
    ):
        self.level = get_level(level)
        self.directory = directory
        self.filename = filename
        self.encoding = encoding
        self.datefmt = datefmt
        self.days_to_keep = days_to_keep
        self.max_mbytes = max_mbytes
        self.name = name.lower()

    def init(self):
        log_file_path = get_log_path(self.directory, self.filename)
        file_hdlr = RotatingFileHandler(filename=log_file_path,
                                        mode="a",
                                        maxBytes=self.max_mbytes * 1024 * 1024,
                                        backupCount=self.days_to_keep,
                                        encoding=self.encoding,
                                        delay=False,
                                        errors=None)
        file_hdlr.rotator = GZipRotatorSize(self.directory, self.days_to_keep)
        return set_file_log_format(file_hdlr, self.level, self.datefmt, self.name)


class GZipRotatorSize:
    def __init__(self, dir_logs: str, days_to_keep: int):
        self.dir = dir_logs
        self.days_to_keep = days_to_keep

    def __call__(self, source: str, dest: str) -> None:
        RemoveOldLogs(self.dir, self.days_to_keep)
        if os.path.isfile(source) and os.stat(source).st_size > 0:
            new_file_number = 1
            old_gz_files_list = list_files(self.dir, ends_with=".gz")
            if old_gz_files_list:
                try:
                    oldest_file_name = old_gz_files_list[-1].name.split(".")[0].split("_")
                    if len(oldest_file_name) > 1:
                        new_file_number = int(oldest_file_name.split("_")[1]) + 1
                except ValueError as e:
                    write_stderr(f"[Unable to get old zip log file number]:{get_exception(e)}: {old_gz_files_list[-1].name}")
            gzip_file(source, new_file_number)
