import sqlite3
from sqlite3 import Error

def sql_connection():
    try:
        con = sqlite3.connect('wbitconv/data/basededatos.db')
        return con
    except Error:
        print(Error)

def sql_table(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE IF NOT EXISTS movimientos(id INTEGER, fecha TEXT NOT NULL, hora TEXT NOT NULL, monedafrom TEXT NOT NULL, cantidadfrom	REAL NOT NULL, monedato	TEXT NOT NULL, cantidadto REAL NOT NULL, pu REAL NOT NULL, PRIMARY KEY(id AUTOINCREMENT))")
    con.commit()


if __name__ == "__main__":
    con = sql_connection()
    sql_table(con)

