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
        print('Respond overridden')
        messages.success(request, 'Email verification sent. Please check your inbox.', extra_tags='user_alert_important')
        return HttpResponseRedirect('/')
