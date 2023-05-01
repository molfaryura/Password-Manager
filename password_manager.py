"""GUI Password Manager"""

import hashlib

from tkinter import *
from tkinter import messagebox

from psycopg2 import errors

from db import PasswordManagerDatabase

from password_generator import PassWord

from widgets import MainWidgets, Buttons, SecretWordUi

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
    return ' '.join([f"{k}: {', '.join(v)}" for k, v in my_dct.items()])


class PasswordManager():
    main_buttons = None
    secret_word_buttons = None

    def __init__(self) -> None:
        self.window = Tk()
        self.window.title('Password Manager')
        self.window.config(padx=10, pady=10, bg=BG_COLOR)

        canvas = Canvas(width=200, height=200, bg=BG_COLOR, highlightthickness=0)
        logo_img = PhotoImage(file='img/logo.png')
        canvas.create_image(100, 100, image=logo_img)
        canvas.grid(column=1, row=0)

        self.main_widgets = None

        self.db = PasswordManagerDatabase()
        self.check_secret_table()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.window.mainloop()

    def create_main_widgets(self):
        secret_word_label = Label(text='Secret Word:', bg=BG_COLOR, font=('Arial', 12, 'bold'))
        secret_word_label.grid(column=0, row=1)

        self.main_widgets = MainWidgets()
        self.main_widgets.create_spinner(root=self.window)
        self.main_widgets.grid_items()

        account_label = Label(text='Account:', bg=BG_COLOR, font=('Arial', 12, 'bold'))
        account_label.grid(column=0, row=2)

        PasswordManager.main_buttons = Buttons()
        PasswordManager.main_buttons.create_add_button()
        self.config_main_buttons()

        password_label = Label(text='Password:', bg=BG_COLOR, font=('Arial', 12, 'bold'))
        password_label.grid(column=0, row=3)


    def pressed_add_secret_word(self):
        self.save_secrete_word_and_hint()

        PasswordManager.secret_word_buttons.add_secret_word_button.destroy()
        PasswordManager.secret_word_buttons.add_secret_word_entry.destroy()
        PasswordManager.secret_word_buttons.add_hint_entry.destroy()
        PasswordManager.secret_word_buttons.add_secret_word_label.destroy()
        PasswordManager.secret_word_buttons.add_hint_label.destroy()

        self.create_main_widgets()

    def pressed_hint_button(self):
        hint = self.db.select_hint_from_db()
        messagebox.showinfo(message=hint)

    def pressed_add_button(self):
        if self.is_secret_word_match():
            self.db.create_main_table()
            account = self.main_widgets.account_entry.get()
            password = self.main_widgets.password_entry.get()
            self.db.insert_account_and_password(account, password)
            messagebox.showinfo(title='Success',
                                message=('Data has been saved successfully.'))

        self.clear_entry()

    def pressed_password_button(self):
        self.main_widgets.password_entry.delete(0, END)
        number = int(self.main_widgets.spinner.get())
        password = PassWord(number).password
        self.main_widgets.password_entry.insert(END, password)


    def save_secrete_word_and_hint(self):
        secret_word = hashlib.sha256(self.secret_word_buttons.add_secret_word_entry.get().encode())
        secret_word = secret_word.hexdigest()
        hint = self.secret_word_buttons.add_hint_entry.get()

        try:
            self.db.create_secret_word_table()
        except errors.InFailedSqlTransaction:
            self.db.connect_to_db.rollback()
        finally:
            self.db.create_secret_word_table()

        self.db.insert_secret_word_and_hint(secret_word, hint)

    def is_secret_word_match(self) -> bool:
        user_secret_word = hashlib.sha256(self.main_widgets.secret_word_entry.get().encode())
        user_secret_word = user_secret_word.hexdigest()
        result = user_secret_word == self.db.select_secret_word_from_db()[0][0]
        if result:
            return True
        messagebox.showerror(title='Error', message=('Incorrect secret word!'))
        return False


    def check_secret_table(self):
        self.db.start_db_connection()

        if not self.db.check_if_secret_table_exists():
            PasswordManager.secret_word_buttons = SecretWordUi(bg_color=BG_COLOR)
            PasswordManager.secret_word_buttons.secret_word_buttons()
            PasswordManager.secret_word_buttons.grid_items()
            add_secret_word_btn = PasswordManager.secret_word_buttons.add_secret_word_button
            add_secret_word_btn.config(command=self.pressed_add_secret_word)
        else:
            self.create_main_widgets()


    def show_password(self):
        if self.is_secret_word_match():
            account_name = self.main_widgets.account_entry.get()
            result = self.db.select_password_from_db(account_name)
            if result:
                message = generate_message(result)
                messagebox.showinfo(message=message)
            else:
                messagebox.showerror(message='This account does not exists')

        self.clear_entry()

    def config_main_buttons(self):
        PasswordManager.main_buttons.hint_button.config(command=self.pressed_hint_button)
        search_button = PasswordManager.main_buttons.search_button
        search_button.config(command=self.show_password)
        generate_password_button = PasswordManager.main_buttons.generate_password_button
        generate_password_button.config(command=self.pressed_password_button)
        PasswordManager.main_buttons.add_button.config(command=self.pressed_add_button)


    def clear_entry(self):
        self.main_widgets.account_entry.delete(0, END)
        self.main_widgets.password_entry.delete(0, END)
        self.main_widgets.secret_word_entry.delete(0, END)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.db.close_db_connection()
            self.window.destroy()
