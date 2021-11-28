The app is developed on WSL. It has been tested on WSL (Ubuntu-20.04) and macOS (Catalina-10.15.7).

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
A list of test tickets will be imported. The ticket file can be found at <code>tests/data/tickets.json</code>.

Then, go to this link: 
<http://localhost:8000/accounts/login/>

# To clean preloaded tickets:
```
./bin/zticketviewerRESET
```

# To run tests:
First clean existing tickets (command above), then:
```
pytest
```
It takes less than 1 minute to finish the tests. The tests send requests to Zendesk API endpoints with limited access rates. Please don't run another round of tests within 30 seconds.


