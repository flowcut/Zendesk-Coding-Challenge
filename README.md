The app is developed on WSL.

# To install app:
First clone the git repository.
## To activate python virtual environment:
```
$ sudo apt-get update
$ sudo apt-get install python3 python3-pip python3-venv python3-wheel python3-setuptools
$ source env/bin/activate
```
## To install app dependency:
```
$ pip install -r requirements.txt
$ pip install -e .
```
# To start app:
```
$ ./bin/zticketviewerRUN
```
A list of test tickets will be imported.

# To clean preloaded tickets:
```
$ ./bin/zticketviewerRESET
```
# To run tests:
First clean existing tickets (command above), then:
```
$ pytest
```


