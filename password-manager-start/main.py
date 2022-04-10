from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import pygame
import json

FONT_LABEL = ("Times", 13, "bold")
GREY = "#DBD0C0"


# ---------------------------- NOTIFICATION SOUND ------------------------------- #

def alert_sound():
    pygame.mixer.init()
    pygame.mixer.music.load("pop sound.wav")
    pygame.mixer.music.play(loops=0)


def confirmation_sound():
    pygame.mixer.init()
    pygame.mixer.music.load("correct_answer.wav")
    pygame.mixer.music.play(loops=0)


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    # Password Generator Project
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

  

    password_letters = [choice(letters) for _ in range(randint(8, 10))]

    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols

    shuffle(password_list)
    # Joins the list values as how define it.
    # for eg: names = [Fazhil, umar, qathab]
    # ----- x = "#".join(names)
    # --- O/P : Fazhil#umar#qathab

    password = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    # Automatically copies the password. -- pyperclip module --
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website_data = website_entry.get()
    email_data = email_entry.get()
    password_data = password_entry.get()
    new_user_data = {
        website_data: {"email": email_data,
                       "password": password_data,
                       }
    }

    if len(website_data) == 0 and len(password_data) == 0 and len(email_data) == 0:
        alert_sound()
        messagebox.showwarning(title="Try Again",
                               message="Mandatory Fields are missing. Please check all fields.")

    elif len(website_data) == 0 and len(password_data) == 0:
        alert_sound()
        messagebox.showwarning(title="Try Again",
                               message="Mandatory Fields are missing. Please check your Website and Password fields.")

    elif len(email_data) == 0 and len(password_data) == 0:
        alert_sound()
        messagebox.showwarning(title="Try Again",
                               message="Mandatory Fields are missing. Please check your Email and Password fields.")

    elif len(website_data) == 0:
        alert_sound()
        messagebox.showwarning(title="Try Again",
                               message="Mandatory Fields are missing. Please fill your Website.")
        website_entry.focus()

    elif len(password_data) == 0:
        alert_sound()
        messagebox.showwarning(title="Try Again",
                               message="Mandatory Fields are missing. Please fill your Password.")
        password_entry.focus()

    elif len(email_data) == 0:
        alert_sound()
        messagebox.showwarning(title="Try Again",
                               message="Mandatory Fields are missing. Please fill your Email/Username.")
        email_entry.focus()

    else:
        confirmation_sound()
        is_ok = messagebox.askokcancel(title=f"For WEBSITE: {website_data}",
                                       message=f"Your credentials: "
                                               f"\n\nEmail/Username: {email_data} "
                                               f"\nPassword: {password_data} "
                                               f"\n\nClick 'OK' to Save your Credentials.")

        if is_ok:
            try:
                with open("data.json", mode="r") as data_file:
                    # Loading the file.
                    user_data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", mode="w") as data_file:
                    json.dump(new_user_data, data_file, indent=4)
            else:
                # Updating with new data.
                user_data.update(new_user_data)
                # Writing to that file with the updated version.
                with open("data.json", mode="w") as data_file:
                    json.dump(user_data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD & DATA (Search Button)------------------------------- #
def find_data():
    website = website_entry.get()
    if len(website) == 0:
        alert_sound()
        messagebox.showwarning(title="Try Again",
                               message="Please fill your Website to get your credentials.")
        website_entry.focus()
    else:
        try:
            with open("data.json", mode="r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            alert_sound()
            messagebox.showwarning(title="Error", message="No Data File Found!")
        else:
            alert_sound()
            if website_entry.get() not in data:
                messagebox.showwarning(title=f"{website} Credentials Not Found",
                                       message="No details for this website exists!")
            else:
                confirmation_sound()
                email = data[website]["email"]
                password = data[website]["password"]
                messagebox.showinfo(title=website, message=f"Your credentials: "
                                                           f"\n\nEmail/Username: {email} "
                                                           f"\nPassword: {password} "
                                    )


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, background=GREY)

canvas = Canvas(width=200, height=200, highlightthickness=0, background=GREY)
pass_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=pass_image)
canvas.grid(column=1, row=0)

# Website Label
website_label = Label(text="Website:", font=FONT_LABEL, background=GREY)
website_label.grid(column=0, row=1)
# Email/Username Label
email_label = Label(text="Email/Username:", font=FONT_LABEL, background=GREY)
email_label.grid(column=0, row=2)
# Password Label
password_label = Label(text="Password:", font=FONT_LABEL, background=GREY)
password_label.grid(column=0, row=3)

# Website Entry
website_entry = Entry(width=33)
website_entry.focus()
website_entry.grid(column=1, row=1, columnspan=1, pady=5)
# Email/Username Entry
email_entry = Entry(width=52)
email_entry.insert(0, "fazhilumar@gmail.com")
email_entry.grid(column=1, row=2, columnspan=2, pady=5)
# Password Entry
password_entry = Entry(width=33)
password_entry.grid(column=1, row=3)

# Generate Password Button
password_button = Button(text="Generate Password", highlightthickness=0, command=generate_password)
password_button.grid(column=2, row=3, pady=5)
# Add Button
add_button = Button(text="Add Website Credentials", width=45, highlightthickness=0, command=save)
add_button.grid(column=1, row=4, columnspan=2)
# Search Button
search_button = Button(text="Search", highlightthickness=0, width=14, command=find_data)
search_button.grid(column=2, row=1)
window.mainloop()
#THE END :)
