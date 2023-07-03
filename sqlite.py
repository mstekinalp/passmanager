import sqlite3
from sqlite3 import Error
from datetime import datetime


# Reference https://docs.python.org/3/library/sqlite3.html

def create_connection(user_name):
    """ Create a database connection to a SQLite db """
    conn = None
    bd_path = f"db/{user_name}.db"
    # I will add a check if user exists later
    try:
        conn = sqlite3.connect(bd_path)
        print("Connection has been established!")
        return conn
    except Error as e:
        print(e)
    return conn


def create_table(conn):
    cur = conn.cursor()
    try:
        res = cur.execute(f"CREATE TABLE IF NOT EXISTS user_info(website TEXT NOT NULL,email TEXT NOT NULL, password "
                          f"TEXT NOT NULL, date TEXT NOT NULL)")
        conn.commit()
        print("Entry has successfully been created")
    except Error as e:
        if e == "table user_info already exists":
            print("You already have an entry press space to see your entries!")
        else:
            print(e)


def read_table(conn):
    cur = conn.cursor()
    try:
        res = cur.execute(f"SELECT * FROM user_info")
        rows = res.fetchall()
        for row in rows:
            print(row)

    except Error as e:
        print(e)


def data_entry(conn, web, email, pas):
    cur = conn.cursor()
    # do something
    if 'http' in web:
        web = web.split('/')[2]

    # if '@' in email:
    #     new_email = email.replace('@', '%@').replace('.', '..')
    #     print(new_email)
    # else:
    #     new_email = email
    try:
        create_table(conn)
        sql = """INSERT INTO user_info (website,email,password,date) VALUES (?,?,?,datetime('now', 'localtime'))"""
        data = (web, email, pas)
        cur.execute(sql, data)
        conn.commit()
        print("Data has been added to the db")
    except Error as e:
        print(e)
    finally:
        conn.close()


def delete_entry():
    pass
