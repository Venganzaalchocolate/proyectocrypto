from wbitconv import app, funciones, api
from wbitconv.forms import FormMovimientos
from flask import render_template, request, url_for, redirect # se utiliza para generar resultados a partir de un archivo de plantilla basado en el motor Jinja2 que se encuentra en la carpeta de plantillas de la aplicación. 
import sqlite3

DBFILE = app.config['DBFILE'] 

@app.route('/')
     
def movimientos(): # Función que llama a la plantilla movimientos y los muestra en pantalla
    mensajes=[]
    try:
        ingresos = funciones.enchufe('SELECT fecha, hora, monedafrom, cantidadfrom, monedato, cantidadto, pu, id FROM movimientos;') #Llamamos a la función enchufe para que haga la consulta
        return render_template("movimientos.html", datos=ingresos, title="Todos los movimientos") #Devolvemos la consulta con su template, dandole a jinja los datos necesarios.
    
    except Exception as e:
        print("**ERROR**🔧: Acceso a base de datos - movimientos: {} - {}". format(type(e).__name__, e))
        mensajes.append("Error en acceso a base de datos. Consulte con el administrador.")
        return render_template("movimientos.html", datos=[], title="Todos los movimientos", mensajes=mensajes)

@app.route('/purchase', methods=['GET', 'POST'])

    # mostrará un formulario para comprar
        #   moneda(from)
        #   moneda(to)
        #   cantidad
                #   calculador(coinmarketcap: total de moneda(to) que se puede conseguir con la cantidad puesta)
                    #   Mostrar cantidad
                    #   Mostrara cantidad(moneda(to))       
        #   botón guardar (tabla MOVEMENTS)
        
def transaccion():# creamos la funcion transacción que servirá para: compra, venta o intercambio de moneda
    form=FormMovimientos() # form es el formulario que he creado que se encuentra en forms.py
    fecha=funciones.fecha() # cojo la fecha de python a través de una función sencilla
    hora=funciones.hora() # cojo la hora de python a través de una función sencilla
    mensajes=[] # Campo vacío donde se almacenará el 'Mensaje de error' que se mostrará si ocurre algo
    
    try:
        monedasDisponibles = funciones.listaMonedas(funciones.totales(funciones.enchufe('SELECT monedafrom, cantidadfrom, monedato, cantidadto, id FROM movimientos;')))
        # monedasDisponibles es una lista de monedas de la base de datos, para ello he realizado una consulta con funciones.enchufe(SELECT..) y después he procesado la inf con una función para extraer los datos y que se muestren de una forma correcta. 
    except Exception as e:
        print("**ERROR**🔧: Acceso a base de datos - monedasDiscponibles: {} - {}". format(type(e).__name__, e))
        mensajes.append("Error en acceso a base de datos. Consulte con el administrador.")
        return render_template('invertir.html', form=form, mensajes=mensajes, oculto=False)

    form.monedafrom.choices=monedasDisponibles #asigno el "choices".monedafrom del formulario a monedasDisponibles
    

    if request.method == 'POST': # si es un 'POST' (es decir, enviar datos al servidor) hará lo siguiente:    
        if form.validate(): # aquí comprueba si es valido
        
            if form.calc.data: # si se aprieta el botón calcular
                
                try: # si la consulta a la base de datos va bien
                    criptos = funciones.totales(funciones.enchufe('SELECT monedafrom, cantidadfrom, monedato, cantidadto, id FROM movimientos;'))
                except Exception as e: # si la consulta a la base de datos va mal
                    print("**ERROR**🔧: Acceso a base de datos - criptos: {} - {}". format(type(e).__name__, e)) # Esto es para los programadores
                    mensajes.append("Error en acceso a base de datos. Consulte con el administrador.") # Este mensaje es para el cliente
                    return render_template("invertir.html", form=form, mensajes=mensajes) # Devolvemos el template con el mensaje

                totalcripto = funciones.criptos(criptos, form.monedafrom.data) # calculamos el total de monedafrom disponible
                if form.monedafrom.data != 'EUR' and form.cantidadfrom.data > totalcripto: # nos aseguramos que el cliente no exceda la cuantia (excepto si son EUR)
                    mensajes.append('La cantidad máxima a invertir es {}'.format(totalcripto))
                    return render_template("invertir.html", form=form, mensajes=mensajes) # si excede la cuantia devolvemos el render template con el mensaje
                
                if form.monedafrom.data != form.monedato.data and (totalcripto is None or (form.cantidadfrom.data<=totalcripto or form.monedafrom.data=='EUR')) :
                    try:
                        conversion = api.convertir(
                            form.monedafrom.data,
                            form.monedato.data,
                            form.cantidadfrom.data,
                        )
                        form.cantidadto.data = conversion
                        form.monedafromoculto.data = form.monedafrom.data
                        form.monedatooculto.data = form.monedato.data
                        form.cantidadfromoculto.data = form.cantidadfrom.data
                        form.preciounitario.data = round(form.cantidadto.data /  form.cantidadfrom.data, 5)
    
                        return render_template("invertir.html", oculto=True, form=form )
                    
                    except Exception as e:
                        print("**ERROR**🔧: Acceso a base de datos - Api: {} - {}". format(type(e).__name__, e))
                        mensajes.append("Error en acceso a Api. Consulte con el administrador o inténtelo más tarde.")
                        return render_template("invertir.html", form=form, mensajes=mensajes) 
                
                else:
                    return render_template("invertir.html", form=form )
            
            if form.insertar.data: # si aprieta el botón aceptar
                try:
                    funciones.enchufe ('INSERT INTO movimientos (fecha, hora, monedafrom, monedato, cantidadfrom, cantidadto, pu) VALUES (?, ?, ?, ?,?,?,?);',
                            (
                                fecha,
                                hora,
                                form.monedafromoculto.data,
                                form.monedatooculto.data,
                                form.cantidadfromoculto.data,
                                form.cantidadto.data,
                                form.preciounitario.data
                            )
                    )

                    return redirect(url_for('movimientos')) # te devuelve a movimientos
                
                except Exception as e:
                    print("**ERROR**🔧: Acceso a base de datos - insertar datos: {} - {}". format(type(e).__name__, e))
                    mensajes.append("Error en acceso a base de datos. Consulte con el administrador.")
                    return render_template("invertir.html", form=form, mensajes=mensajes) 
                
            else: # si no lo és te redigirá al formulario otra vez
                    return render_template("invertir.html", form=form, mensajes=mensajes) 
            

    return render_template("invertir.html", oculto=False , form=form ) #calc=False# te mostrará la plantilla del formulario
        
@app.route('/status')
    
def total():
    mensajes=[]
    try:
        dic = funciones.enchufe('SELECT monedafrom, cantidadfrom, monedato, cantidadto, id FROM movimientos;') #Llamamos a la función enchufe para que haga la consulta
    except Exception as e:
        print("**ERROR**🔧: Acceso a base de datos - totales: {} - {}". format(type(e).__name__, e))
        mensajes.append("Error en acceso a base de datos. Consulte con el administrador.")
        return render_template("estado.html", mensajes=mensajes, valoractual=0, eurosinvertidos= 0, ganancias= 0) 
    
    totales=funciones.totales(dic)
    try:
        bitcoins = funciones.bitcoins(funciones.totales(dic))
         
    except Exception as e:
        print("**ERROR**🔧: Acceso a API - bitcoins: {} - {}". format(type(e).__name__, e))
        mensajes.append("Error en acceso a Api. Consulte con el administrador o inténtelo más tarde.")
        return render_template("estado.html", mensajes=mensajes, valoractual=0, eurosinvertidos= 0, ganancias= 0)
    
    euros = funciones.euros(funciones.totales(dic))
    eurosinvertidos = funciones.eurosinvertidos(dic)
    valoractual = bitcoins + euros + eurosinvertidos
    ganancias= round(valoractual - eurosinvertidos, 5)
    return render_template("estado.html", valoractual = valoractual, eurosinvertidos=eurosinvertidos, ganancias=ganancias, title="Todos los movimientos")  
        