import sqlite3
import time
import datetime
import random


conn = sqlite3.connect('stonkdata.db')
c = conn.cursor()  # c is cursor


def create_table():
    c.execute(
        'CREATE TABLE IF NOT EXISTS stonkdata(unix REAL, datestamp TEXT, keyword TEXT, value REAL)')


def data_entry():
    c.execute(
        "INSERT INTO stonkdata VALUES(155123452, '2016-01-02', 'Python', 8)")
    conn.commit()
    c.close()
    conn.close()


def dynamic_data_entry():
    unix = time.time()
    date = str(datetime.datetime.fromtimestamp(
        unix).strftime('%Y-%m-%d %H:%M:%S'))
    keyword = 'Python'
    value = random.randrange(0, 10)
    c.execute("INSERT INTO stonkdata (unix, datestamp, keyword, value) VALUES (?, ?, ?, ?)",
              (unix, date, keyword, value))
    conn.commit()


create_table()
# data_entry()

for i in range(10):
    dynamic_data_entry()
    time.sleep(1)
c.close()
conn.close()
