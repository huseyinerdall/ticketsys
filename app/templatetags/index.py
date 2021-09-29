from django import template

register = template.Library()

@register.filter
def index(list, i):
    i = int(i)
    return list[i]