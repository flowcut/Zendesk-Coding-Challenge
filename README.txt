$ sudo apt-get update
$ sudo apt-get install python3 python3-pip python3-venv python3-wheel python3-setuptools


$ source env/bin/activate
$ which pip
$ pip install -r requirements.txt
$ pip install -e .

$ export FLASK_ENV=development
$ export FLASK_APP=zticketviewer
$ flask run --host 0.0.0.0 --port 8000

subject
status, priority, type
description
