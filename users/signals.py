from allauth.account.signals import user_logged_out
from allauth.account.signals import user_logged_in
from allauth.account.signals import email_confirmation_sent
from django.dispatch import receiver
from django.shortcuts import reverse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages

@receiver(user_logged_out, sender=User)
def notif_logout(sender, request, user, **kwargs):
    messages.success(request, 'You have logged out', extra_tags='user_alert_info')

@receiver(user_logged_in, sender=User)
def notif_login(sender, request, user, **kwargs):
    messages.success(request, 'Successfully logged in', extra_tags='user_alert_info')
