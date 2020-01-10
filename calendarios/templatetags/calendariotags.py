from django import template
from django.utils.safestring import mark_safe, SafeString
from django.utils.html import format_html

register = template.Library()

# arg is a list which contains two lists: the first one has all days ocuppied, the second one has an instance of RESERVAS
# value is the current date we are iterating
@register.filter(name='render_cell')
def render_cell(arg, value):
    if value in arg[0]:
        return format_html("<td bgcolor='#FF6666'>Reservado por {}</td>", arg[1][arg[0].index(value)].nombre)
    else:
        return mark_safe("<td bgcolor='#66FF66'>Libre</td>")