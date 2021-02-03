from wbitconv import app, api
import sqlite3
import time
import datetime

DBFILE = app.config['DBFILE'] 


def enchufe(query, params=()):
    conn = sqlite3.connect(DBFILE) #conectamos con la base de datos
    c = conn.cursor() # creamos el cursor

    c.execute(query, params) 
    conn.commit()

    filas = c.fetchall()
    conn.close()
    listaDeDiccionarios=consulta(filas,c)
    return listaDeDiccionarios

def consulta(filas,c):
    if len(filas) == 0:
        return filas

    columnNames = []
    for columnName in c.description:
        columnNames.append(columnName[0])

    listaDeDiccionarios = []

    for fila in filas:
        d = {}
        for ix, columnName in enumerate(columnNames):
            d[columnName] = fila[ix]
        listaDeDiccionarios.append(d)

    return listaDeDiccionarios

def hora():
    hora=time.strftime("%X")
    return hora

def fecha():
    fecha=datetime.date.today()
    return fecha

def listaMonedas(lista):
    listamonedas=[]
    for clave, valor in lista.items():
        if valor > 0:
            listamonedas.append(clave)
    if not 'EUR' in listamonedas:
        listamonedas.append('EUR')
    return listamonedas

def totales(totales):
    diccionariototales={}

    for a in totales:
        clave=a.get('monedato')
        valor=a.get('cantidadto')
        
        claveE=a.get('monedafrom')
        valorE=a.get('cantidadfrom')
        
        if diccionariototales.get(clave) == None:
            diccionariototales[clave] = valor
        else:
            diccionariototales[clave] = valor + diccionariototales[clave]
            
        if diccionariototales.get(claveE) == None:
            diccionariototales[claveE] = - valorE
        else:
            diccionariototales[claveE] =  diccionariototales[claveE] - valorE
    
    return diccionariototales

def bitcoins(dic):
        tot=0
        for clave, valor in dic.items():
            if clave != 'EUR' and valor>0:
                monedato='EUR'
                invertir= api.convertir(clave,monedato,valor)
                tot+=invertir
        
        return tot 

def euros(dic):
    if dic != {}:
        for clave, valor in dic.items():
            if clave == 'EUR':
                return valor
    else:
        return 0 
        
def criptos(dic, key):
    for clave, valor in dic.items():
        if clave == key:
            return valor 

def eurosinvertidos(dic):
    total=0
    for a in dic:
        claveE=a.get('monedafrom')
        valorE=a.get('cantidadfrom')
        if claveE=='EUR':
            total+=valorE
    return total

