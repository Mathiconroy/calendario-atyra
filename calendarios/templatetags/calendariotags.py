from django import template
from django.utils.safestring import mark_safe, SafeString
from django.utils.html import format_html

register = template.Library()

@register.filter
def print_values(value):
    pass

@register.filter
def test0():
    return True

@register.filter(name='render_cell')
def render_cell(arg, value):
    if value in arg[0]:
        return format_html("<td bgcolor='#FF6666'>Reservado por {}</td>", arg[1][arg[0].index(value)])
    else:
        return mark_safe("<td bgcolor='#66FF66'>Libre</td>")