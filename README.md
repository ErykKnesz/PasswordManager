# PasswordManager
## About
This is a simple tool whose purpose is to act as a password manager, i.e. store passwords in an encrypted (hashed) form. User with access to the database is able to add, retrieve, update and delete passwords.
It comes both as a GUI and CLI utility.

## Requirements
See the requirements.txt for dependencies. This tool also needs a MySQL database that needs to be installed separately.

## How To
Upon installing MySQL and requirements you run the tool by:
* To run it without GUI, type: `python passman.py`
* To run it with GUI: `python passman.py -g`
* Or: `python passman.py --gui`

![GUI](/Screenshotexample.png?raw=true "Example Screenshot of the app")