"""Secure password generator"""

import re

import string

import secrets

SYMBOLS = string.printable[:-5]


class PassWord:
    """A class that generates and validates strong passwords.

    Attributes:
    - password: a string representing the generated password

    Methods:
    - __init__(self, length): constructs a PassWord instance
    - generate_password(self, length): generates a password of the specified length
    - is_password_valid(self, password): checks if the specified password meets the requirements
    - set_password(self, length): sets the password attribute to a generated password
    """

    def __init__(self, length) -> None:
        """Constructs a PassWord instance.

        Parameters:
        - length(int): represents the desired length of the password
        """

        self.password = None
        self.set_password(length)

    @staticmethod
    def generate_password(length) -> str:
        """Generates a password of the specified length using a secure random generator.

        Parameters:
        - length(int): represents the desired length of the password
        """

        passw_chars = (secrets.choice(SYMBOLS) for _ in range(length))
        return "".join(passw_chars)

    @staticmethod
    def is_password_valid(password) -> bool:
        """Checks if the specified password meets the minimum strength requirements.

        Parameters:
        - password(str): represents the password to be checked
        """

        re_pattern = r'^(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])'
        return re.match(pattern=re_pattern, string=password)

    def set_password(self, length) -> None:
        """Sets the password attribute to a generated password.

        Parameters:
        - length(int): represents the desired length of the password
        """

        while not self.password:
            password = PassWord.generate_password(length)
            if PassWord.is_password_valid(password):
                self.password = password
