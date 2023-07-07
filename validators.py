import logging
from getpass import getpass
import commands
from database_manager import PASSWORD


def option_choice_is_valid(choice, options):
    return choice in options or choice.upper() in options


def get_user_input(label, required=True):
    value = (input(f'{label}: ') if 'password' not in label.lower()
             else getpass(f'{label}: '))
    while required and not value:
        value = input(f'{label}: ') or None
    return value


def passwords_match(password):
    pass_confirm = get_user_input('Confirm password')
    return password == pass_confirm


def user_is_authenticated():
    password = get_user_input("Enter User's password")
    return password == PASSWORD


def find_id(name):
    db_row = commands.ListAllPasswordsWhereCommand().execute(name=name)
    try:
        return db_row[0][0]
    except IndexError as e:
        logging.error(e)