import tkinter
from tkinter import ttk
from tkinter import messagebox
from random import choice, randint, shuffle

import commands
# ---------------------------- UI SETUP ------------------------------- #
EDIT_BG = "white"
BTN_SUCCESS_BG = "#7cd8ad"
BTN_SUCCESS_BG_ACTIVE = "#a8e5c8"
BTN_DANGER_BG = "#ff8080"
BTN_DANGER_BG_ACTIVE = "#ff9999"
BTN_INFO_BG = "#b3e6ff"
BTN_INFO_BG_ACTIVE = "#cceeff"


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
        self.title_label = tkinter.Label(text="Title:", padx=10)
        self.title_label.grid(column=0, row=2)
        self.login_label = tkinter.Label(text="Login:", padx=1)
        self.login_label.grid(column=0, row=3)
        self.password_label = tkinter.Label(text="Password:", padx=10)
        self.password_label.grid(column=0, row=4)

        # Entries
        self.title_entry = tkinter.Entry(width=24)
        self.title_entry.grid(row=2, column=1)
        self.title_entry.focus()
        self.login_entry = tkinter.Entry(width=24)
        self.login_entry.grid(row=3, column=1)
        self.login_entry.insert(0, "EMAIL")
        self.password_entry = tkinter.Entry(show="*", width=24)
        self.password_entry.grid(row=4, column=1)

        # Buttons
        self.generate_pass_button = tkinter.Button(text="Generate Password", width=14,
                                                   background=BTN_INFO_BG,
                                                   activebackground=BTN_INFO_BG_ACTIVE,
                                                   command="generate_password")
        self.generate_pass_button.grid(row=3, column=2)
        self.add_button = tkinter.Button(text="Add", width=21,
                                         background=BTN_SUCCESS_BG,
                                         activebackground=BTN_SUCCESS_BG_ACTIVE,
                                         command=self.add_item)
        self.add_button.grid(row=5, column=1)
        self.delete_button = tkinter.Button(text="Delete", width=14,
                                            background=BTN_DANGER_BG,
                                            activebackground=BTN_DANGER_BG_ACTIVE,
                                            command=self.delete_item)
        self.delete_button.grid(row=4, column=2)

        # Edit Frame
        self.edit_frame = tkinter.Frame(self, bg=EDIT_BG,
                                        highlightbackground="black",
                                        highlightthickness=0.5)
        self.edit_frame.grid(row=0, column=1)
        self.edit_frame.grid_forget()  # hide until enabled
        self.close_edit_button = tkinter.Button(self.edit_frame, text="X",
                                                command=self.close_edit_mode,
                                                background=BTN_DANGER_BG,
                                                activebackground=BTN_DANGER_BG_ACTIVE,
                                                padx=0,
                                                pady=0)
        self.close_edit_button.pack(anchor=tkinter.NE)
        self.edit_title_label = tkinter.Label(self.edit_frame, text="Title:",
                                              bg=EDIT_BG)
        self.edit_title_label.pack()
        self.edit_title_entry = tkinter.Entry(self.edit_frame, bg=EDIT_BG)
        self.edit_title_entry.pack(expand=True)
        self.edit_login_label = tkinter.Label(self.edit_frame, text="Login:",
                                              bg=EDIT_BG)
        self.edit_login_label.pack()
        self.edit_login_entry = tkinter.Entry(self.edit_frame, bg=EDIT_BG)
        self.edit_login_entry.pack(expand=True)
        self.edit_password_label = tkinter.Label(self.edit_frame, text="Password:",
                                                 bg=EDIT_BG)
        self.edit_password_label.pack()
        self.edit_password_entry = tkinter.Entry(self.edit_frame, bg=EDIT_BG)
        self.edit_password_entry.pack(expand=True)
        self.update_button = tkinter.Button(
            self.edit_frame,
            background=BTN_SUCCESS_BG,
            activebackground=BTN_SUCCESS_BG_ACTIVE,
            text="Update",
            width=14,
            pady=5,
            command=lambda: commands.UpdatePasswordCommand(
                ).execute({
                    "name": self.edit_title_entry.get(),
                    "login": self.edit_login_entry.get(),
                    "password": self.edit_password_entry.get()
                         })
            )
        self.update_button.pack(fill=tkinter.BOTH, expand=True)


    def create_table_widget(self):
        columns = ("id", "title",)
        table = ttk.Treeview(self, columns=columns, show="headings")
        table.heading("id", text="id")
        table.heading("title", text="Title")
        table["displaycolumns"] = ("title",)
        table.bind("<Button-3>", self.open_menu)
        table.bind("<Double-1>", self.get_password)
        table.grid(row=0, column=0, sticky=tkinter.NSEW)

        scrollbar = ttk.Scrollbar(self, orient=tkinter.VERTICAL, command=table.yview)
        self.bind("<Button-4>", lambda event: self.table.yview_scroll(int(-1*event.num), "units"))
        table.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="nsw")

        #  Right click context menu
        table.menu = tkinter.Menu(table, tearoff=0)
        table.menu.add_command(label="Edit", command=self.open_edit_mode)
        table.menu.bind("<FocusOut>", self.close_menu)

        for i in commands.ListAllPasswordsCommand().execute():
            table.insert("", tkinter.END, values=i)
        return table

    def open_menu(self, event):
        try:
            self.table.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.table.menu.grab_release()

    def close_menu(self, event):
        self.table.menu.unpost()

    def open_edit_mode(self):
        self.edit_frame.grid(row=0, column=1)
        self.edit_frame.winfo_children()[2].focus_set()
        self.edit_frame.winfo_children()[2].insert(0,text)
        print(self.edit_frame.winfo_children())
        self.edit_frame.grab_set()

    def close_edit_mode(self):
        self.edit_frame.grab_release()
        self.edit_frame.grid_forget()


    def get_password(self, event):
        print(event)
        for item in self.table.selection():
            title = self.table.item(item, 'values')[1]
            commands.RetrievePasswordCommand().execute({"name": title})
            messagebox.showinfo("Success", "Password is in your clipboard now!")

    def add_item(self):
        data = {
            "name": self.title_entry.get(),
            "login": self.login_entry.get(),
            "password": self.password_entry.get(),
        }
        lastrowid = commands.AddPasswordCommand().execute(data)
        self.table.insert('', tkinter.END, values=(lastrowid,
                                                   data["name"],
                                                   data["login"],
                                                   data["password"]))

    def delete_item(self):
        for item in self.table.selection():
            obj_id = self.table.item(item, 'values')[0]
            self.table.delete(item)
            commands.DeletePasswordCommand().execute(obj_id)

    def update_item(self):
        selected_item = self.table.selection()[0]
        obj_id = self.table.item(selected_item, "values")[0]
        data = {}
        commands.UpdatePasswordCommand().execute(obj_id, data)
        self.table.item(selected_item, text="blub", values=("foo", "bar"))
        self.edit_frame.grid_forget()
        pass # see above




