# -*- encoding: utf-8 -*-
import os
import tempfile
from datetime import datetime
from ddcLogs import SizeRotatingLog, TimedRotatingLog
from ddcLogs.log_utils import delete_file


class TestLogs:
    @classmethod
    def setup_class(cls):
        cls.level = "debug"
        cls.directory = tempfile.gettempdir()
        cls.filenames = ("test1.log", "test2.log")

    @classmethod
    def teardown_class(cls):
        for filename in cls.filenames:
            file_path = str(os.path.join(cls.directory, filename))
            if os.path.isfile(file_path):
                delete_file(file_path)

    def test_timed_rotating_log(self):
        year = 2020
        month = 10
        day = 10

        log = TimedRotatingLog(directory=self.directory, level=self.level, filenames=self.filenames).init()
        log.debug("start")

        # change files datetime
        epoch_times = datetime(year, month, day, 1, 1, 1).timestamp()
        for filename in self.filenames:
            file_path = str(os.path.join(self.directory, filename))
            os.utime(file_path, (epoch_times, epoch_times))

        log = TimedRotatingLog(directory=self.directory, level=self.level, filenames=self.filenames).init()
        log.debug("end")

        # delete test.gz files
        for filename in self.filenames:
            gz_file_name = f"{os.path.splitext(filename)[0]}_{year}{month}{day}.log.gz"
            gz_file_path = os.path.join(tempfile.gettempdir(), gz_file_name)
            assert os.path.exists(gz_file_path)
            delete_file(str(gz_file_path))

    def test_size_rotating_log(self):
        # creating files with 2MB
        for filename in self.filenames:
            file_path = str(os.path.join(self.directory, filename))
            with open(file_path, "wb") as f:
                f.seek((2 * 1024 * 1024) - 1)
                f.write(b"\0")

        max_mbytes = 1
        log = SizeRotatingLog(directory=self.directory,
                              level=self.level,
                              filenames=self.filenames,
                              max_mbytes=max_mbytes).init()

        log.debug("test")

        # delete test.gz files
        for filename in self.filenames:
            gz_file_name = f"{os.path.splitext(filename)[0]}_1.log.gz"
            gz_file_path = os.path.join(tempfile.gettempdir(), gz_file_name)
            assert os.path.isfile(gz_file_path)
            delete_file(gz_file_path)
