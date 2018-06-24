from django.conf import settings
from django.utils import timezone
import time
from django.core.cache import cache
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, resolve_url, redirect
from allauth.account.adapter import DefaultAccountAdapter


class ExtAccountAdapter(DefaultAccountAdapter):

    # Email Verification Sent Redirect to HomePage
    def respond_email_verification_sent(self, request, user):
        messages.success(request, 'Email verification sent. Please check your inbox.',
                         extra_tags='user_alert_important')
        return HttpResponseRedirect('/')

    # Added emails are automatically set to primary
    def confirm_email(self, request, email_address):
        email_address.verified = True
        email_address.set_as_primary()
        email_address.save()
