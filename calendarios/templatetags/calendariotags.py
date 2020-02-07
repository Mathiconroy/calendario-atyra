from django import template
from django.utils.safestring import mark_safe, SafeString
from django.utils.html import format_html
from django.template.defaultfilters import date as _date

from ..views import casas 

register = template.Library()

# arg is a list which contains two lists: the first one has all days ocuppied, the second one has an instance of RESERVAS
# value is the current date we are iterating
@register.simple_tag(takes_context=True, name='render_cell')
def render_cell(context, dictionary, fecha):
    request = context['request']
    #print('fecha', fecha, 'dictionary', dictionary[fecha])
    table_row = '' # Construct a string with the html for the table row
    for reserva in dictionary[fecha]:
        if reserva:
            table_row = table_row + format_html("<td class='calendario-row-data' bgcolor='#FF6666'>Reservado por <strong><a href='/view_client_form/{}'>{}</a></strong> ({} personas)</td>",
                reserva.id,
                reserva.nombre,
                reserva.cantidad_personas)
        else:
            table_row = table_row + format_html("<td bgcolor='#66FF66'>Libre</td>")

    return mark_safe(table_row)

    """
    if value == arg[0]:
        if request.user.is_authenticated:
            return format_html("<td class='calendario-row-data' bgcolor='#FF6666'>Reservado por <strong><a href='/view_client_form/{}'>{}</a></strong> ({} personas)</td>",
            arg[1].id,
            arg[1].nombre,
            arg[1].cantidad_personas)
        else:
            return format_html("<td class='calendario-row-data' bgcolor='#FF6666'>Reservado</td>")
    else:
        return mark_safe("<td bgcolor='#66FF66'>Libre</td>")
    """

@register.simple_tag(name='render_confirm')
def render_confirm(dictionary, key): # The dictionary contains submitted ReservaForm values
    correct_names_dict = {
        "fecha_inicio":"Fecha de inicio", 
        "fecha_fin":"Fecha de fin",
        "email":"Email",
        "nombre":"Nombre",
        "casa":"Casa",
        "cantidad_personas":"Cantidad de personas",
        "notas":"Notas",
    }   
    if key == "casa":
        return f"{correct_names_dict[key]}: {casas.get(int(dictionary.get(key)))}"
    elif key == "fecha_fin" or key == "fecha_inicio":
        return f"{correct_names_dict[key]}: {_date(dictionary.get(key))}"
    else:
        return mark_safe("<td bgcolor='#66FF66'>Libre</td>")