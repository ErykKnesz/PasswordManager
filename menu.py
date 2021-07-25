import sql
from tkinter import Tk
import security


def ask_for_prompt():
    """Ask the user to choose an option from menu"""
    prompt = """Choose your action:
        0 - exit the programrd,
        2 - add a password,
        3 - update a password,, 
        1 - select a passwo
        4 - delete a password,
        Please enter the relevant number: """

    try:
        option = int(input(prompt))
        if option in range(5):
            return option
        else:
            print("No such option, try again!")
            return ask_for_prompt()
    except ValueError:
        print("Only numbers from 0 to 4 are allowed")
        return ask_for_prompt()


def perform_desired_action(conn, option):
    if option == 0:
        exit()
    elif option == 1:
        perform_select_password(conn)
    elif option == 2:
        perform_add(conn)
    elif option == 3:
        perform_update(conn)
    elif option == 4:
        perform_delete(conn)


def perform_select_password(conn):
    name = input("Enter the name to select this password from DB: ")
    row = sql.select_passwords_where(conn, name=name)
    password = row[0][2]
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(password)
    r.update()  # now it stays on the clipboard after the window is closed
    return password


def perform_add(conn):
    name = input("Enter the name of the service or tool/program: ")
    while True:
        password_1 = input("Enter the password: ")
        password_2 = input("Enter the password again: ")
        if password_1 == password_2:
            sql.add_password(conn, name, password_1)
            break
        else:
            print("The passwords do not match")
            continue


def perform_update(conn):
    name = input("Provide the name of the password you want to update: ")
    db_row = sql.select_passwords_where(conn, name=name)
    new_name = input(f"Update current name: {name}. New name: ")

    while True:
        new_password_1 = input(f"Update password for {name}. New one: ")
        new_password_2 = input(f"Reenter the new password for {name}: ")
        id = db_row[0][0]
        if new_password_1 == new_password_2:
            sql.update(conn, id,
                       name=new_name, password=new_password_1)
            break
        else:
            continue


def perform_delete(conn):
    name = input("Provide the name of the password you want to delete: ")
    db_row = sql.select_passwords_where(conn, name=name)
    sql.delete(conn, db_row[0][0])