from database_manager import db
import commands
from menu import Option

options = {
    'A': Option('Add password', commands.AddPasswordCommand()),
    'B': Option('Select a password', commands.RetrievePasswordCommand()),
    'C': Option('Update password', commands.UpdatePasswordCommand()),
    'D': Option('Delete password', commands.DeletePasswordCommand()),
    'Q': Option('Quit', commands.QuitCommand())
}


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


def get_new_password_data():
    return {
        'name': get_user_input('name'),
        'password': get_user_input('password')
    }

if __name__ == '__main__':
    db.create_database()
    conn = db.create_connection()
    commands.CreatePasswordsTableCommand.execute()
    is_on = True
    while is_on:
        rows = commands.ListAllPasswordsCommand()
        for name in rows:
            print(f"Your database includes passwords for: \n - {name[1]}",
                  end="\n")
        print_options(options)
        chosen_option = get_option_choice(options)
        chosen_option.choose()
