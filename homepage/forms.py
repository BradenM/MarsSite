from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Fieldset, Field, MultiField, HTML
from allauth.account.forms import LoginForm


class ExtSignupForm(forms.Form):
    first_name = forms.CharField(max_length=32, label='First Name', widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'input'}))
    last_name = forms.CharField(max_length=32, label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'input'}))

    def __init__(self, *args, **kwargs):
        super(ExtSignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = "/accounts/signup/"
        self.helper.add_input(Submit('submit', 'Sign Up', css_class="button is-info is-rounded"))
        self.helper.form_class = 'form'
        self.helper.layout = Layout(
            Field('email', css_class='input', type="email"),
            Field('first_name', css_class='input'),
            Field('last_name', css_class='input'),
            Field('password1', css_class='input'),
            Field('password2', css_class='input'),
        )

    def signup(self, request, user):
        #user.email_address = self.cleaned_data['email_address']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()


class ExtLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(ExtLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = "/accounts/login/"
        self.helper.add_input(Submit('submit', 'Login', css_class="button is-info is-rounded"))
        self.helper.form_class = 'form'
        self.helper.layout = Layout(
            Field('login', css_class="input", type="email"),
            Field('password', css_class="input")
        )

    def login(self, *args, **kwargs):
        return super(ExtLoginForm, self).login(*args, **kwargs)