import logging
from tkinter import Tk
import security
import commands


class Option:
    def __init__(self, name, command, prep_call=None,
                 prep_call_required=False):
        self.name = name
        self.command = command
        self.prep_call = prep_call
        self.prep_call_required = prep_call_required

    def choose(self):
        data = self.prep_call() if self.prep_call else None
        if self.prep_call_required and data is None:
            print("Wrong data provided")
        else:
            message = (self.command.execute(data)
                       if data else self.command.execute())

            print(message)

    def __str__(self):
        return self.name


def print_options(options):
    for shortcut, option in options.items():
        print(f'({shortcut}) {option}')
        print()


def option_choice_is_valid(choice, options):
    return choice in options or choice.upper() in options


def get_option_choice(options):
    choice = input('Choose an option:')
    while not option_choice_is_valid(choice, options):
        print("Wrong choice")
        choice = input('Choose an option:')
    return options[choice.upper()]


def get_user_input(label, required=True):
    value = input(f'{label}: ') or None
    while required and not value:
        value = input(f'{label}: ') or None
    return value


def passwords_match(password):
    pass_confirm = get_user_input('Confirm password')
    return password == pass_confirm


def get_new_password_data():
    name = get_user_input("Name")
    while True:
        password = get_user_input('Password')
        if passwords_match(password):
            return {
                'name': name,
                'password': password
            }
        else:
            print("Passwords do not match!")


def find_id(name):
    db_row = commands.passwords_by.execute(name=name)
    try:
        return db_row[0][0]
    except IndexError as e:
        logging.error(e)


def get_retrieve_data():
    name = get_user_input("Name")
    return {'name': name}


def get_update_data():
    name = get_user_input("Name")
    id = find_id(name)
    if id is None:
        print("No such password found")
        return None
    want_new_name = input(
        f"Do you want to update the name too (press ENTER if not)?"
    )
    if want_new_name:
        name = get_user_input('Name')

    while True:
        password = get_user_input('Password')
        if passwords_match(password):
            return {
                'id': id,
                'name': name,
                'password': password
            }


def get_delete_data():
    name = get_user_input("Name")
    id = find_id(name)
    if id is not None:
        return id
    print("No such password found")


options = {
    'A': Option('Add password', commands.AddPasswordCommand(),
                prep_call=get_new_password_data, prep_call_required=True),
    'B': Option('Select a password', commands.RetrievePasswordCommand(),
                prep_call=get_retrieve_data, prep_call_required=True),
    'C': Option('Update password', commands.UpdatePasswordCommand(),
                prep_call=get_update_data, prep_call_required=True),
    'D': Option('Delete password', commands.DeletePasswordCommand(),
                prep_call=get_delete_data, prep_call_required=True),
    'Q': Option('Quit', commands.QuitCommand())
}
