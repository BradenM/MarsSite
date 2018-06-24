from django import forms
from crispy_forms.helper import FormHelper
from phonenumber_field.formfields import PhoneNumberField
from crispy_forms.layout import Layout, Submit, Fieldset, Field, MultiField, HTML, Div
from allauth.account.forms import LoginForm, PasswordField, SetPasswordField
from .models import Profile
from allauth.account.adapter import get_adapter


class ExtSignupForm(forms.Form):
    first_name = forms.CharField(max_length=32, label='First Name', widget=forms.TextInput(
        attrs={'placeholder': 'First Name', 'class': 'input'}))
    last_name = forms.CharField(max_length=32, label='Last Name', widget=forms.TextInput(
        attrs={'placeholder': 'Last Name', 'class': 'input'}))
    phone = PhoneNumberField()

    def __init__(self, *args, **kwargs):
        super(ExtSignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form'
        self.helper.form_method = "post"
        self.helper.form_id = 'auth_signupform'
        self.helper.layout = Layout(
            HTML(
                "{% csrf_token %}"
            ),
            Div(
                Field('email', css_class='input', type="email"),
                HTML("<p id='email_errors' class='help is-danger'></p >"),
                css_class="field"
            ),
            Div(
                Field('first_name', css_class='input'),
                HTML("<p id='first_name_errors' class='help is-danger'></p>"),
                css_class="field"
            ),
            Div(
                Field('last_name', css_class='input'),
                HTML("<p id='last_name_errors' class='help is-danger'></p>"),
                css_class="field"
            ),
            Div(
                Field('phone', css_class="input",
                      placeholder="Your Phone Number"),
                HTML("<p id='phone_errors' class='help is-danger'></p>"),
                css_class="field"
            ),
            Div(
                Field('password1', css_class='input'),
                HTML("<p id='password1_errors' class='help is-danger'></p>"),
                css_class="field"
            ),
            Div(
                Field('password2', css_class='input'),
                HTML("<p id='password2_errors' class='help is-danger'></p>"),
                css_class="field"
            ),
            Div(
                HTML(
                    "<a id='signupform_loader' class='button is-text is-loading is-hidden'></a>"),
                Submit('submit', 'Sign Up',
                       css_class="button is-info is-rounded"),
                css_class="field"
            )

        )

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.profile.phone = self.cleaned_data['phone']
        user.save()
        user.profile.save()


class ExtLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(ExtLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.form_class = 'form'
        self.helper.form_id = 'auth_loginform'
        self.helper.layout = Layout(
            HTML(
                "{% csrf_token %}"
            ),
            Div(
                Field('login', css_class="input", type="email"),
                css_class="field"
            ),
            Div(
                Field('password', css_class="input"),
                HTML("<p id='form_errors' class='help is-danger'></p>"),
                HTML(
                    "<a id='form_loader' class='button is-text is-loading is-hidden'></a>"),
                css_class="field"
            ),
            Div(
                Submit('submit', 'Login', css_class="button is-info is-rounded"),
            )
        )

    def login(self, *args, **kwargs):
        return super(ExtLoginForm, self).login(*args, **kwargs)


