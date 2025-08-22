## Introduction
This web app provide a dashboard for the Lego city's traffic light system to both monitoring the coil states and also allowed to switch between the rush mode and unrush mode (default is unrush).


## Quick Setup
1. Clone this project
2. Install pipenv for quick setup (no need to install in Global, can be inside your virtual env)
```terminal
pip install pipenv
pipenv install  # install dependency from the requirement list of Pipenv file
pipenv shell    # activate the env
```

## OpenPLC 
### Coil Mapping
Raspberry Pi to OpenPLC mapping: (see default mapping of raspberry to openplc to know exact pin to put)
- N: `%QX0.0-0.2` (RAG) (Red: 0.0, Amber:0.1, Green: 0.2)
- EW: `%QX0.3-0.5`(RAG)
- S: `%QX0.6-0.7` `%QX1.0`(RAG)

The above mapping in pymodbus API:
```python
SIGNAL_MAP = {
    0: 'N_red', 1: 'N_orange', 2: 'N_green',
    3: 'EW_red', 4: 'EW_orange', 5: 'EW_green',
    6: 'S_red', 7: 'S_orange', 8: 'S_green'
}
```
## Access management
1. Write: only privilege as high as or higher than an engineer can write
2. Read: anyone logined with an account can see the dashboard display

## DB management
### Spec
- sqlite3
- in-program API: SQL language query
- Table content for each user
    - id
    - role
    - username
### Operation
1. Create: there will always be a default user with username/password being admin/admin. Only the admin can create users. (now create by hard coding)
2. Delete: only admin can delete users.

Q: How does real world system's DB being managed?
> For now just create a DB that supports at least 3 users: Admin(with highest privilege), engineer(with lower privilege).