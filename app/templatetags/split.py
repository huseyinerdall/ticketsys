from django import template

register = template.Library()

@register.filter
def split(data,deli=','):
    splited_data = data.split(deli)
    return splited_data