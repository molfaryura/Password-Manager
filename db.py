"""PostgreSQL database"""

import psycopg2
from psycopg2 import sql

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


class PasswordManagerDatabase():
    def __init__(self) -> None:
        """Connects to the postgresql database"""

        self.connect_to_db = psycopg2.connect(host=DB_HOST,
                                dbname=DB_NAME,
                                user=DB_USER,
                                password=DB_PASSWORD,
                                port=DB_PORT)

        self.db_cursor = self.connect_to_db.cursor()

    def close_db_connection(self) -> None:
        """Closes connection to the database"""

        if self.db_cursor is not None:
            self.db_cursor.close()
            self.db_cursor = None

        if self.connect_to_db is not None:
            self.connect_to_db.close()
            self.connect_to_db = None

    def create_main_table(self) -> None:
        """Creates a table for the user's passwords"""

        self.db_cursor.execute(sql.SQL('''CREATE TABLE IF NOT EXISTS Passwords
                            (id serial PRIMARY KEY, account varchar(255), 
                            password varchar(255))'''))
        self.connect_to_db.commit()


    def create_secret_word_table(self) -> None:
        """Creates a table for the secret word"""

        self.db_cursor.execute(sql.SQL('''CREATE TABLE IF NOT EXISTS SecretWord
                            (id serial PRIMARY KEY,
                            word varchar(255),
                            hint varchar(255))'''))
        self.connect_to_db.commit()

    def insert_secret_word_and_hint(self, secret_word, user_hint) -> None:
        """Insert secret word and a hint into a table

        Args:
            secret_word(str): Secret word to save.
            user_hint(str): Hint for the secret word.
        """
        self.db_cursor.execute('''INSERT INTO SecretWord (word, hint)
                            VALUES (%s, %s) ''',
                            (secret_word, user_hint))
        self.connect_to_db.commit()

    def insert_account_and_password(self, account, password) -> None:
        """Insert account and a password into a table

        Args:
            account (str): The account to save.
            password(str): Password for the account.
        """
        self.db_cursor.execute('''INSERT INTO Passwords (account, password)
                            VALUES (%s, %s) ''',
                            (account, password))
        self.connect_to_db.commit()


    def select_password_from_db(self, account) -> list:
        """Selects a password for the particular account

        Args:
            account (str): The account for which to retrieve password information.

        Returns:
            list: A list of tuples containing the 'account' and 'password' values.
        """

        self.db_cursor.execute('''SELECT account,password
                            FROM Passwords
                            WHERE account=%s''', (account,))
        rows = self.db_cursor.fetchall()
        return rows


    def select_hint_from_db(self) -> list:
        """Selects a hint from the SecretWord table

        Returns:
            list: A list of tuples containing the 'hint' values.
        """

        self.db_cursor.execute(sql.SQL('''SELECT hint FROM SecretWord'''))
        rows = self.db_cursor.fetchall()
        return rows

    def select_secret_word_from_db(self) -> list:
        """Selects a secret word from the SecretWord table

        Returns:
            list: A list of tuples containing the 'word' values.
        """

        self.db_cursor.execute(sql.SQL('''SELECT word FROM SecretWord'''))
        rows = self.db_cursor.fetchall()
        return rows

    def check_if_secret_table_exists(self) -> bool:
        """Returns True if secret_table exists otherwise False"""

        try:
            self.select_hint_from_db()
            return True
        except psycopg2.errors.UndefinedTable:
            return False
