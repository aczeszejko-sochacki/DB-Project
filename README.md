# DB Project
A simple API to manage corporation structure.
## Requirements
* Python 3.6.3+
* Pipenv 11.10.2+
* PostgreSQL 9.5.12+
## Setup
Installing dependencies from Pipfile.lock in the app directory: 
```
pipenv install
```
Acitvate virtualenv in the app directory:
```
pipenv shell
```
Run app:
```python
pipenv run python3 main.py --init  # init mode
pipenv run python main.py  # normal mode
```
## Running tests
Each test should be in 'tests/' directory. After running app type name of the test to be execute
