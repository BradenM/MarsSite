from django.shortcuts import render
from allauth.account.views import SignupView, LoginView
from django.shortcuts import HttpResponseRedirect, reverse
from django.contrib import messages
from allauth.account.forms import SignupForm

# Override invalid form on Signup
class ExtSignupView(SignupView):

    def form_invalid(self, form):
        self.request.session['invalid_signup'] = self.request.POST
        return HttpResponseRedirect('/')



class ExtLoginView(LoginView):

    def form_invalid(self, form):
        self.request.session['invalid_login'] = self.request.POST
        return HttpResponseRedirect('/')