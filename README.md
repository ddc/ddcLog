# Log Functions

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
     + This is just a basic log, it does not use any file
```python
from ddcLogs import BasicLog
logger = BasicLog(
    level="info",
    name = "app",
    utc = True,
    show_location = False, # This will show the filename and the line number where the message originated
).init()
logger.warning("This is a warning example")
```


# SizeRotatingLog
+ Setup Logging
    + Logs will rotate based on the file size
    + Logs will be deleted based on the `days_to_keep` variable, defaults to 30
```python
from ddcLogs import SizeRotatingLog
logger = SizeRotatingLog(
    level = "info",
    directory = "logs",
    filenames = ["app.log", "app1.log"],
    days_to_keep = 7,
    max_mbytes = 5,
    name = "app",
    utc = True,
    stream_handler = True, # Add stream handler along with file handler
    show_location = False # This will show the filename and the line number where the message originated
).init()
logger.warning("This is a warning example")
```


# TimedRotatingLog
+ Setup Logging
    + Logs will rotate based on `when` variable to a `.gz` file, defaults to `midnight`
    + Logs will be deleted based on the `days_to_keep` variable, defaults to 30
    + Current 'when' events supported:
        + midnight - roll over at midnight
        + W{0-6} - roll over on a certain day; 0 - Monday
```python
from ddcLogs import TimedRotatingLog
logger = TimedRotatingLog(
    level = "info",
    directory = "logs",
    filenames = ["app.log", "app1.log"],
    days_to_keep = 7,
    when = "midnight",
    name = "app",
    utc = True,
    stream_handler = True, # Add stream handler along with file handler
    show_location = False # This will show the filename and the line number where the message originated
).init()
logger.warning("This is a warning example")
```

### Example of output
`[2024-10-08T19:08:56.918]:[WARNING]:[app]:This is a warning example`



# Source Code
### Build
```shell
poetry build -f wheel
```


### Publish to test pypi
```shell
poetry publish -r test-pypi
```


### Publish to pypi
```shell
poetry publish
```


### Run Tests and Get Coverage Report
```shell
poetry run coverage run --omit=./tests/* --source=./ddcLogs -m pytest -v && poetry run coverage report
```


# License
Released under the [MIT License](LICENSE)
