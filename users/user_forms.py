from allauth.account.forms import ChangePasswordForm, AddEmailForm, UserForm
from django import forms
from crispy_forms.helper import FormHelper
from phonenumber_field.formfields import PhoneNumberField
from crispy_forms.layout import Layout, Submit, Fieldset, Field, MultiField, HTML, Div
from allauth.account.forms import LoginForm, PasswordField, SetPasswordField
from allauth.account.models import EmailAddress
from .models import Profile


class ExtChangePasswordForm(ChangePasswordForm):
    oldpassword = PasswordField(label="Current Password")
    password1 = SetPasswordField(label="New Password")
    password2 = PasswordField(label="New Password (again)")

    def __init__(self, *args, **kwargs):
        super(ExtChangePasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.form_action = "/accounts/password/change/"
        self.helper.form_class = 'form'
        self.helper.form_id = 'auth_changepass'
        self.helper.layout = Layout(
            HTML(" {% csrf_token %} "),
            Div(
                Field('oldpassword', css_class="input",
                      placeholder="Current Password", autocomplete=False),
                HTML("<p id='oldpassword_error' class='help is-danger'></p >"),
                css_class="field"
            ),
            Div(
                Field('password1', css_class="input",
                      placeholder="New Password", autocomplete=False),
                HTML("<p id='password1_error' class='help is-danger'></p >"),
                css_class="field"
            ),
            Div(
                Field('password2', css_class="input",
                      placeholder="New Password (again)", autocomplete=False),
                HTML("<p id='password2_error' class='help is-danger'></p >"),
                css_class="field"
            ),
            Div(
                HTML(
                    "<a id='pc_loader' class='button is-text is-loading is-hidden'></a>"),
                Submit('submit', 'Change Password',
                       css_class="button is-info is-rounded", css_id="pc_submit")
            )
        )

    def save(self):
        super(ExtChangePasswordForm, self).save()


class ExtAddEmailForm(AddEmailForm):
    def __init__(self, *args, **kwargs):
        super(ExtAddEmailForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('email', type="hidden"),
        )

        def save(self, request):
            user_email = EmailAddress.objects.first(
                user=self.user, primary=True)
            return user_email.change(request, self.cleaned_data['email'], confirm=True)


class ChangePhoneForm(UserForm):
    phone = PhoneNumberField()

    def __init__(self, *args, **kwargs):
        super(ChangePhoneForm, self).__init__(*args, **kwargs)

    def save(self, request):
        prof = self.user.profile
        return prof.change_phone(request, self.user, self.cleaned_data['phone'])
