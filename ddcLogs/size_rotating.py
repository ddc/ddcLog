# -*- encoding: utf-8 -*-
import logging.handlers
import os
from dotenv import load_dotenv
from .log_utils import (
    check_directory_permissions,
    check_filename_instance,
    get_exception,
    get_level,
    get_log_path,
    get_logger_and_formatter,
    get_stream_handler,
    gzip_file,
    list_files,
    remove_old_logs,
    write_stderr
)
from .settings import LogSettings


load_dotenv()
settings = LogSettings()


class SizeRotatingLog:
    def __init__(
        self,
        level: str = settings.level,
        name: str = settings.name,
        directory: str = settings.directory,
        filenames: list | tuple = (settings.filename,),
        encoding: str = settings.encoding,
        datefmt: str = settings.date_format,
        days_to_keep: int = int(settings.days_to_keep),
        utc: bool = settings.utc,
        stream_handler: bool = settings.stream_handler,
        show_location: bool = settings.show_location,
        max_mbytes: int = int(settings.max_file_size_mb),
    ):
        self.level = get_level(level)
        self.name = name
        self.directory = directory
        self.filenames = filenames
        self.encoding = encoding
        self.datefmt = datefmt
        self.days_to_keep = days_to_keep
        self.utc = utc
        self.stream_handler = stream_handler
        self.show_location = show_location
        self.max_mbytes = max_mbytes

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
