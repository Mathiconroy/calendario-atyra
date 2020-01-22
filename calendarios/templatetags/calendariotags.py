from django import template
from django.utils.safestring import mark_safe, SafeString
from django.utils.html import format_html

register = template.Library()

# arg is a list which contains two lists: the first one has all days ocuppied, the second one has an instance of RESERVAS
# value is the current date we are iterating
@register.simple_tag(takes_context=True, name='render_cell')
def render_cell(context, arg, value):
    request = context['request']
    if value in arg[0]:
        if request.user.is_authenticated:
            return format_html("<td class='calendario-row-data' bgcolor='#FF6666'>Reservado por <strong><a href='/view_client_form/{}'>{}</a></strong> ({} personas)</td>",
            arg[1][arg[0].index(value)].id,
            arg[1][arg[0].index(value)].nombre,
            arg[1][arg[0].index(value)].cantidad_personas)
        else:
            return format_html("<td class='calendario-row-data' bgcolor='#FF6666'>Reservado</td>")
    else:
        return mark_safe("<td bgcolor='#66FF66'>Libre</td>")