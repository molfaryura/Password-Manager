"""GUI Password Manager"""

import hashlib

from tkinter import *
from tkinter import messagebox

from db import PasswordManagerDatabase

from password_generator import PassWord

BG_COLOR = '#669170'

def generate_message(account: list):
    """Creates a string message from the given account information.

    Args:
        account(list of tuple): The account information in the format [(account, password), ...].

    Returns:
        str: The generated message with each account and its associated passwords.
    """

    my_dct = {k: [v for kk, v in account if kk == k] for k, _ in account}
    if len(my_dct) > 1:
        return '\n'.join([f"{k}: {', '.join(v)}" for k, v in my_dct.items()])
    else:
        return ' '.join([f"{k}: {', '.join(v)}" for k, v in my_dct.items()])


class PasswordManager():

    def __init__(self) -> None:
        self.window = Tk()
        self.window.title('Password Manager')
        self.window.config(padx=10, pady=10, bg=BG_COLOR)

        self.canvas = Canvas(width=200, height=200, bg=BG_COLOR, highlightthickness=0)
        logo_img = PhotoImage(file='img/logo.png')
        self.canvas.create_image(100, 100, image=logo_img)
        self.canvas.grid(column=1, row=0)
        
        self.db = PasswordManagerDatabase()
        self.check_secret_table()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.window.mainloop()

    def create_main_widgets(self):
        secret_word_label = Label(text='Secret Word:', bg=BG_COLOR, font=('Arial', 12, 'bold'))
        secret_word_label.grid(column=0, row=1)

        self.secret_word_entry = Entry(width=21)
        self.secret_word_entry.grid(column=1, row=1)
        self.secret_word_entry.focus()

        self.hint_button_image = PhotoImage(file='img/hint.png')
        self.hint_button = Button(image=self.hint_button_image, width=32, bg=BG_COLOR, highlightthickness=0, command=self.pressed_hint_button)
        self.hint_button.grid(column=2, row=1)

        account_label = Label(text='Account:', bg=BG_COLOR, font=('Arial', 12, 'bold'))
        account_label.grid(column=0, row=2)

        self.account_entry = Entry(width=21)
        self.account_entry.grid(column=1, row=2, pady=10)

        self.search_button_image = PhotoImage(file='img/search_button.png')
        self.search_button = Button(image=self.search_button_image, width=32, bg=BG_COLOR, highlightthickness=0, command=self.show_password)
        self.search_button.grid(column=2, row=2)

        password_label = Label(text='Password:', bg=BG_COLOR, font=('Arial', 12, 'bold'))
        password_label.grid(column=0, row=3)

        self.password_entry = Entry(width=21)
        self.password_entry.grid(column=1, row=3)

        self.generate_button_image = PhotoImage(file='img/generator.png')
        self.generate_password_button = Button(image=self.generate_button_image, bg=BG_COLOR, highlightthickness=0, command=self.pressed_password_button)
        self.generate_password_button.grid(column=3, row=3, padx=5)

        self.spinner = Spinbox(self.window, from_=4, to=20, increment=1, width=2)
        self.spinner.grid(column=2, row=3, padx=5)

        self.add_button = Button(text='Save account and password',highlightthickness=0, width=21, command=self.pressed_add_button)
        self.add_button.grid(column=1, row=4, columnspan=1, pady=10)

    
    def create_secret_word(self):
        messagebox.showinfo(title='Attention', message=('Please create secret word, hint, and type the icon to start. '))
        self.save_image = PhotoImage(file='img/save.png')
        self.add_secret_word_button = Button(image=self.save_image,highlightthickness=0, bg=BG_COLOR ,command=self.pressed_add_secret_word_button)
        self.add_secret_word_button.grid(column=2, row=4,  pady=10, rowspan=2)

        self.add_secret_word_entry = Entry(width=21)
        self.add_secret_word_entry.grid(column=1, row=4, pady=10)

        self.add_hint_entry = Entry(width=21)
        self.add_hint_entry.grid(column=1, row=5)

        self.add_secret_word_label = Label(text='Secret Word:', bg=BG_COLOR, font=('Arial', 12, 'bold'))
        self.add_secret_word_label.grid(column=0, row=4)

        self.add_hint_label = Label(text='Hint:', bg=BG_COLOR, font=('Arial', 12, 'bold'))
        self.add_hint_label.grid(column=0, row=5)


    def pressed_add_secret_word_button(self):
        self.save_secrete_word_and_hint()

        self.add_secret_word_button.destroy()
        self.add_secret_word_entry.destroy()
        self.add_hint_entry.destroy()
        self.add_secret_word_label.destroy()
        self.add_hint_label.destroy()

        self.create_main_widgets()

    def pressed_hint_button(self):
        hint = self.db.select_hint_from_db()
        messagebox.showinfo(message=hint)

    def pressed_add_button(self):
        if self.is_secret_word_match():
            self.db.create_main_table()
            account = self.account_entry.get()
            password = self.password_entry.get()
            self.db.insert_account_and_password(account, password)
            messagebox.showinfo(title='Success',
                                message=('Data has been saved successfully.'))

        self.clear_entry()

    def pressed_password_button(self):
        self.password_entry.delete(0, END)
        number = int(self.spinner.get())
        password = PassWord(number).password
        self.password_entry.insert(END, password)


    def save_secrete_word_and_hint(self):
        secret_word = hashlib.sha256(self.add_hint_entry.get().encode()).hexdigest()
        self.hint = self.add_hint_entry.get()
        self.db.create_secret_word_table()
        self.db.insert_secret_word_and_hint(secret_word, self.hint)

    def is_secret_word_match(self) -> bool:
        user_secret_word = hashlib.sha256(self.secret_word_entry.get().encode()).hexdigest()
        result = user_secret_word == self.db.select_secret_word_from_db()[0][0]
        if result:
            return True
        else:
            messagebox.showerror(title='Error', message=('Incorrect secret word!'))
            return False


    def check_secret_table(self):
        if not self.db.check_if_secret_table_exists():
            self.create_secret_word()
        else:
            self.create_main_widgets()


    def show_password(self):
        if self.is_secret_word_match():
            account_name = self.account_entry.get()
            result = self.db.select_password_from_db(account_name)
            if result:
                message = generate_message(result)
                messagebox.showinfo(message=message)
            else:
                messagebox.showerror(message='This account does not exists')

        self.clear_entry()


    def clear_entry(self):
        self.account_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.secret_word_entry.delete(0, END)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.db.close_db_connection()
            self.window.destroy()
