import tkinter
from tkinter import messagebox
from random import choice, randint, shuffle

import commands
# ---------------------------- UI SETUP ------------------------------- #


class GUI(tkinter.Tk):
    def __init__(self):
        super().__init__()

        self.title("Passman")
        self.config(padx=40, pady=20)
        self.canvas = tkinter.Canvas(width=200, height=200)
        self.img = tkinter.PhotoImage(file="logo.png")
        self.canvas.create_image(100, 100, image=self.img)
        self.canvas.grid(column=2, row=0)

        self.table = self.create_table_widget()

        # Labels
        self.title_label = tkinter.Label(text="Website:", padx=10)
        self.title_label.grid(column=0, row=2)
        self.email_name_label = tkinter.Label(text="Email/username:", padx=1)
        self.email_name_label.grid(column=0, row=3)
        self.password_label = tkinter.Label(text="Password:", padx=10)
        self.password_label.grid(column=0, row=4)

        # Entries
        self.title_entry = tkinter.Entry(width=24)
        self.title_entry.grid(row=2, column=1)
        self.title_entry.focus()
        self.email_name_entry = tkinter.Entry(width=42)
        self.email_name_entry.grid(row=3, column=1, columnspan=2)
        self.email_name_entry.insert(0, "EMAIL")
        self.password_entry = tkinter.Entry(width=24)
        self.password_entry.grid(row=4, column=1)

        # Buttons
        self.generate_pass_button = tkinter.Button(text="Generate Password", width=14, command="generate_password")
        self.generate_pass_button.grid(row=4, column=2)
        self.add_button = tkinter.Button(text="Add", width=22,
                                         command=lambda: commands.AddPasswordCommand(
                                         ).execute({
                                             "password": self.password_entry.get(),
                                             "name": self.title_entry.get()}
                                                  ))
        self.add_button.grid(row=5, column=1)
        self.update_button = tkinter.Button(text="Update", width=14,
                                            command=lambda: commands.UpdatePasswordCommand(
                                            ).execute({
                                             "password": self.password_entry.get(),
                                             "name": self.title_entry.get()}
                                                  ))
        self.update_button.grid(row=5, column=2)
        self.search_button = tkinter.Button(text="Search", width=14, command="find_password")
        self.search_button.grid(row=2, column=2)

    def create_table_widget(self):
        list_items = tkinter.Variable(value=[i[1] for i in commands.ListAllPasswordsCommand().execute()])
        listbox = tkinter.Listbox(
            self,
            height=10,
            listvariable=list_items
        )
        # for i in commands.ListAllPasswordsCommand().execute():
        #     listbox.insert("end", i)
        listbox.grid(column=0, columnspan=2, row=0)
        listbox.bind('<Double-1>', "some edit view function")
        return list_items





