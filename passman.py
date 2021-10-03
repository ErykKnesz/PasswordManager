from database_manager import DatabaseManager
import commands
import menu

db = DatabaseManager("PasswordManager")

if __name__ == '__main__':
    db.create_database()
    create_table = commands.CreatePasswordsTableCommand()
    create_table.execute()
    is_on = True
    while is_on:
        passwords = commands.ListAllPasswordsCommand()
        rows = passwords.execute()
        print("Your database includes passwords for:")
        for name in rows:
            print(f"- {name[1]}",
                  end="\n")
        menu.print_options(menu.options)
        chosen_option = menu.get_option_choice(menu.options)
        chosen_option.choose()
