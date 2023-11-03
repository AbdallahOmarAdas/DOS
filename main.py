# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sqlite3

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    conn = sqlite3.connect("my_database.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS book (
                        id INTEGER PRIMARY KEY,
                        title TEXT,
                        catalog TEXT,
                        quantity INTEGER,
                        price INTEGER
                     )''')
    # cursor.execute("INSERT INTO book  VALUES (1,'How to get a good grade in DOS in 40 minutes a day','distributed systems',20,30)")
    # cursor.execute("INSERT INTO book  VALUES (2,'RPCs for Noobs','distributed systems',40,40)")
    # cursor.execute("INSERT INTO book VALUES (3,'Xen and the Art of Surviving Undergraduate School','undergraduate school',30,30)")
    # cursor.execute("INSERT INTO book VALUES (4,'Cooking for the Impatient Undergrad','undergraduate school',40,40)")
    conn.commit()
    cursor.execute("SELECT * FROM book")
    data = cursor.fetchall()
    for row in data:
        print(row)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
