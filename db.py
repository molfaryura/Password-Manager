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
                        secret_word varchar(255),
                        hint varchar(255))'''))
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
