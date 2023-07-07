import tkinter
from tkinter import messagebox
from random import choice, randint, shuffle


# ---------------------------- UI SETUP ------------------------------- #

window = tkinter.Tk()
window.title("Passman")
window.config(padx=40, pady=20)
EMAIL = "eryktostyknie@gmail.com"

canvas = tkinter.Canvas(width=200, height=200)
img = tkinter.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=img)
canvas.grid(column=1, row=0)

# Labels
title_label = tkinter.Label(text="Website:", padx=10)
title_label.grid(column=0, row=1)
email_name_label = tkinter.Label(text="Email/username:", padx=10)
email_name_label.grid(column=0, row=2)
password_label = tkinter.Label(text="Password:", padx=10)
password_label.grid(column=0, row=3)


# Entries
title_entry = tkinter.Entry(width=24)
title_entry.grid(row=1, column=1)
title_entry.focus()
email_name_entry = tkinter.Entry(width=42)
email_name_entry.grid(row=2, column=1, columnspan=2)
email_name_entry.insert(0, EMAIL)
password_entry = tkinter.Entry(width=24)
password_entry.grid(row=3, column=1)

# Buttons
generate_pass_button = tkinter.Button(text="Generate Password", width=14, command="generate_password")
generate_pass_button.grid(row=3, column=2)
add_button = tkinter.Button(text="Add", width=39, command="save")
add_button.grid(row=4, column=1, columnspan=2)
search_button = tkinter.Button(text="Search", width=14, command="find_password")
search_button.grid(row=1, column=2)

window.mainloop()
