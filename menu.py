import commands
from validators import (option_choice_is_valid, passwords_match,
                        user_is_authenticated, get_user_input, find_id)


class Option:
    def __init__(self, name, command, prep_call=None,
                 prep_call_required=False):
        self.name = name
        self.command = command
        self.prep_call = prep_call
        self.prep_call_required = prep_call_required

    def choose(self):
        """

        """
        data = self.prep_call() if self.prep_call else None
        if self.prep_call_required and data is None:
            print("Wrong data provided")
        else:
            print(self.command.execute(data)
                  if data else self.command.execute())

    def __str__(self):
        return self.name


class Prompter:

    def get_option_choice(self, options):
        choice = input("Choose an option:")
        while not option_choice_is_valid(choice, options):
            print("Wrong choice")
            choice = input("Choose an option:")
        return options[choice.upper()]

    def get_new_password_data(self):
        name = get_user_input("Name")
        login = get_user_input("Login")
        while True:
            password = get_user_input("Password")
            if passwords_match(password):
                return {
                    "name": name,
                    "login": login,
                    "password": password
                }
            else:
                print("Passwords do not match!")

    def get_retrieve_data(self):
        name = get_user_input("Name")
        return {"name": name}

    def get_update_data(self):
        name = get_user_input("Name")
        obj_id = find_id(name)
        update_data = {"id": obj_id, }
        if obj_id is None:
            print("No such data found")
            return None
        elif user_is_authenticated():
            want_new_name = input(
                f"Do you want to update the name too (type yes if so)?"
            )
            if want_new_name.lower() == "yes":
                update_data["name"] = get_user_input("Name")

            want_new_login = input(
                f"Do you want to update the login too (type yes if so)?"
            )
            if want_new_login.lower() == "yes":
                update_data["login"] = get_user_input("Login")

            while True:
                password = get_user_input("Password")
                if passwords_match(password):
                    update_data["password"] = password
                    return update_data

    def get_delete_data(self):
        name = get_user_input("Name")
        obj_id = find_id(name)
        if obj_id is not None and user_is_authenticated():
            return obj_id


class Menu:
    def __init__(self, options):
        self.options = options

    def print_options(self):
        for shortcut, option in self.options.items():
            print(f"({shortcut}) {option}")
            print()







