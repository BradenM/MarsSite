from allauth.account.forms import ChangePasswordForm
from django import forms
from crispy_forms.helper import FormHelper
from phonenumber_field.formfields import PhoneNumberField
from crispy_forms.layout import Layout, Submit, Fieldset, Field, MultiField, HTML, Div
from allauth.account.forms import LoginForm, PasswordField, SetPasswordField


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
                HTML("<p id='pc_oldpassword_errors' class='help is-danger'></p >"),
                css_class="field"
            ),
            Div(
                Field('password1', css_class="input",
                      placeholder="New Password", autocomplete=False),
                HTML("<p id='pc_password1_errors' class='help is-danger'></p >"),
                css_class="field"
            ),
            Div(
                Field('password2', css_class="input",
                      placeholder="New Password (again)", autocomplete=False),
                HTML("<p id='pc_password2_errors' class='help is-danger'></p >"),
                css_class="field"
            ),
            Div(
                HTML(
                    "<a id='pc_loader' class='button is-text is-loading is-hidden'></a>"),
                Submit('submit', 'Change Password',
                       css_class="button is-info is-rounded", css_id="pc_submit")
            )
        )

    # def save(self):
    #     get_adapter().set_password(self.user, self.cleaned_data["password1"])

    def save(self):
        super(ExtChangePasswordForm, self).save()
