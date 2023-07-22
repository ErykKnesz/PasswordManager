import argparse

from database_manager import DatabaseManager
import commands
from menu import Menu, Prompter, Option

# Run without GUI by default, or enable GUI
parser = argparse.ArgumentParser(description='Want a GUI?')
parser.add_argument('-g', '--gui', action='store_true', help="Run with GUI")
args = parser.parse_args()

prompter = Prompter()
cli_options = {
    'A': Option('Add password', commands.AddPasswordCommand(),
                prep_call=prompter.get_new_password_data, prep_call_required=True),
    'B': Option('Select a password', commands.RetrievePasswordCommand(),
                prep_call=prompter.get_retrieve_data, prep_call_required=True),
    'C': Option('Update password', commands.UpdatePasswordCommand(),
                prep_call=prompter.get_update_data, prep_call_required=True),
    'D': Option('Delete password', commands.DeletePasswordCommand(),
                prep_call=prompter.get_delete_data, prep_call_required=True),
    'Q': Option('Quit', commands.QuitCommand())
}
cli_menu = Menu(cli_options)
db = DatabaseManager("PasswordManager")

if __name__ == '__main__':
    try:
        db.create_database()
        commands.CreatePasswordsTableCommand().execute()
    except AttributeError:
        print("Wrong credentials")
        commands.QuitCommand().execute()
    passwords_command = commands.ListAllPasswordsCommand()
    if args.gui is True:
        import gui
        gui_app = gui.GUI()
        gui_app.mainloop()
    else:
        passman_is_running = True
        while passman_is_running:
            print("Your database includes passwords for:")
            for title in passwords_command.execute():
                print(f"- {title[1]}",
                      end="\n")
            cli_menu.print_options()
            chosen_option = prompter.get_option_choice(cli_options)
            chosen_option.choose()
