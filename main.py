"""GUI Password Manager"""

from tkinter import *
from tkinter import messagebox

from db import close_db_connection

BG_COLOR = '#669170'

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        close_db_connection()
        window.destroy()

window = Tk()
window.title('Password Manager')
window.config(padx=10, pady=10, bg=BG_COLOR)

canvas = Canvas(width=200, height=200, bg=BG_COLOR, highlightthickness=0)
logo_img = PhotoImage(file='img/logo.png')
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

secret_word_label = Label(text='Secret Word:', bg=BG_COLOR, font=('Arial', 12, 'bold'))
secret_word_label.grid(column=0, row=1)

secret_word_entry = Entry(width=21)
secret_word_entry.grid(column=1, row=1)
secret_word_entry.focus()

hint_button_image = PhotoImage(file='img/hint.png')
hint_button = Button(image=hint_button_image, width=32, bg=BG_COLOR, highlightthickness=0)
hint_button.grid(column=2, row=1)

account_label = Label(text='Account:', bg=BG_COLOR, font=('Arial', 12, 'bold'))
account_label.grid(column=0, row=2)

account_entry = Entry(width=21)
account_entry.grid(column=1, row=2, pady=10)

search_button_image = PhotoImage(file='img/search_button.png')
search_button = Button(image=search_button_image, width=32, bg=BG_COLOR, highlightthickness=0)
search_button.grid(column=2, row=2)

password_label = Label(text='Password:', bg=BG_COLOR, font=('Arial', 12, 'bold'))
password_label.grid(column=0, row=3)

password_entry = Entry(width=21)
password_entry.grid(column=1, row=3)

generate_button_image = PhotoImage(file='img/generator.png')
generate_password_button = Button(image=generate_button_image, bg=BG_COLOR, highlightthickness=0)
generate_password_button.grid(column=3, row=3, padx=5)

spinner = Spinbox(window, from_=4, to=30, increment=1, width=2)
spinner.grid(column=2, row=3, padx=5)

add_button = Button(text='Save account and password',highlightthickness=0, width=21)
add_button.grid(column=1, row=4, columnspan=1, pady=10)

window.protocol("WM_DELETE_WINDOW", on_closing)


if __name__ == '__main__':
    window.mainloop()
