# Few Utility Functions

[![License](https://img.shields.io/github/license/ddc/ddcLogs.svg?style=plastic)](https://github.com/ddc/ddcLogs/blob/master/LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=plastic)](https://www.python.org)
[![PyPi](https://img.shields.io/pypi/v/ddcLogs.svg?style=plastic)](https://pypi.python.org/pypi/ddcLogs)
[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A//actions-badge.atrox.dev/ddc/ddcLogs/badge?ref=main&style=plastic&label=build&logo=none)](https://actions-badge.atrox.dev/ddc/ddcLogs/goto?ref=main)


# Install
```shell
pip install ddcLogs
```


# BasicLog
+ Setup Logging
```python
from ddcLogs import BasicLog
log = BasicLog(
    level = "info",
    datefmt = "%Y-%m-%dT%H:%M:%S",
    encoding = "UTF-8",
    name = "app"
)
log.init()
```


# SizeRotatingLog
+ Setup Logging
    + Logs will rotate based on the file size
```python
from ddcLogs import SizeRotatingLog
log = SizeRotatingLog(
    level = "info",
    directory = "logs",
    filename = "app.log",
    encoding = "UTF-8",
    datefmt = "%Y-%m-%dT%H:%M:%S",
    days_to_keep = 7,
    max_mbytes = 5,
    name = "app"
)
log.init()
```


# TimedRotatingLog
+ Setup Logging
    + Logs will rotate based on `when` variable to a `.tar.gz` file, defaults to `midnight`
    + Logs will be deleted based on the `days_to_keep` variable, defaults to 7
    + Current 'when' events supported:
        + S - Seconds
        + M - Minutes
        + H - Hours
        + D - Days
        + midnight - roll over at midnight
        + W{0-6} - roll over on a certain day; 0 - Monday
```python
from ddcLogs import TimedRotatingLog
log = TimedRotatingLog(
    level = "info",
    directory = "logs",
    filename = "app.log",
    encoding = "UTF-8",
    datefmt = "%Y-%m-%dT%H:%M:%S",
    days_to_keep = 7,
    when = "midnight",
    utc = True,
    name = "app"
)
log.init()
```


# Source Code
### Build
```shell
poetry build
```

### Publish to test pypi
```shell
poetry publish -r test-pypi
```

### Publish to pypi
```shell
poetry publish
```


### Run Tests
```shell
poetry run coverage run -m pytest -v
```


### Get Coverage Report
```shell
poetry run coverage report
```


# License
Released under the [MIT License](LICENSE)
