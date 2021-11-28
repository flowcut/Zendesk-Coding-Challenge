The app is developed on WSL.

# To install app:
First clone the git repository.
## To create python virtual environment:
```
python3 -m venv env
```
## To activate python virtual environment:
```
source env/bin/activate
```
## To install app dependency:
```
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install -e .
```
# To start app:
```
./bin/zticketviewerRUN
```
A list of test tickets will be imported.

# To clean preloaded tickets:
```
./bin/zticketviewerRESET
```
# To run tests:
First clean existing tickets (command above), then:
```
pytest
```


