from tkinter import *
import sqlite
from tkinter import messagebox, simpledialog
import string
from random import randint, choice, shuffle
from tkinter.simpledialog import askstring
import gen_key


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    ran_num = randint(5, 10)
    pass_letters = [choice(string.ascii_letters) for _ in range(ran_num)]
    pass_nums = [choice(string.digits) for _ in range(ran_num)]
    pass_chars = [choice(string.punctuation) for _ in range(ran_num)]

    pass_list = pass_nums + pass_chars + pass_letters
    shuffle(pass_list)
    result = "".join(pass_list)
    password_entry.insert(0, result)


# ---------------------------- ENCRYPT PASSWORD ------------------------------- # Search username, if exist there is
# possibly an encryption file so no need for generate key. After that you can add another condition t osearch file in
# the current directory, if you would like.
password_key = askstring("Input", "This will encrypt your file! Do not forget your password!!\nEnter Password: ")
gen_key.generate_key(password_key)

messagebox.showerror(title="Error", message="Password is wrong. Try again!")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    username = username_entry.get()
    website = website_entry.get()
    email = gen_key.encrypt(email_entry.get())
    password = gen_key.encrypt(password_entry.get())

    if len(username) < 1 or len(website) < 1 or len(email) < 1 or len(password) < 1:
        messagebox.showinfo(title="No no nooo...", message="Don't leave any fields empty. Go back and fill "
                                                           "them...please!")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"{username}, do you want to continue?")
        if is_ok:
            conn = sqlite.create_connection(username)
            sqlite.data_entry(conn, website, email, password)
            # After db write, delete fields
            website_entry.delete(0, END)
            email_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- SEARCH SETUP ------------------------------- #

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
window.columnconfigure(index=1, weight=2)
window.rowconfigure(index=0, weight=2)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img, anchor='center')
canvas.grid(row=0, column=1, columnspan=1)

# Labels
username_label = Label(text="App User: ")
username_label.grid(row=1, column=0, sticky='w')
website_label = Label(text="Website name/URL: ")
website_label.grid(row=2, column=0, sticky='w')
email_label = Label(text="Email/Username: ")
email_label.grid(row=3, column=0, sticky='w')
password_label = Label(text="Password: ")
password_label.grid(row=4, column=0, sticky='w')

# Entries
username_entry = Entry(width=40, borderwidth=2)
username_entry.focus()
username_entry.grid(row=1, column=1, columnspan=3)
website_entry = Entry(width=40, borderwidth=2)
website_entry.grid(row=2, column=1, columnspan=3, sticky='w')
email_entry = Entry(width=40, borderwidth=2)
email_entry.grid(row=3, column=1, columnspan=3, sticky='w')
password_entry = Entry(width=23, borderwidth=2)
password_entry.grid(row=4, column=1, sticky='w')

# Buttons
gen_pass = Button(text="Gen Password", command=generate_password)
gen_pass.grid(row=4, column=2, sticky='e')
add_btn = Button(text="Add to DB", width=37, command=save)
add_btn.grid(row=5, column=1, columnspan=2)

window.mainloop()
