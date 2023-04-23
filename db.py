"""PostgreSQL database"""

import psycopg2
from psycopg2 import sql

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

CUR = None
CONN = None

def connect_to_db():
    """Connects to the postgresql database

    Returns: None
    """

    global CUR, CONN

    CONN = psycopg2.connect(host=DB_HOST,
                            dbname=DB_NAME,
                            user=DB_USER,
                            password=DB_PASSWORD,
                            port=DB_PORT)

    CUR = CONN.cursor()

def close_db_connection():
    """Closes connection to the database

    Returns: None
    """

    global CONN, CUR

    if CUR is not None:
        CUR.close()
        CUR = None

    if CONN is not None:
        CONN.close()
        CONN = None

def create_main_table():
    """Creates a table for the user's passwords

    Returns: None
    """

    CUR.execute(sql.SQL('''CREATE TABLE IF NOT EXISTS Passwords
                        (id serial PRIMARY KEY, account varchar(255), 
                        password varchar(255))'''))
    CONN.commit()


def create_secret_word_table():
    """Creates a table for the secret word

    Returns: None
    """

    CUR.execute(sql.SQL('''CREATE TABLE IF NOT EXISTS SecretWord
                        (id serial PRIMARY KEY,
                        word varchar(255),
                        hint varchar(255))'''))
    CONN.commit()

def insert_secret_word_and_hint(secret_word, user_hint):
    """Insert secret word and a hint into a table
    
    Args:
        secret_word(str): Secret word to save.
        user_hint(str): Hint for the secret word.

    Returns: None
    """
    CUR.execute('''INSERT INTO SecretWord (word, hint)
                           VALUES (%s, %s) ''',
                           (secret_word, user_hint))
    CONN.commit()

def insert_account_and_password(account, password):
    """Insert account and a password into a table

    Args:
        account (str): The account to save.
        password(str): Password for the account.

    Returns: None
    """
    CUR.execute('''INSERT INTO Passwords (account, password)
                           VALUES (%s, %s) ''',
                           (account, password))
    CONN.commit()


def select_password_from_db(account):
    """Selects a password for the particular account

    Args:
        account (str): The account for which to retrieve password information.

    Returns:
        list: A list of tuples containing the 'account' and 'password' values for the given account.
    """

    CUR.execute(sql.SQL('''SELECT account,password
                        FROM Passwords
                        WHERE account={}''').format(sql.Identifier(account)))
    rows = CUR.fetchall()
    return rows


def select_hint_from_db():
    """Selects a hint from the SecretWord table

    Returns:
        list: A list of tuples containing the 'hint' values.
    """

    CUR.execute(sql.SQL('''SELECT hint FROM SecretWord'''))
    rows = CUR.fetchall()
    return rows

def select_secret_word_from_db():
    """Selects a secret word from the SecretWord table

    Returns:
        list: A list of tuples containing the 'word' values.
    """

    CUR.execute(sql.SQL('''SELECT word FROM SecretWord'''))
    rows = CUR.fetchall()
    return rows

def check_if_secret_table_exists():
    try:
        connect_to_db()
        select_hint_from_db()
        return True
    except psycopg2.errors.UndefinedTable:
        return False
