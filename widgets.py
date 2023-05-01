"""Classes for the main user interface"""

from tkinter import Entry, Spinbox, Button, PhotoImage, Label
from tkinter import messagebox

class MainWidgets:
    """A class that represents the main widgets used in a password manager application.

    Attributes:
    -----------
    secret_word_entry : tkinter.Entry
        An Entry widget that allows the user to enter a secret word.
    account_entry : tkinter.Entry
        An Entry widget that allows the user to enter an account name.
    password_entry : tkinter.Entry
        An Entry widget that allows the user to enter a password.
    spinner : tkinter.Spinbox
        A Spinbox widget that allows the user to select a password length.

    Methods:
    --------
    grid_items():
        A method that places widgets on a grid.
    create_spinner(root: tkinter.Tk):
        A method that creates a Spinbox widget and places it on a grid.
    """

    def __init__(self) -> None:
        """Initializes a new instance of MainWidgets class."""

        self.secret_word_entry = Entry(width=21)
        self.account_entry = Entry(width=21)
        self.password_entry = Entry(width=21)
        self.spinner = None

    def grid_items(self) -> None:
        """Arranges the GUI widgets in a grid format."""

        self.secret_word_entry.grid(column=1, row=1)
        self.secret_word_entry.focus()

        self.account_entry.grid(column=1, row=2, pady=10)
        self.password_entry.grid(column=1, row=3)

    def create_spinner(self, root) -> None:
        """Creates a spinner widget.

        Args:
            root: The parent window in which the spinner widget is created
        """

        self.spinner = Spinbox(root, from_=4, to=20, increment=1, width=2)
        self.spinner.grid(column=2, row=3, padx=5)


class Buttons:
    """A class to represent the buttons in the password manager GUI.

    Attributes:
    -----------
    hint_button_image: tkinter.PhotoImage
        The image of the hint button.
    hint_button: tkinter.Button
        The hint button.
    search_button_image: tkinter.PhotoImage
        The image of the search button.
    search_button: tkinter.Button
        The search button.
    generate_button_image: tkinter.PhotoImage
        The image of the generate password button.
    generate_password_button: tkinter.Button
        The generate password button.
    add_button: tkinter.Button
        The button to save account and password.

    Methods:
    -----------
    create_add_button():
        Creates the 'save account and password' button.
    grid_items():
        Places the buttons in the correct positions on the grid.
    """

    def __init__(self):
        """Initializes Buttons with images and buttons."""

        self.hint_button_image = PhotoImage(file='img/hint.png')
        self.hint_button = Button(image=self.hint_button_image, width=32, highlightthickness=0)

        self.search_button_image = PhotoImage(file='img/search_button.png')
        self.search_button = Button(image=self.search_button_image, width=32, highlightthickness=0)

        self.generate_button_image = PhotoImage(file='img/generator.png')
        self.generate_password_button = Button(image=self.generate_button_image,
                                               highlightthickness=0)

        self.add_button = None

        self.create_add_button()
        self.grid_items()

    def create_add_button(self):
        """Creates the 'save account and password' button."""

        self.add_button = Button(text='Save account and password',highlightthickness=0, width=21)
        self.add_button.grid(column=1, row=4, columnspan=1, pady=10)


    def grid_items(self):
        """Places the buttons in the correct positions on the grid."""

        self.hint_button.grid(column=2, row=1)
        self.search_button.grid(column=2, row=2)
        self.generate_password_button.grid(column=3, row=3, padx=5)


class SecretWordUi:
    """A class for creating the user interface for adding a secret word and hint.

    Attributes:
    -----------
    bg_color: str
        The background color of the user interface.
    add_secret_word_entry: tkinter.Entry
        An entry widget for typing in the secret word.
    add_hint_entry: tkinter.Entry
        An entry widget for typing in the hint for the secret word.
    add_secret_word_label: tkinter.Label
        A label for the secret word entry widget.
    add_hint_label: tkinter.Label
        A label for the hint entry widget.
    save_image: tkinter.PhotoImage
        An image for the save button widget.
    add_secret_word_button: tkinter.Button
        A button widget for saving the secret word and hint.

    Methods:
    -----------
    show_info():
        Displays a messagebox with instructions for creating a secret word and hint.
    grid_items():
        Grids the user interface widgets on the screen.
    secret_word_buttons():
        Creates and grids the save button widget.
    """

    def __init__(self, bg_color) -> None:
        """Initializes a new instance of the SecretWordUi class.

        Parameters:
            bg_color (str): The background color of the user interface.
        """

        SecretWordUi.show_info()

        self.add_secret_word_entry = Entry(width=21)

        self.add_hint_entry = Entry(width=21)

        self.add_secret_word_label = Label(text='Secret Word:', font=('Arial', 12, 'bold'),
                                           bg=bg_color)

        self.add_hint_label = Label(text='Hint:',  font=('Arial', 12, 'bold'), bg=bg_color)

        self.save_image = None
        self.add_secret_word_button = None

    @staticmethod
    def show_info():
        """Displays a messagebox with instructions for creating a secret word and hint."""

        messagebox.showinfo(title='Attention',
                            message=('Create secret word, hint, and type the icon to start. '))

    def grid_items(self):
        """Places the buttons in the correct positions on the grid."""

        self.add_secret_word_entry.grid(column=1, row=4, pady=10)
        self.add_hint_entry.grid(column=1, row=5)
        self.add_secret_word_label.grid(column=0, row=4)
        self.add_hint_label.grid(column=0, row=5)
        self.add_secret_word_button.grid(column=2, row=4,  pady=10, rowspan=2)

    def secret_word_buttons(self):
        """Creates and grids the save button widget."""

        self.save_image = PhotoImage(file='img/save.png')
        self.add_secret_word_button = Button(image=self.save_image, highlightthickness=0)
