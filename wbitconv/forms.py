from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Length, NumberRange

# El objeto form nos ofrece algunos atributos y métodos para su gestión:

    # form.validate_on_submit(): Nos permite comprobar si el formulario ha sido enviado y es válido.
    # form.data: Nos ofrece un diccionario con los datos del formulario.
    # form.errors: Si el formulario no es válido nos devuelve un diccionario con los errores.
    # form.num1.data: Para cada campo (en este ejemplo num1)`nos devuelve su valor.
    # form.num1.errors: Es una tupla con los errores de validación de el campo determinado.
    # form.num1(): Nos devuelve el código HTML para generar este campo.
    # form.num1.label(): Nos devuelve el código HTML para general la etiqueta del campo.
def ValidandoIguales(form, field):
    if form.monedafrom.data == form.monedato.data:
        raise ValidationError('Las monedas no deben ser iguales')


monedas=['EUR', 'ETH', 'LTC', 'BNB', 'EOS', 'XLM', 'TRX', 'BTC', 'XRP', 'BCH', 'USDT', 'BSV', 'ADA']
monedas.sort()

class FormMovimientos(FlaskForm):
    monedafrom = SelectField('Con', validators=[DataRequired(), ValidandoIguales])
    monedafromoculto= HiddenField()
    monedato = SelectField('Comprar', choices=monedas, validators=[DataRequired()])
    monedatooculto= HiddenField()
    cantidadfrom = FloatField('Cantidad', validators=[DataRequired(), NumberRange(min=0.00001, max=1000000, message='cantidad mínima: 0,1, cantidad máxima: 1000000')])
    cantidadfromoculto = HiddenField()
    cantidadto = HiddenField ()
    preciounitario = HiddenField ()
    
    insertar = SubmitField('INVERTIR')
    calc =SubmitField('CALCULAR')
    

    