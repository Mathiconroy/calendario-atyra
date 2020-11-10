from django import template
from django.utils.safestring import mark_safe, SafeString
from django.utils.html import format_html
from django.template.defaultfilters import date as _date

from ..views import casas, tipos_adelanto

register = template.Library()

@register.simple_tag(name='get_casa_display')
def get_casa(value):
    return casas[value]

# Dictionary is a dictionary that has as keys a date object and as values a list with Reserva object or None
# fecha is the date object we currently are (goes from today up to x days after, depending on what the value of days_to_count in views.py is)
@register.simple_tag(takes_context=True, name='render_row')
def render_row(context, dictionary, fecha):
    """Look up the dictionary with the given date and make a string of html to render the table row"""
    request = context['request']
    table_row = ''
    red_hex_value = "#FF6666"
    green_hex_value = "#66FF66"
    yellow_hex_value = "#FFFF66"
    for reserva in dictionary[fecha]:
        if reserva:
            if reserva.estado == 0:
                color = yellow_hex_value
                if request.user.is_authenticated:
                    text = "Reserva pedida por"
                else:
                    text = "Reserva sin confirmar"
            else:
                color = red_hex_value
                if request.user.is_authenticated:
                    text = "Reservado por"
                else:
                    text = "Reservado"
            if request.user.is_authenticated:
                table_row = table_row + format_html("<td class='calendario-row-data' bgcolor={}>{} <strong><a href='/view_client_form/{}'>{}</a></strong> ({} personas)</td>",
                    color,
                    text,
                    reserva.id,
                    reserva.nombre,
                    reserva.cantidad_adultos + reserva.cantidad_menores + reserva.cantidad_gratis
                )
            else:
                table_row = table_row + format_html("<td class='calendario-row-data' bgcolor={}>{}</td>",
                    color,
                    text,
                )
        else:
            color = green_hex_value
            table_row = table_row + format_html("<td bgcolor={}>Libre</td>", color)

    return mark_safe(table_row)

@register.simple_tag(name='render_date')
def render_date(date):
    if date.weekday() == 6 or date.weekday() == 5:
        return mark_safe(format_html("<td><b>{}</b></td>", _date(date)))
    else:
        return mark_safe(format_html("<td>{}</td>", _date(date)))

@register.simple_tag(name='render_confirm')
def render_confirm(dictionary, key): # The dictionary contains submitted ReservaForm values
    correct_names_dict = {
        "fecha_inicio":"Fecha de inicio", 
        "fecha_fin":"Fecha de fin",
        "email":"Email",
        "nombre":"Nombre",
        "casa":"Casa",
        "cantidad_adultos":"Cantidad de adultos",
        "cantidad_menores":"Cantidad de menores",
        "cantidad_gratis":"Cantidad de gratis",
        "tipo_adelanto": "Medio de seña",
        "notas":"Notas",
    }
    if key == "casa":
        return f"{correct_names_dict[key]}: {casas.get(int(dictionary.get(key)))}"
    elif key == "tipo_adelanto":
        return f"{correct_names_dict[key]}: {tipos_adelanto.get(int(dictionary.get(key)))}"
    elif key == "fecha_fin" or key == "fecha_inicio":
        return f"{correct_names_dict[key]}: {_date(dictionary.get(key))}"
    else:
        return f"{correct_names_dict[key]}: {dictionary.get(key)}"