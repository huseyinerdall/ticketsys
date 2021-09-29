from django import template

register = template.Library()

@register.filter
def fileext(data):
    name = data.get_ext()
    return name
