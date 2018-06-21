from django import template
from django.conf import settings
from allauth.account.forms import SignupForm
from users.forms import ExtLoginForm

register = template.Library()


@register.simple_tag(name="get_login")
def get_login_form():
    return ExtLoginForm()


@register.simple_tag(name="get_signup")
def get_signup_form():
    return SignupForm()
