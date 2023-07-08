import sys
import logging
from tkinter import Tk
import cryptography
from database_manager import DatabaseManager
from security import Cryptographer

cryptographer = Cryptographer()
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
        password = cryptographer.encrypt_psw(data['password']) # encryption
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
            password = cryptographer.decrypt_psw(password)  # decryption
            r = Tk()
            r.withdraw()
            r.clipboard_clear()
            r.clipboard_append(password)
            r.update()
            return 'Password found and copied'
        except (IndexError, TypeError) as e:
            logging.error(e)
            return "No such password found"
        except cryptography.fernet.InvalidToken:
            return "Unauthorised, invalid token used"


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
