from django import forms
from crispy_forms.helper import FormHelper
from phonenumber_field.formfields import PhoneNumberField
from crispy_forms.layout import Layout, Submit, Fieldset, Field, MultiField, HTML, Div
from allauth.account.forms import LoginForm
from .models import Profile

class ExtSignupForm(forms.Form):
    first_name = forms.CharField(max_length=32, label='First Name', widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'input'}))
    last_name = forms.CharField(max_length=32, label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'input'}))
    phone = PhoneNumberField()

    def __init__(self, *args, **kwargs):
        super(ExtSignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = "/accounts/signup/"
        self.helper.add_input(Submit('submit', 'Sign Up', css_class="button is-info is-rounded"))
        self.helper.form_class = 'form'
        self.helper.layout = Layout(
            Div(
                Field('email', css_class='input', type="email"),
                css_class="field"
            ),
            Div(
                Field('first_name', css_class='input'),
                css_class="field"
            ),
            Div(
                Field('last_name', css_class='input'),
                css_class="field"
            ),
            Div(
                Field('phone', css_class="input"),
                css_class="field"
            ),
            Div(
                Field('password1', css_class='input'),
                css_class="field"
            ),
            Div(
                Field('password2', css_class='input'),
                css_class="field"
            ),

        )

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.profile.phone = self.cleaned_data['phone']
        user.save()
        user.profile.save()

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('phone',)

class ExtLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(ExtLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.form_action = "/accounts/login/"
        self.helper.add_input(Submit('submit', 'Login', css_class="button is-info is-rounded"))
        self.helper.form_class = 'form'
        self.helper.layout = Layout(
            Div(
                Field('login', css_class="input", type="email"),
                css_class = "field"
            ),
            Div(
                Field('password', css_class="input"),
                css_class="field"
            )
        )

    def login(self, *args, **kwargs):
        return super(ExtLoginForm, self).login(*args, **kwargs)
