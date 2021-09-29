from django import template
import json

register = template.Library()

@register.filter
def loadjson(data):
    try:
        json_data = json.loads(data)
    except:
        json_data = []
    return json_data
