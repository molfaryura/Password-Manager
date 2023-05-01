"""Classes for the main user interface"""

from tkinter import Entry, Spinbox, Button, PhotoImage, Label
from tkinter import messagebox

class MainWidgets:
    def __init__(self) -> None:
        self.secret_word_entry = Entry(width=21)
        self.account_entry = Entry(width=21)
        self.password_entry = Entry(width=21)
        self.spinner = None

    def grid_items(self):
        self.secret_word_entry.grid(column=1, row=1)
        self.secret_word_entry.focus()

        self.account_entry.grid(column=1, row=2, pady=10)
        self.password_entry.grid(column=1, row=3)

    def create_spinner(self, root):
        self.spinner = Spinbox(root, from_=4, to=20, increment=1, width=2)
        self.spinner.grid(column=2, row=3, padx=5)


class Buttons:
    def __init__(self):
        self.hint_button_image = PhotoImage(file='img/hint.png')
        self.hint_button = Button(image=self.hint_button_image, width=32, highlightthickness=0)

        self.search_button_image = PhotoImage(file='img/search_button.png')
        self.search_button = Button(image=self.search_button_image, width=32, highlightthickness=0)

        self.generate_button_image = PhotoImage(file='img/generator.png')
        self.generate_password_button = Button(image=self.generate_button_image, highlightthickness=0)

        self.add_button = None

        self.create_add_button()
        self.grid_items()

    def create_add_button(self, *args):
        self.add_button = Button(text='Save account and password',highlightthickness=0, width=21)
        self.add_button.grid(column=1, row=4, columnspan=1, pady=10)
        

    def grid_items(self):
        self.hint_button.grid(column=2, row=1)
        self.search_button.grid(column=2, row=2)
        self.generate_password_button.grid(column=3, row=3, padx=5)


class SecretWordUi:
    def __init__(self, bg_color) -> None:
        SecretWordUi.show_info()

        self.add_secret_word_entry = Entry(width=21)

        self.add_hint_entry = Entry(width=21)

        self.add_secret_word_label = Label(text='Secret Word:', font=('Arial', 12, 'bold'), bg=bg_color)

        self.add_hint_label = Label(text='Hint:',  font=('Arial', 12, 'bold'), bg=bg_color)

        self.save_image = None
        self.add_secret_word_button = None

    @staticmethod
    def show_info():
        messagebox.showinfo(title='Attention', message=('Please create secret word, hint, and type the icon to start. '))

    def grid_items(self):
        self.add_secret_word_entry.grid(column=1, row=4, pady=10)
        self.add_hint_entry.grid(column=1, row=5)
        self.add_secret_word_label.grid(column=0, row=4)
        self.add_hint_label.grid(column=0, row=5)
        self.add_secret_word_button.grid(column=2, row=4,  pady=10, rowspan=2)

    def secret_word_buttons(self):
        self.save_image = PhotoImage(file='img/save.png')
        self.add_secret_word_button = Button(image=self.save_image, highlightthickness=0)