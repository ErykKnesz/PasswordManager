import sys
import logging
from tkinter import Tk
from database_manager import DatabaseManager
import security

db = DatabaseManager("PasswordManager")


class CreatePasswordsTableCommand:
    def execute(self):
        db.create_table('passwords', {
            'id': 'INTEGER PRIMARY KEY AUTO_INCREMENT',
            'name': 'VARCHAR(255) NOT NULL UNIQUE',
            'password': 'VARCHAR(255) NOT NULL',
        })


class AddPasswordCommand:
    def execute(self, data):
        password = security.encrypt_psw(data['password']) # encryption
        db.add_password(data['name'], password)
        return "Password added!"


class ListAllPasswordsCommand:
    def execute(self):
        return db.select_all()


class ListAllPasswordsWhereCommand:
    def execute(self, **query):
        return db.select_passwords_where(**query)


class RetrievePasswordCommand:
    def execute(self, data):
        row = db.retrieve_password(data['name'])
        try:
            password = row[0]
            password = security.decrypt_psw(password) # decryption
            r = Tk()
            r.withdraw()
            r.clipboard_clear()
            r.clipboard_append(password)
            r.update()  # now it stays on the clipboard after the window is closed
            return 'Password found and copied'
        except IndexError as e:
            logging.error(e)
            return "No such password found"


class DeletePasswordCommand:
    def execute(self, data):
        db.delete('passwords', data)
        return "Password deleted!"


class UpdatePasswordCommand:
    def execute(self, data):
        id = data.pop('id')
        db.update(id, **data)
        return "Password updated!"


class QuitCommand:
    def execute(self):
        sys.exit()


create_table = CreatePasswordsTableCommand()
add = AddPasswordCommand()
list_passwords = ListAllPasswordsCommand()
passwords_by = ListAllPasswordsWhereCommand()
retrieve = RetrievePasswordCommand()
update = UpdatePasswordCommand()
delete = DeletePasswordCommand()
quit = QuitCommand()