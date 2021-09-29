from django import template
from app.models import User
from django.shortcuts import get_object_or_404

register = template.Library()

@register.filter
def userinfo(id):
    userinfo = get_object_or_404(User, pk=id)
    print(userinfo.profile_image)
    userinfot = {
        'fullname': userinfo.first_name + ' ' + userinfo.last_name,
        'email': userinfo.email,
        'id': id,
        'profile_image': userinfo.profile_image
    }
    return userinfot
