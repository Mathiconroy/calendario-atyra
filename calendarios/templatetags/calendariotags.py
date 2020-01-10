from django import template

register = template.Library()

@register.filter
def print_values(value):
    pass

@register.filter
def test0():
    return True

@register.filter(is_safe=True)
def render_cell(arg, value):
    if value in arg[0]: # TODO: Make the colors!
        return f"Ocupado por {arg[1][arg[0].index(value)]}"
    else:
        return "Libre"