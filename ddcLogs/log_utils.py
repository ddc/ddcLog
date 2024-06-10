# -*- encoding: utf-8 -*-
import errno
import gzip
import logging.handlers
import os
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path


class RemoveOldLogs:
    def __init__(self, logs_dir: str, days_to_keep: int) -> None:
        files_list = list_files(logs_dir, ends_with=".gz")
        for file in files_list:
            file_path = str(os.path.join(logs_dir, file))
            if is_older_than_x_days(file_path, days_to_keep):
                try:
                    remove(file_path)
                except Exception as e:
                    write_stderr(f"[Unable to remove old logs]:{get_exception(e)}: {file_path}")


def list_files(directory: str, ends_with: str | tuple[str, ...] | list[str] = None) -> tuple:
    """
    List all files in the given directory and returns them in a list sorted by creation time in ascending order
    :param directory:
    :param ends_with:
    :return: tuple
    """

    try:
        result: list = []
        if os.path.isdir(directory):
            result: list = [Path(os.path.join(directory, f)) for f in os.listdir(directory) if
                            f.lower().endswith(tuple(ends_with))]
            result.sort(key=os.path.getctime)
        return tuple(result)
    except Exception as e:
        sys.stderr.write(get_exception(e))
        raise e


def remove(path: str) -> bool:
    """
    Remove the given file and returns True if the file was successfully removed
    :param path:
    :return: True
    """
    try:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.exists(path):
            shutil.rmtree(path)
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
    except OSError as e:
        sys.stderr.write(get_exception(e))
        raise e
    return True


def is_older_than_x_days(path: str, days: int) -> bool:
    """
    Check if a file or directory is older than the specified number of days
    :param path:
    :param days:
    :return:
    """

    if not os.path.exists(path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)

    if int(days) == 1:
        cutoff_time = datetime.today()
    else:
        cutoff_time = datetime.today() - timedelta(days=int(days))

    stats = os.stat(path)
    days_epoch = cutoff_time.timestamp()
    if stats.st_ctime < days_epoch:
        return True
    return False


def get_exception(e) -> str:
    """
    Get exception
    :param e: exception string
    :return: str
    """

    module = e.__class__.__module__
    if module is None or module == str.__class__.__module__:
        module_and_exception = f"[{e.__class__.__name__}]:[{e}]"
    else:
        module_and_exception = f"[{module}.{e.__class__.__name__}]:[{e}]"
    return module_and_exception.replace("\r\n", " ").replace("\n", " ")


def write_stderr(msg: str) -> None:
    """
    Write msg to stderr
    :param msg:
    :return: None
    """

    sys.stdout.write(f"[ERROR]:{msg}\n")


def get_level(level: str) -> logging:
    """
    Get logging level
    :param level:
    :return: level
    """

    if not isinstance(level, str):
        write_stderr("[Unable to get log level]. Default level to: 'info'")
        return logging.INFO
    match level.lower():
        case "debug":
            return logging.DEBUG
        case "warning":
            return logging.WARNING
        case "error":
            return logging.ERROR
        case "critical":
            return logging.CRITICAL
        case _:
            return logging.INFO


def get_log_path(directory: str, filename: str) -> str:
    """
    Get log file path
    :param directory:
    :param filename:
    :return: path as str
    """

    try:
        os.makedirs(directory, exist_ok=True) if not os.path.isdir(directory) else None
    except Exception as e:
        write_stderr(f"[Unable to create logs directory]:{get_exception(e)}: {directory}")
        raise e

    log_file_path = str(os.path.join(directory, filename))

    try:
        open(log_file_path, "a+").close()
    except IOError as e:
        write_stderr(f"[Unable to open log file for writing]:{get_exception(e)}: {log_file_path}")
        raise e

    return log_file_path


def set_log_format(file_hdlr, level: logging) -> logging.Logger:
    """
    Set log format
    :param file_hdlr:
    :param level:
    :return: logger
    """

    _debug_formatt = ""
    if level == logging.DEBUG:
        _debug_formatt = f"[PID:{os.getpid()}]:[%(filename)s:%(funcName)s:%(lineno)d]:"

    formatt = f"[%(asctime)s.%(msecs)03d]:[%(levelname)s]:{_debug_formatt}%(message)s"
    formatter = logging.Formatter(formatt, datefmt="%Y-%m-%dT%H:%M:%S")

    logger = logging.getLogger()
    logger.setLevel(level)

    file_hdlr.setFormatter(formatter)
    file_hdlr.setLevel(level)
    logger.addHandler(file_hdlr)

    stream_hdlr = logging.StreamHandler()
    stream_hdlr.setFormatter(formatter)
    stream_hdlr.setLevel(level)
    logger.addHandler(stream_hdlr)

    return logger


def gzip_file(source, output_partial_name) -> gzip:
    """
    gzip file
    :param source:
    :param output_partial_name:
    :return: gzip
    """

    if os.path.isfile(source) and os.stat(source).st_size > 0:
        try:
            sfname, sext = os.path.splitext(source)
            renamed_dst = f"{sfname}_{output_partial_name}{sext}.gz"
            with open(source, "rb") as fin:
                with gzip.open(renamed_dst, "wb") as fout:
                    fout.writelines(fin)
            remove(source)
        except Exception as e:
            write_stderr(f"[Unable to zip log file]:{get_exception(e)}: {source}")
