from django import forms
from .fields import CreditCardField, CCExpField
from djstripe.models import Card
from crispy_forms.layout import Layout, Submit, Fieldset, Field, MultiField, HTML, Div
from crispy_forms.helper import FormHelper

class CardForm(forms.Form):
    number = CreditCardField(required=True, label="Card Number")
    expiration = CCExpField(required=True, label="Expiration")
    ccv = forms.IntegerField(required=True, label="CCV Number",
                             max_value=9999, widget=forms.TextInput(attrs={'size': '4'}))

    def __init__(self, *args, **kwargs):
        super(CardForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = "/store/user/add-card/"
        self.helper.add_input(Submit('submit', 'Add Card'))

        self.helper.layout = Layout(
            Div(
                Field('number', css_class='input', type="email", placeholder="Card Number"),
                css_class="field"
            ),
            Div(
                Field('expiration', css_class='input', placeholder="Expiration Month"),
                css_class="field"
            ),
            Div(
                Field('ccv', css_class="input", placeholder="Security Number"),
                css_class="field"
            )

        )

        def clean(self):
            cleaned = super(CardForm, self).clean()
            if not self.errors:
                result = self.process_payment()
                if result and result[0] == 'Card declined':
                    raise forms.ValidationError('Your credit card was declined.')
                elif result and result[0] == 'Processing error':
                    raise forms.ValidationError(
                        'We encountered the following error while processing ' +
                        'your credit card: '+result[1])
            return cleaned
