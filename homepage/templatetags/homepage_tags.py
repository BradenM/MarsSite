from django import template
from django.shortcuts import HttpResponseRedirect, redirect, reverse
from django.contrib import messages

register = template.Library()

@register.simple_tag
def bad_login(request):
    messages.success(request, 'Incorrect email/password, please try again.', extra_tags='user_alert_error')
    return None