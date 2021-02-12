# dockerapi

This is a project to operate docker engine using ``Docker SDK for Python``

run the following package before start the project:
```shell
pip install docker
```

```shell
pip install Flask
```

```shell
pip install flask-cors
```

shell file run.sh

```shell
#!/bin/bash

nohup python3 main.py >log.log 2>&1 &
```

start the app in background, and output the log to file log.log, `2>&1` redirect all stdout and error to log.log file.
