from django import template

register = template.Library()

@register.filter
def filename(data):
    name = data.get_filename()
    return name
