from django import template

register = template.Library()


@register.filter(name='format_number')
def format_number(value):
    formatted_value = "{:,.2f}".format(value)
    return formatted_value.replace(",", "*").replace(".", ",").replace("*", ".")
