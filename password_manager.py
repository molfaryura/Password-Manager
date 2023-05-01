"""GUI Password Manager"""

import hashlib

from tkinter import Tk, Canvas, PhotoImage, Label, END
from tkinter import messagebox

from psycopg2 import errors

from db import PasswordManagerDatabase

from password_generator import PassWord

from widgets import MainWidgets, Buttons, SecretWordUi

BG_COLOR = '#669170'

def generate_message(account: list) -> str:
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
    """A password manager GUI application that stores account and password information in the db.

    Attributes:
    -----------
    window: trkinter.Tk
        the main window of the application.
    main_widgets: MainWidgets
        a collection of UI widgets for the main screen.
    data_base: PasswordManagerDatabase
        a database that stores the account and password information.
    main_buttons: Buttons
        a collection of UI buttons for the main screen.
    secret_word_buttons: SecretWordUi
        a collection of UI buttons for the secret word input screen.

    Methods:
    -----------
    create_main_widgets():
        Creates the main widgets of the GUI for account and password input.
    pressed_add_secret_word():
        Saves the secret word and hint to the database and creates the main widgets.
    pressed_hint_button():
        Shows the hint associated with the secret word.
    pressed_add_button():
        Saves the account and password to the database if the secret word is correct.
    pressed_password_button():
        Generates a random password and inserts it into the password entry.
    save_secrete_word_and_hint():
        Hashes and saves the secret word and hint to the database.
    is_secret_word_match() -> bool:
        Compares the hashed secret word entered by the user to the one in the database.
    check_secret_table():
        Checks if the secret word table exists in the database and displays the corresponding GUI.
    show_password():
        Retrieves and shows the password for the selected account.
    config_main_buttons():
        Configures the command functions for the main buttons of the GUI.
    clear_entry():
        Clears the input fields of the main widgets.
    on_closing():
        Closes the database connection and destroys the Tkinter window.
    """

    main_buttons = None
    secret_word_buttons = None

    def __init__(self) -> None:
        """Initializes the Tkinter window and database connection."""
        self.window = Tk()
        self.window.title('Password Manager')
        self.window.config(padx=10, pady=10, bg=BG_COLOR)

        canvas = Canvas(width=200, height=200, bg=BG_COLOR, highlightthickness=0)
        logo_img = PhotoImage(file='img/logo.png')
        canvas.create_image(100, 100, image=logo_img)
        canvas.grid(column=1, row=0)

        self.main_widgets = None

        self.data_base = PasswordManagerDatabase()
        self.check_secret_table()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.window.mainloop()

    def create_main_widgets(self) -> None:
        """Creates the main widgets of the GUI for account and password input."""

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


    def pressed_add_secret_word(self) -> None:
        """Saves the secret word and hint to the database and creates the main widgets."""

        if self.save_secrete_word_and_hint():
            PasswordManager.secret_word_buttons.add_secret_word_button.destroy()
            PasswordManager.secret_word_buttons.add_secret_word_entry.destroy()
            PasswordManager.secret_word_buttons.add_hint_entry.destroy()
            PasswordManager.secret_word_buttons.add_secret_word_label.destroy()
            PasswordManager.secret_word_buttons.add_hint_label.destroy()

            self.create_main_widgets()
        else:
            messagebox.showerror(title='Error', message='Please fill in all fields.')

    def pressed_hint_button(self) -> None:
        """Shows the hint associated with the secret word."""

        hint = self.data_base.select_hint_from_db()
        messagebox.showinfo(message=hint)

    def pressed_add_button(self) -> bool:
        """Saves the account and password to the database if the secret word is correct."""
        account = self.main_widgets.account_entry.get()
        password = self.main_widgets.password_entry.get()

        if len(account) < 1 or len(password) < 1:
            messagebox.showerror(title='Error', message='Please fill in all fields.')
            return False

        if self.is_secret_word_match():
            self.data_base.create_main_table()
            self.data_base.insert_account_and_password(account, password)
            messagebox.showinfo(title='Success',
                                message=('Data has been saved successfully.'))

        self.clear_entry()

        return True

    def pressed_password_button(self) -> None:
        """Generates a random password and inserts it into the password entry."""

        self.main_widgets.password_entry.delete(0, END)
        number = int(self.main_widgets.spinner.get())
        password = PassWord(number).password
        self.main_widgets.password_entry.insert(END, password)


    def save_secrete_word_and_hint(self) -> bool:
        """Hashes and saves the secret word and hint to the database."""

        secret_word_entry = self.secret_word_buttons.add_secret_word_entry.get()
        secret_word = hashlib.sha256(secret_word_entry.encode())
        secret_word = secret_word.hexdigest()
        hint = self.secret_word_buttons.add_hint_entry.get()
        if len(secret_word_entry) < 1 or len(hint) < 1:
            return False

        try:
            self.data_base.create_secret_word_table()
        except errors.InFailedSqlTransaction:
            self.data_base.connect_to_db.rollback()
        finally:
            self.data_base.create_secret_word_table()

        self.data_base.insert_secret_word_and_hint(secret_word, hint)
        messagebox.showinfo(title='Success', message='Data has been saved successfully.')

        return True

    def is_secret_word_match(self) -> bool:
        """Compares the hashed secret word entered by the user to the one in the database."""

        user_secret_word = hashlib.sha256(self.main_widgets.secret_word_entry.get().encode())
        user_secret_word = user_secret_word.hexdigest()
        result = user_secret_word == self.data_base.select_secret_word_from_db()[0][0]
        if result:
            return True
        messagebox.showerror(title='Error', message=('Incorrect secret word!'))
        return False


    def check_secret_table(self) -> None:
        """Checks if the secret word table exists in the database and displays the GUI."""

        self.data_base.start_db_connection()

        if not self.data_base.check_if_secret_table_exists():
            PasswordManager.secret_word_buttons = SecretWordUi(bg_color=BG_COLOR)
            PasswordManager.secret_word_buttons.secret_word_buttons()
            PasswordManager.secret_word_buttons.grid_items()
            add_secret_word_btn = PasswordManager.secret_word_buttons.add_secret_word_button
            add_secret_word_btn.config(command=self.pressed_add_secret_word)
        else:
            self.create_main_widgets()


    def show_password(self) -> None:
        """Retrieves and shows the password for the selected account."""

        if self.is_secret_word_match():
            account_name = self.main_widgets.account_entry.get()
            result = self.data_base.select_password_from_db(account_name)
            if result:
                message = generate_message(result)
                messagebox.showinfo(message=message)
            else:
                messagebox.showerror(message='This account does not exists')

        self.clear_entry()

    def config_main_buttons(self) -> None:
        """Configures the command functions for the main buttons of the GUI."""

        PasswordManager.main_buttons.hint_button.config(command=self.pressed_hint_button)
        search_button = PasswordManager.main_buttons.search_button
        search_button.config(command=self.show_password)
        generate_password_button = PasswordManager.main_buttons.generate_password_button
        generate_password_button.config(command=self.pressed_password_button)
        PasswordManager.main_buttons.add_button.config(command=self.pressed_add_button)


    def clear_entry(self) -> None:
        """Clears the input fields of the main widgets."""

        self.main_widgets.account_entry.delete(0, END)
        self.main_widgets.password_entry.delete(0, END)
        self.main_widgets.secret_word_entry.delete(0, END)

    def on_closing(self) -> None:
        """Closes the database connection and destroys the Tkinter window
        when the user closes the application.
        """

        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.data_base.close_db_connection()
            self.window.destroy()
