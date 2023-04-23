"""GUI Password Manager"""

from tkinter import *
from tkinter import messagebox

from db import close_db_connection, create_secret_word_table, connect_to_db
from db import check_if_secret_table_exists, insert_secret_word_and_hint

BG_COLOR = '#669170'

class PasswordManager():

    def __init__(self) -> None:
        self.window = Tk()
        self.window.title('Password Manager')
        self.window.config(padx=10, pady=10, bg=BG_COLOR)

        self.canvas = Canvas(width=200, height=200, bg=BG_COLOR, highlightthickness=0)
        logo_img = PhotoImage(file='img/logo.png')
        self.canvas.create_image(100, 100, image=logo_img)
        self.canvas.grid(column=1, row=0)

        self.check_secret_table()
        connect_to_db()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.window.mainloop()

    def create_main_widgets(self):
        self.secret_word_label = Label(text='Secret Word:', bg=BG_COLOR, font=('Arial', 12, 'bold'))
        self.secret_word_label.grid(column=0, row=1)

        self.secret_word_entry = Entry(width=21)
        self.secret_word_entry.grid(column=1, row=1)
        self.secret_word_entry.focus()

        self.hint_button_image = PhotoImage(file='img/hint.png')
        self.hint_button = Button(image=self.hint_button_image, width=32, bg=BG_COLOR, highlightthickness=0)
        self.hint_button.grid(column=2, row=1)

        self.account_label = Label(text='Account:', bg=BG_COLOR, font=('Arial', 12, 'bold'))
        self.account_label.grid(column=0, row=2)

        self.account_entry = Entry(width=21)
        self.account_entry.grid(column=1, row=2, pady=10)

        self.search_button_image = PhotoImage(file='img/search_button.png')
        self.search_button = Button(image=self.search_button_image, width=32, bg=BG_COLOR, highlightthickness=0)
        self.search_button.grid(column=2, row=2)

        self.password_label = Label(text='Password:', bg=BG_COLOR, font=('Arial', 12, 'bold'))
        self.password_label.grid(column=0, row=3)

        self.password_entry = Entry(width=21)
        self.password_entry.grid(column=1, row=3)

        self.generate_button_image = PhotoImage(file='img/generator.png')
        self.generate_password_button = Button(image=self.generate_button_image, bg=BG_COLOR, highlightthickness=0)
        self.generate_password_button.grid(column=3, row=3, padx=5)

        self.spinner = Spinbox(self.window, from_=4, to=30, increment=1, width=2)
        self.spinner.grid(column=2, row=3, padx=5)

        self.add_button = Button(text='Save account and password',highlightthickness=0, width=21)
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

    def save_secrete_word_and_hint(self):
        self.secret_word = self.add_hint_entry.get()
        self.hint = self.add_hint_entry.get()
        create_secret_word_table()
        insert_secret_word_and_hint(self.secret_word, self.hint)


    def check_secret_table(self):
        if not check_if_secret_table_exists():
            self.create_secret_word()
        else:
            self.create_main_widgets()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            close_db_connection()
            self.window.destroy()
