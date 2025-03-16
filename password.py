import random
from tkinter import *
from tkinter import messagebox

import pyperclip

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z']
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '-', '=', '{', '}', '[', ']']


def generate_pwd():
    pwd_generated = (random.choices(letters, k=random.randrange(6, 8))
                     + random.choices(numbers, k=random.randrange(2, 4))
                     + random.choices(symbols, k=random.randrange(2, 4)))

    random.shuffle(pwd_generated)

    pwd = "".join(pwd_generated)
    pyperclip.copy(pwd)
    password_input.insert(0, pwd)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_pwd():
    website = website_input.get()
    user_name = email_username_input.get()
    pwd = password_input.get()

    if website == '' or pwd == '':
        messagebox.showwarning(title="oops", message="Don't leave any fields empty!")
    else:
        is_ok = messagebox.askokcancel(title=f"{website}",
                                       message=f"UserName: {user_name} \n Password: {pwd} \n Is it Ok to add the password?")
        if is_ok:
            with open(file="my_password.txt", mode="a") as pwd_file:
                pwd_file.write(f"{website} | {user_name} | {pwd} \n")
                website_input.delete(0, END)
                password_input.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

logo = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

website_label = Label(text="Website: ")
website_label.grid(column=0, row=1)

website_input = Entry(width=46)
website_input.grid(column=1, row=1, columnspan=2, sticky=W)
website_input.focus()

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
