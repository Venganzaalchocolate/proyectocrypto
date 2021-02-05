import sqlite3
from sqlite3 import Error
import os


def nom():
    # os.mkdir('wbitconv\data')
    clave=input('¿Que clave te gustaría poner?')  
    ndatos=nombrebase()
    archivo = open('config.py', 'w')
    archivo.write('SECRET_KEY="{}"'.format(clave))
    archivo.write("\nDBFILE='wbitconv/data/{}.db'".format(ndatos))
    archivo.close()
    
    return ndatos

def nombrebase():
    while True:
        ndatos=input('¿Que nombre te gustaría ponerle a tu base de datos?')
                
        if ndatos.isalpha():
            return ndatos.lower()
        else:
            print("Debes escribir una palabra sin números ni carácteres especiales.")
            continue
            

def sql_connection(ndatos):
    try:
        con = sqlite3.connect('wbitconv/data/{}.db'.format(ndatos))
        cursorObj = con.cursor()
        cursorObj.execute("CREATE TABLE IF NOT EXISTS movimientos(id INTEGER, fecha TEXT NOT NULL, hora TEXT NOT NULL, monedafrom TEXT NOT NULL, cantidadfrom	REAL NOT NULL, monedato	TEXT NOT NULL, cantidadto REAL NOT NULL, pu REAL NOT NULL, PRIMARY KEY(id AUTOINCREMENT))")
        con.commit()
    except Error:
        print(Error)

if __name__ == "__main__":
    sql_connection(nom())

