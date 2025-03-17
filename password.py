import json
import os
import os.path
import random
import sys
from tkinter import *
from tkinter import messagebox

import pyperclip

# Determine the correct path to bundled files
if getattr(sys, 'frozen', False):  # Running as an .exe
    base_path = sys._MEIPASS  # Temporary extraction folder
else:
    base_path = os.path.dirname(os.path.abspath(__file__))  # Normal execution

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z']
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '-', '=', '{', '}', '[', ']']


# ---------------------------- SEARCH PASSWORD ------------------------------- #

def search_password():
    website = website_input.get().lower()
    exist_website = False
    try:
        if os.path.getsize(my_password_path) != 0:
            with open(file=my_password_path, mode="r") as pwd_file:
                data = json.load(pwd_file)
                exist_website = website in data
                if exist_website:
                    pwd_data = data.get(website)
                    messagebox.showinfo(title=website,
                                        message=f"UserName: {pwd_data.get("UserName")} \n Password: {pwd_data.get("Password")} \n")
    except FileNotFoundError:
        pass

    if not exist_website:
        messagebox.showinfo(title="opps", message=f"Not found any password for {website}")


def generate_pwd():
    pwd_generated = (random.choices(letters, k=random.randrange(6, 8))
                     + random.choices(numbers, k=random.randrange(2, 4))
                     + random.choices(symbols, k=random.randrange(2, 4)))

    random.shuffle(pwd_generated)

    pwd = "".join(pwd_generated)
    pyperclip.copy(pwd)
    password_input.insert(0, pwd)


def save_password(data):
    with open(file=my_password_path, mode="w") as pwd_file:
        json.dump(data, pwd_file, indent=4)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_pwd():
    website = website_input.get().lower()
    user_name = email_username_input.get()
    pwd = password_input.get()

    if website == '' or pwd == '':
        messagebox.showwarning(title="oops", message="Don't leave any fields empty!")
    else:
        is_ok = messagebox.askokcancel(title=f"{website}",
                                       message=f"UserName: {user_name} \n Password: {pwd} \n Is it Ok to add the password?")
        password = {
            website:
                {
                    "UserName": user_name,
                    "Password": pwd
                }
        }
        if is_ok:
            try:
                # open the file in mode of read
                if os.path.getsize(my_password_path) != 0:
                    with open(file=my_password_path, mode="r") as pwd_file:
                        data = json.load(pwd_file)
                        data.update(password)
                else:
                    data = password
            except FileNotFoundError:
                # create the file
                save_password(password)
            else:
                # load the data
                save_password(data)
            finally:
                # write or update the file
                website_input.delete(0, END)
                password_input.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

logo = PhotoImage(file=logo_path)
canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

website_label = Label(text="Website: ")
website_label.grid(column=0, row=1)

website_input = Entry(width=26)
website_input.grid(column=1, row=1, columnspan=2, sticky=W)
website_input.focus()

search_button = Button(text="Search", width=15, command=search_password)
search_button.grid(column=2, row=1, sticky=W)

email_username_label = Label(text="Email/UserName: ")
email_username_label.grid(column=0, row=2)

email_username_input = Entry(width=46)
email_username_input.grid(column=1, row=2, columnspan=2, sticky=W)
email_username_input.insert(0, "default@email.com")

password_label = Label(text="Password")
password_label.grid(column=0, row=3)

password_input = Entry(width=25)
password_input.grid(column=1, row=3, sticky=W)

generate_password_button = Button(text="Generate Password", command=generate_pwd)
generate_password_button.grid(column=2, row=3, sticky=W)

add_button = Button(width=46, text="Add", command=save_pwd)
add_button.grid(column=1, row=4, columnspan=2, sticky=W)

window.mainloop()
