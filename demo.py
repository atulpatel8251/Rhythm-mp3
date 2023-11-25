import sqlite3
#cx_Oracle.init_oracle_client(lib_dir=r"F:\instantclient-basic-windows.x64-11.2.0.4.0")
import traceback
conn=None
try:
    conn=sqlite3.connect("mouzikka/music@127.0.0.1/xe")
    print("connected successfully two the DB")
    print("DB User:",conn.username)
except sqlite3.DatabaseError:
    print("DB Error")
    print(traceback.format_exc())
finally:
    if conn is not None:
        conn.close()
        print("disconnected suceesfully from the DB")

